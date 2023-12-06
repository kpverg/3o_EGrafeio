import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3,shutil
from PIL import Image
import shutil 
from datetime import datetime
import pandas as pd
from xlsxwriter import Workbook
import style
con=sqlite3.connect("grammateia.db")
cur=con.cursor()

current_date = datetime.now()
greek_month_names = {
    1: "Ιαν",
    2: "Φεβ",
    3: "Μάρ",
    4: "Απρ",
    5: "Μάι",
    6: "Ιούν",
    7: "Ιούλ",
    8: "Αύγ",
    9: "Σεπ",
    10: "Οκτ",
    11: "Νοε",
    12: "Δεκ"
}
greek_month = greek_month_names[current_date.month]
formatted_date =f"{current_date.year} {greek_month} {current_date.day}"
current_date.strftime(" %d  %b %Y")



class kataxwrhsheggrafou(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Αριθμοί Υποφακέλου")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,550,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        ###widgets top Layout
        self.addProducyimg=QLabel()
        self.img=QPixmap("icons/add_file.png")
        self.addProducyimg.setPixmap(self.img)
        self.addProducyimg.setAlignment(Qt.AlignCenter)
        ####widgets of bottom layout####
        ####widgets left layout####
   

        self.btndel = QPushButton("Διαγραφή όλων")
        self.btndel.setStyleSheet(style.ListBtnStyle())
        self.btndel.clicked.connect(self.deleteEverything)

        self.btnupdate = QPushButton("Update")
        self.btnupdate.setStyleSheet(style.ListBtnStyle())
        self.btnupdate.clicked.connect(self.updateTables)

        self.btnfind = QPushButton("Εύρεση")
        self.btnfind.setStyleSheet(style.ListBtnStyle())
        self.btnfind.clicked.connect(self.findEntry)

        self.btnprint = QPushButton("Εκτύπωση όλων")
        self.btnprint.setStyleSheet(style.ListBtnStyle())
        self.btnprint.clicked.connect( self.printDocs)


        #self.renamer.clicked.connect(self.rename_pass)
        self.arxeiothetisibtn= QPushButton("Αρχειοθέτηση \nΕισερχομένων")
        #self.arxeiothetisibtn.clicked.connect(self.arxeiothetisifunc)
        ####widgets Right layout####
        
        self.ekserxomeno = QLabel("Εξερχόμενο")
        self.prodManufLbl = QLabel("Επέλεξε Φάκελο:")
        self.fakelosEntry  =QComboBox()
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tableNames = con.execute(query).fetchall()

        for name in tableNames:
            if  name[0] != "sqlite_sequence":
                file_name=name[0]
                self.fakelosEntry.addItem(file_name)
        self.fakelosEntry.addItem("Άλλο...")
        self.fakelosEntry.model().sort(0)

        self.fakelosEntry.currentIndexChanged.connect(self.updatecombo)
        self.ekserxomenoLbl=QLabel("Αριθμός θεματολογίου")
        self.arthematologiouEntry=QLineEdit()       # edw thelw na balw enable=false
        self.dtLbl = QLabel("Ημερομηνία εγγράφου:")
        self.dteggradouEntry = QLineEdit()
        self.dteggradouEntry.setText(formatted_date)
        self.monadaLbl = QLabel("Μονάδα/γραφείο:")
        self.monadaEntry = QLineEdit()
        self.monadaEntry.setText( "33 ΜΚ ΤΑΞ/3o ΕΓ")


        self.pliristaytotitalbl= QLabel("Πλήρης Ταυτότητα:")
        self.pliristaytotitaEntry = QLineEdit()
        self.uploadBtn=QPushButton("Καταχώρηση")
        self.uploadBtn.setStyleSheet(style.ListBtnStyle())
        self.uploadBtn.clicked.connect(self.fillTable)
        #self.submitBtn = QPushButton("Submit")
        #self.submitBtn.clicked.connect(self.fillTable)
    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottonmainlayout=QHBoxLayout()        
        self.bottomleftLayout=QVBoxLayout()
        self.bottomrightLayout=QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame = QFrame()
        
        self.bottomFrame.setStyleSheet(style.productbottomFrame())

        ######add widgets######
        ### widget top Layout#####
        self.topLayout.addWidget(self.addProducyimg)
        self.topFrame.setLayout(self.topLayout)
        ### widget botleft Layout#####

        ### widget form Layout#####
  
        self.bottomrightLayout.addRow(  self.prodManufLbl,self.fakelosEntry)
        self.bottomrightLayout.addRow(   self.ekserxomenoLbl,self.arthematologiouEntry )
  
 
        self.bottomrightLayout.addRow( self.dtLbl,self.dteggradouEntry)
        self.bottomrightLayout.addRow( self.monadaLbl ,self.monadaEntry)
        self.bottomrightLayout.addRow(  self.pliristaytotitalbl, self.pliristaytotitaEntry)
        self.bottomrightLayout.addRow("Καταχώρηση", self.uploadBtn)
        self.bottomrightLayout.addRow("Διαγραφή", self.btndel)
        self.bottomrightLayout.addRow("Update", self.btnupdate)
        self.bottomrightLayout.addRow("Εύρεση",self.btnfind)
        self.bottomrightLayout.addRow("Εκτύπωση όλων",self.btnprint)       
        self.bottonmainlayout.addLayout(self.bottomleftLayout)
        self.bottonmainlayout.addLayout(self.bottomrightLayout)
        self.bottomFrame.setLayout( self.bottonmainlayout)


        self.mainLayout.addWidget(self.topFrame,50)
        self.mainLayout.addWidget(self.bottomFrame,50)
        self.setLayout(self.mainLayout)
  
    def updatecombo(self):
        global table_name
        if self.fakelosEntry.currentText()=="Άλλο...":
            try:
                i, okPressed = QInputDialog.getInt(self, "ΘΕΜΑΤΟΛΟΓΙΟ", "Δώστε τον αριθμό φακέλου:", 1, 0, 999, 1)
                if okPressed:
                    if i<10:
                        self.fakelosEntry.addItem("f_00"+ str(i))
                        self.fakelosEntry.setCurrentText("f_00"+ str(i))
                    elif i<100:
                        self.fakelosEntry.addItem("f_0"+ str(i))
                        self.fakelosEntry.setCurrentText("f_0" + str(i))
                    elif i<990:
                        self.fakelosEntry.addItem("f_"+ str(i))
                        self.fakelosEntry.setCurrentText("f_" + str(i))
            except:
                pass
        table_name=self.fakelosEntry.currentText()
        print(table_name)

        cur.execute("CREATE TABLE IF NOT EXISTS " + table_name + "(id INTEGER PRIMARY KEY AUTOINCREMENT,perigrafi TEXT,tautotita TEXT, date_paralavis TEXT,eiserxomeno_exerxomeno TEXT)")
        con.commit()
        max_id=cur.execute("SELECT MAX(id) FROM "+table_name).fetchone()

        try:
            max=str(max_id[0]+1)
        except:
            max=str(1)
        self.arthematologiouEntry.setText(max)
        self.pliristaytotitaEntry.setText( f"{table_name.replace('f', 'Φ')}/{max}")

    def fillTable(self):
        global table_name
        # tautotita=str(self.pliristaytotitaEntry)
        # date_paralavis=str(self.dteggradouEntry)

        if self.pliristaytotitaEntry.text()!="":
            try:
                query = "INSERT INTO " + table_name + " (perigrafi,tautotita,date_paralavis) VALUES (?,?,?)"
                cur.execute(query, (self.monadaEntry.text(), self.pliristaytotitaEntry.text(), self.dteggradouEntry.text()))#perigrafi den exw
                con.commit()
                QMessageBox.information(self,"info","Η καταχώρηση ολοκληρώθηκε")                
            except:
                QMessageBox.information(self,"info","Η καταχώρηση δεν ολοκληρώθηκε")

    def updateTables(self):
        try:
            cur.execute("UPDATE " + table_name + " SET perigrafi=?, tautotita=?, date_paralavis=? WHERE id=?",
            (        self.monadaEntry.text()  ,  self.pliristaytotitaEntry.text(), self.dteggradouEntry.text(),  int(self.arthematologiouEntry.text() )))
            con.commit()
            QMessageBox.information(self,"info","Η καταχώρηση Ενημερώθηκε") 
        except:
            QMessageBox.information(self,"info","Η καταχώρηση δεν Ενημερώθηκε")

    def findEntry(self):
        x=int(self.arthematologiouEntry.text())
        data=cur.execute("SELECT * FROM " + table_name + " WHERE id = ?", ( x,)).fetchone()
        print(data[0])
        self.arthematologiouEntry.setText(str(data[0])) 
        self.dteggradouEntry.setText(data[3])  
        self.monadaEntry.setText(data[1])  
        self.pliristaytotitaEntry.setText(data[2]) 

    def printDocs(self):
 
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cur.fetchall()
        table_names = [table[0] for table in table_names]

# Δημιουργία ενός Excel writer
        excel_writer = pd.ExcelWriter('output_file.xlsx', engine='xlsxwriter')

# Επεξεργασία κάθε πίνακα και εισαγωγή των δεδομένων στο αντίστοιχο worksheet
        for table_name in table_names:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, con)
            df.to_excel(excel_writer, sheet_name=table_name, index=False)

# Κλείσιμο του Excel writer για να αποθηκευτούν οι αλλαγές στο αρχείο
        #excel_writer.save()
        excel_writer.close()

# Κλείσιμο της σύνδεσης με τη βάση δεδομένων

    def deleteEverything(self):
        result = QMessageBox.question(None,"Data Deletion Confirmation",
        f"Do you want to delete all data ?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
        if result == QMessageBox.Yes:
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            table_names = cur.fetchall()
            table_names = [table[0] for table in table_names]
            for table_name in table_names:
                cur.execute(f"DELETE FROM {table_name};")
                cur.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';")
            con.commit()
            QMessageBox.information(None, "Success", f"All data has been deleted.")
        else:
            QMessageBox.information(None, "Cancellation", "Data deletion has been canceled.")




