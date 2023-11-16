import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import style
from PIL import Image



con=sqlite3.connect("3o_grafeio.db")
cur=con.cursor()

defaultImg="store.png"

class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,350,550)
        self.setFixedSize(self.size())
        
        self.UI()
        
        self.show()

    def UI(self):
        self.widgets()
        self.fillCbusers()
        self.Layouts()

    def widgets(self):
        self.addMemberImg=QLabel()
        self.img=QPixmap('icons/addmember.png')

        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText=QLabel("Προσθήκη Χεριστή")
        self.titleText.setAlignment(Qt.AlignCenter)
        ####### Widgets for bottom Layouts#######

        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Προσθήκη Ονόματος")
        self.vathmosEntry=QLineEdit()
        self.vathmosEntry.setPlaceholderText("Προσθήκη Βαθμού")
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setPlaceholderText("Εσώτερικό Τηλέφωνο")
        self.submitbtn=QPushButton("Καταχώρηση")
        self.submitbtn.setStyleSheet(style.ListBtnStyle())
        self.submitbtn.clicked.connect(self.addMemberFunc)
        self.delbtn=QPushButton("Διαγραφή")
        self.delbtn.setStyleSheet(style.ListBtnStyle())
        self.delbtn.clicked.connect(self.delemberFunc)
        self.closeBtn = QPushButton("Κλείσιμο")
        self.closeBtn.setStyleSheet(style.ListBtnStyle())
        self.closeBtn.clicked.connect(self.uiclose)


    def Layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.productbottomFrame())
        ######## add widgets####
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Βαθμός:"), self.vathmosEntry)       
        self.bottomLayout.addRow(QLabel("Ονοματεπώνυμο:"),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Τηλ. Εσώτ:"), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitbtn)
        
        self.bottomLayout.addRow(QLabel(""), self.delbtn)       
        self.bottomLayout.addRow(QLabel(""), self.closeBtn)
        
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def addMemberFunc(self):
        txtname=self.nameEntry.text()
        txtvathmos=self.vathmosEntry.text()
        txtphone=self.phoneEntry.text()

        if(txtname and txtvathmos and txtphone !=""):

            try:
                query="INSERT INTO 'members' (vathmos,name, phone) VALUES (?,?,?)"
                cur.execute(query,(txtvathmos,txtname,txtphone))
                con.commit()
                QMessageBox.information(self,"info","Η εγγραφή Καταχωρήθηκε")
                self.nameEntry.setText("")
                self.vathmosEntry.setText("")
                self.phoneEntry.setText("")
            except:
                QMessageBox.information(self,"Warning","Η εγγραφή δεν καταχωρήθηκεd")
        else:
            QMessageBox.information(self, "Warning", "Συμπληρώστε τα κενά")
    
    def fillCbusers(self):
        query = cur.execute("SELECT name from members ORDER BY name ASC" ).fetchall() 
        lst=list()
        for entry in query:
            lst.append(entry[0])
        completer = QCompleter(lst, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.nameEntry.setCompleter(completer)
        
    def delemberFunc(self):
        txtname=self.nameEntry.text()
        found=True
        while found:
            if txtname == "":
                QMessageBox.information(self, "warning", "Συμπηρώστε το όνομα προς Διαγραφή")
                break           
            else:
                self.nameEntry.setText("")
                results =cur.execute("SELECT id,vathmos,name FROM members WHERE name LIKE ? ", ("%" + txtname + "%",)).fetchall()
                print(results)
                if results == []:
                    QMessageBox.information(self, "warning", "Δεν Βρέθηκε τέτοια εγγραφή")  
                    break
                else:          
                    for user in results: 
                        buttonReply = QMessageBox.question(self, 'Διαγραφή Προσωπικού', "Είστε σίγουρος θέλετε να διαγράψετε τον {} ;".format(user[2]), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            try:
                                cur.execute("Delete FROM members WHERE id=?",(user[0] ,))
                                con.commit()
                                QMessageBox.information(self,"info","User has been Deleted")
                                self.close()
                                found= False
                            except:
                                QMessageBox.information(self,"info","Member has not been Deleted")
                        else:
                            continue
                
    def uiclose(self):
         self.close()