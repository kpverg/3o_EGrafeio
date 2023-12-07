import os
import sqlite3
import schedule
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import *
from PIL import Image
Image.warnings.simplefilter('ignore', Image.DecompressionBombWarning)
class FileManagerApp(QWidget):
    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle("Αριθμοί Υποφακέλου")
    #     self.setWindowIcon(QIcon("icons/icon.ico"))
    #     self.setGeometry(450,150,550,750)
    #     self.setFixedSize(self.size())
    #     self.UI()
    #     self.show()

    # def UI(self):
    #     self.widgets()
    #     self.layouts()  


    # def widgets(self):


    def __init__(self):
        super(FileManagerApp, self).__init__()
        self.setWindowTitle("Ευρεση Εγγράφου")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(250,150,290,500)
        self.setFixedSize(self.size())
        # Load the previous folder path from settings or use a default value
        self.settings = QSettings("YourCompany", "FileManagerApp")
        self.folder_path = self.settings.value("FolderPath", "")

        self.selected_file = None

        self.init_ui()

        # Schedule the database update every Friday at a specific time
        schedule.every().friday.at("12:00").do(self.update_database)

        # Run the scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.start()

    def init_ui(self):
        layout = QVBoxLayout()

        # Textbox for folder path
        self.folder_path_entry = QLineEdit(self)
        self.folder_path_entry.setText(self.folder_path)
        layout.addWidget(self.folder_path_entry)

        # Button to select folder
        select_folder_button = QPushButton("Select Folder", self)
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button)

        # Button to initialize database
        initialize_button = QPushButton("Initialize Database", self)
        initialize_button.clicked.connect(self.initialize_database)
        layout.addWidget(initialize_button)

        # Textbox for file search
        self.search_entry = QLineEdit(self)
        self.search_entry.textChanged.connect(self.search_files_and_display)
        layout.addWidget(self.search_entry)

        # Button to search files
        search_button = QPushButton("Search Files", self)
        search_button.clicked.connect(self.search_files_and_display)
        layout.addWidget(search_button)

        # Listbox to display search results
        self.file_listbox = QListWidget(self)
        self.file_listbox.clicked.connect(self.on_file_selected)
        self.file_listbox.doubleClicked.connect(self.open_selected_file)
        layout.addWidget(self.file_listbox)

        # Button to open selected file
        open_button = QPushButton("Open File", self)
        open_button.clicked.connect(self.open_selected_file)
        layout.addWidget(open_button)

        # Entry for new file name
        self.new_name_entry = QLineEdit(self)
        layout.addWidget(self.new_name_entry)

        # Button to rename selected file
        rename_button = QPushButton("Rename File", self)
        rename_button.clicked.connect(self.rename_selected_file)
        layout.addWidget(rename_button)

        # Button to close the application
        close_button = QPushButton("Close App", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Button to delete the database
        delete_database_button = QPushButton("Delete Database", self)
        delete_database_button.clicked.connect(self.delete_database)
        layout.addWidget(delete_database_button)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        # self.setCentralWidget(central_widget)
        self.show()
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", self.folder_path)
        if folder_path:
            self.folder_path = folder_path
            self.folder_path_entry.setText(folder_path)

            # Save the chosen folder path to settings
            self.settings.setValue("FolderPath", folder_path)

    def initialize_database(self):
        if self.folder_path:
            self.scan_folder()
            self.search_files_and_display()

    def scan_folder(self):
        conn=sqlite3.connect(os.path.abspath('db_Servises/file_database.db'))
 
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS files (name TEXT, path TEXT)''')

        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx')):
                    file_path = os.path.join(root, file)
                    c.execute("SELECT * FROM files WHERE name=? AND path=?", (file, file_path))
                    existing_entry = c.fetchone()

                    if not existing_entry:
                        # Insert new entry
                        c.execute("INSERT INTO files VALUES (?, ?)", (file, file_path))
                        # # Update existing entry
                        # c.execute("UPDATE files SET name=?, path=? WHERE name=? AND path=?",
                        #         (file, file_path, existing_entry[0], existing_entry[1]))
                    else:
                        pass

        conn.commit()
        conn.close()

    def search_files_and_display(self):
        query = self.search_entry.text()
        conn = sqlite3.connect('file_database.db')
        c = conn.cursor()
        c.execute("SELECT name FROM files WHERE name LIKE ?", (query + '%',))
        files = c.fetchall()
        self.file_listbox.clear()
        for file in files:
            self.file_listbox.addItem(file[0])

        conn.close()

    def on_file_selected(self):
        selected_item = self.file_listbox.currentItem()
        if selected_item:
            self.selected_file = selected_item.text()

    def open_selected_file(self):
        if self.selected_file:
            conn = sqlite3.connect('file_database.db')
            c = conn.cursor()
            c.execute("SELECT * FROM files WHERE name=?", (self.selected_file,))
            selected_file = c.fetchone()

            # Check if the file is a PDF
            if selected_file[1].lower().endswith('.pdf'):
                self.open_pdf_file(selected_file[1])
            else:
                print("Selected file is not a PDF.")

            conn.close()

    def open_pdf_file(self, file_path):
        try:
            # Use the default PDF viewer
            os.startfile(file_path)
        except Exception as e:
            print(f"Error opening PDF file: {e}")

    def rename_selected_file(self):
        new_name = self.new_name_entry.text()
        if self.selected_file and new_name:
            conn = sqlite3.connect('file_database.db')
            c = conn.cursor()
            c.execute("SELECT * FROM files WHERE name=?", (self.selected_file,))
            selected_file = c.fetchone()
            new_path = os.path.join(os.path.dirname(selected_file[1]), new_name)
            os.rename(selected_file[1], new_path)
            c.execute("UPDATE files SET name=?, path=? WHERE name=? AND path=?",
                      (new_name, new_path, selected_file[0], selected_file[1]))
            conn.commit()
            conn.close()
            self.search_files_and_display()

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def update_database(self):
        print("Updating database...")
        if self.folder_path:
            self.scan_folder()

    def delete_database(self):
        confirm = QMessageBox.question(self, 'Delete Database', 'Are you sure you want to delete the database?',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            os.remove('file_database.db')
            print("Database deleted.")

# if __name__ == '__main__':
#     app = QApplication([])
#     window = FileManagerApp()
#     window.show()
#     app.exec_()
