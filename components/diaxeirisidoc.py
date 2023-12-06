import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3,shutil
from PIL import Image
import shutil 
from datetime import datetime
con=sqlite3.connect("grammateia.db")
cur=con.cursor()

current_date = datetime.now()
formatted_date = current_date.strftime("%Y_%m_%d")

class kataxwrhsheggrafou(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Διαχείριση Εγγράφου")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,550,550)
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
        ####widgets of bottom layout####
        ####widgets left layout####
        self.eiserxomeno = QLabel("Εισερχόμενο")
        self.renamer = QPushButton("Rename Files")
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
            if name[0] != "thematologio" and name[0] != "upoxrewseis" and name[0] != "sqlite_sequence":
                file_name=name[0]


                self.fakelosEntry.addItem(file_name)
        self.fakelosEntry.addItem("Άλλο...")

        self.fakelosEntry.currentIndexChanged.connect(self.updatecombo)
        self.ekserxomenoLbl=QLabel("Αριθμός θεματολογίου")
        self.arthematologiouEntry=QLabel()       # edw thelw na balw enable=false
        self.protokolloLbl = QLabel("Αριθμός Πρωτόκολλου:")
        self.arprotokollouEntry = QLineEdit()
        self.arprotokollouEntry.setPlaceholderText("Εισάγετε Αριθμό Πρωτοκόλλου")
        self.arprotokollouEntry.returnPressed.connect(self.auto_fillQline)

        self.sxedioLbl = QLabel("Αριθμός Σχεδίου:")
        self.arithmosSxediouEntry = QLineEdit()
        self.arithmosSxediouEntry.setPlaceholderText("Εισάγετε Αριθμό Σχεδίου")
        self.arithmosSxediouEntry.returnPressed.connect(self.auto_fillQline)
        self.dtLbl = QLabel("Ημερομηνία εγγράφου:")
        self.dteggradouEntry = QLineEdit()
 
        self.dteggradouEntry.setText(formatted_date)
        self.dteggradouEntry.returnPressed.connect(self.auto_fillQline)

        self.monadaLbl = QLabel("Μονάδα/γραφείο:")
        self.monadaEntry = QLineEdit()
        self.monadaEntry.setText( "33 ΜΚ ΤΑΞ/3o ΕΓ")
        self.monadaEntry.returnPressed.connect(self.auto_fillQline)

        self.pliristaytotitalbl= QLabel("Πλήρης Ταυτότητα:")
        self.pliristaytotitaEntry = QLineEdit()
        self.uploadBtn=QPushButton("Upload")
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
        # self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame = QFrame()
        #self.bottomLayout = QFormLayout()
        # self.bottomFrame.setStyleSheet(style.productbottomFrame())

        ######add widgets######
        ### widget top Layout#####
        self.topLayout.addWidget(self.addProducyimg)
        self.topFrame.setLayout(self.topLayout)
        ### widget botleft Layout#####

        ### widget form Layout#####
        self.bottomrightLayout.addRow( self.ekserxomeno )
        self.bottomrightLayout.addRow(  self.prodManufLbl,self.fakelosEntry)
        self.bottomrightLayout.addRow(   self.ekserxomenoLbl,self.arthematologiouEntry )
        self.bottomrightLayout.addRow( self.protokolloLbl,self.arprotokollouEntry)
        self.bottomrightLayout.addRow( self.sxedioLbl,self.arithmosSxediouEntry)
        self.bottomrightLayout.addRow( self.dtLbl,self.dteggradouEntry)
        self.bottomrightLayout.addRow( self.monadaLbl ,self.monadaEntry)
        self.bottomrightLayout.addRow(  self.pliristaytotitalbl, self.pliristaytotitaEntry)
        self.bottomrightLayout.addRow("Καταχώρηση", self.uploadBtn)
        self.bottonmainlayout.addLayout(self.bottomleftLayout)
        self.bottonmainlayout.addLayout(self.bottomrightLayout)
        self.bottomFrame.setLayout( self.bottonmainlayout)


        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
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
        print(max_id[0])
        try:
           int(max_id[0])
           self.arthematologiouEntry.setText(str(max_id[0]+1))
        except:
            self.arthematologiouEntry.setText(str(1))
    def fillTable(self):
        global table_name
        tautotita=str(self.pliristaytotitaEntry)
        date_paralavis=datetime.datetime.now()
        eiserxomeno_exerxomeno="ΕΞΕΡΧΟΜΕΝΟ"
        if tautotita!="":
            try:
                query = "INSERT INTO " + table_name + " (perigrafi,tautotita,date_paralavis,eiserxomeno_exerxomeno) VALUES (?,?,?,?)"
                cur.execute(query, ("", tautotita, date_paralavis, eiserxomeno_exerxomeno))#perigrafi den exw
                con.commit()
            except:
                QMessageBox.information(self,"info","Η καταχώρηση δεν ολοκληρώθηκε")
    def auto_fillQline(self):
        pass
       # if( self.fakelosEntry.currentText()!=""and self.arthematologiouEntry.text()   !=""  and  self.arprotokollouEntry.text()!=""and self.arithmosSxediouEntry.text()!=""and self.dteggradouEntry.text()!=""and self.monadaEntry.text()!=""):
      #      self.pliristaytotitaEntry.setText(self.fakelosEntry.currentText() +"_"+ self.arthematologiouEntry.text() +"_"+self.arprotokollouEntry.text()+"_"+self.arithmosSxediouEntry.text()+"_"+self.dteggradouEntry.text()+"_"+self.monadaEntry.text())
    def arxeiothetisifunc(self):
        directory = QFileDialog.getExistingDirectory()
        for root, dirs, files in os.walk(directory):
            for fname in files:
                if ".pdf" in fname:
                    old_name = fname
                    new_name = "f_"+old_name[2:5]
                    ar_fak=str(old_name[2:3])
                    ar_upofakfak=str(old_name[3:5])
                    cur.execute("CREATE TABLE IF NOT EXISTS " +  new_name + "(id INTEGER PRIMARY KEY AUTOINCREMENT,link TEXT,tautotita TEXT, date_paralavis TEXT,eiserxomeno_exerxomeno TEXT)")
                    con.commit()
                    max_id = cur.execute("SELECT MAX(id) FROM " + new_name).fetchone()
                    try:
                        int(max_id)
                        max_id+=1
                    except :
                        max_id=1
                    try:
                        old_name = os.path.join(root, fname)
                        new_nm = os.path.join(root, str(max_id)+"__"+fname)
                        os.rename(old_name, new_nm)
                    except:
                        pass
                new_path="/home/thedoctorlptp/Επιφάνεια εργασίας/ΘΕΜΑΤΟΛΟΓΙΟ"
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = "/home/thedoctorlptp/Επιφάνεια εργασίας/ΘΕΜΑΤΟΛΟΓΙΟ/"+ ar_fak +"00"
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                new_path = "/home/thedoctorlptp/Επιφάνεια εργασίας/ΘΕΜΑΤΟΛΟΓΙΟ/"+ar_fak+"00/"+ar_fak+ar_upofakfak
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                shutil.move(new_nm , new_path+"/"+ str(max_id)+"__"+fname)
                link=new_path+"/"+ str(max_id)+"__"+fname
                tautotita=str(max_id)+"__"+fname
                date_paralavis=datetime.datetime.now()
                eiserxomeno_exerxomeno="ΕΙΣΕΡΧΟΜΕΝΟ"
                query = "INSERT INTO " + new_name + " (link,tautotita,date_paralavis,eiserxomeno_exerxomeno) VALUES (?,?,?,?)"
                cur.execute(query, (link, tautotita, date_paralavis, eiserxomeno_exerxomeno))  # perigrafi den exw
                con.commit()