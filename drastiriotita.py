import sys,os
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from PyQt5.QtCore import *
import sqlite3
import main
import style
from datetime import datetime


 

class addDrastiriotita(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Προσθήκη δραστηριότητας")
        self.setWindowIcon(QIcon("icons/add_work.png"))
        self.setGeometry(500,300,700,700)
        self.setFixedSize(self.size())
        self.connectTODb()
        self.filepath=""
        self.filename=""
        self.userid=0
        self.UI()
        self.fillCbusers()
        self.show()
    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        ###widgets top Layout
        self.addProducyimg=QLabel()
        self.img=QPixmap("icons/add_work.png")
        self.addProducyimg.setPixmap(self.img)
        self.titleText=QLabel("Προσθήκη Δραστηριότητας")
        ###widgets top right Layout
        self.dtdrastiriotitas=QCalendarWidget()
        self.btnapo=QPushButton("ΑΠΟ-->")
        self.btnapo.setStyleSheet(style.ListBtnStyle())

        self.btnapo.clicked.connect(self.passDttotext)
        self.btnmexri = QPushButton("ΜΕΧΡΙ-->")
        self.btnmexri.clicked.connect(self.passDttotextmexri)
        self.btnmexri.setStyleSheet(style.ListBtnStyle())
        self.dtapo=QLineEdit(self)
        self.dtapo.setPlaceholderText("Ημέρα Έναρξης")
        self.dtmexri=QLineEdit(self)
        self.dtmexri.setPlaceholderText("Ημέρα Πέρατος")
        ####widgets of bottom layout####
        self.lbldrastiriotita=QLabel("Τίτλος Δραστηριότητας:")
        self.drastiriotitaEntry=QLineEdit()
        self.drastiriotitaEntry.setPlaceholderText("Τίτλος")
        self.lblsxetiko = QLabel("Σχετικό:")
        self.sxetikoEntry = QLineEdit("Φ.   /   /Σ.   /")
        self.lblPerioxi = QLabel("Περιοχή:")
        self.perioxiEntry = QLineEdit()
        self.perioxiEntry.setPlaceholderText(" Εισάγετε Περιοχή")

        self.simetoxesLbl = QLabel("Απαιτήσεις:")
        self.simetoxesEntry = QTextEdit()
        self.simetoxesEntry.setStyleSheet(style.textEditStyle())
        self.lbluser=QLabel("Χειριστής:")        
        self.user=QLineEdit()
        self.uploadBtn=QPushButton("link")
        self.uploadBtn.setStyleSheet(style.ListBtnStyle())
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Καταχώρηση")
        self.submitBtn.setStyleSheet(style.ListBtnStyle())
        self.submitBtn.clicked.connect(self.addxwsimo)
        self.closeBtn = QPushButton("Κλείσιμο")
        self.closeBtn.setStyleSheet(style.ListBtnStyle())
        self.closeBtn.clicked.connect(self.uiclose)
        

    def layouts(self):
        self.totalmainLayout=QHBoxLayout()
        self.mainLayout=QVBoxLayout()

        self.topLayout=QHBoxLayout()
        self.topright=QVBoxLayout()

        self.frmrighttop=QFormLayout()
        self.bottomLayout=QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.productbottomFrame())

        ######add widgets######
        ### widget top Layout#####
        self.topLayout.addWidget(self.addProducyimg)
        self.topright.addWidget(self.dtdrastiriotitas)
        self.frmrighttop.addRow(self.btnapo,self.dtapo)
        self.frmrighttop.addRow(self.btnmexri,self.dtmexri)
        self.topright.addLayout(self.frmrighttop)
        self.topLayout.addLayout(self.topright)
        self.topFrame.setLayout(self.topLayout)

        ### widget form Layout#####
        self.bottomLayout.addRow(self.lbldrastiriotita,self.drastiriotitaEntry)
        self.bottomLayout.addRow(self.lblsxetiko, self.sxetikoEntry)
        self.bottomLayout.addRow(self.lblPerioxi, self.perioxiEntry)
        self.bottomLayout.addRow(self.lbluser, self.user)
        self.bottomLayout.addRow(self.simetoxesLbl, self.simetoxesEntry)
        self.bottomLayout.addRow("Upload", self.uploadBtn)
        self.bottomLayout.addRow("Submit", self.submitBtn)
        self.bottomLayout.addRow("close",  self.closeBtn)       
 
        self.bottomFrame.setLayout( self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        #self.simetoxesEntry.setStyleSheet(style.textEditStyle())
        self.setLayout(self.mainLayout)
    def connectTODb(self):
            self.con=sqlite3.connect("3o_grafeio.db")
            self.cur=self.con.cursor()
    def passDttotext(self):
        self.dtapo.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))
        
    def fillCbusers(self):
        query = self.cur.execute("SELECT name from members ORDER BY name ASC" ).fetchall() 
        lst=list()
        for entry in query:
            lst.append(entry[0])
        #wordList = ["alpha", "omega", "omicron", "zeta"]
        completer = QCompleter(lst, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.user.setCompleter(completer)
                
    def uiclose(self):
        self.close()
        
    def passDttotextmexri(self):
        self.dtmexri.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))
        self.validatedtmexri()
        
    def uploadImg(self):
        size = (256, 256)
        self.filepath, ok = QFileDialog.getOpenFileName(self, "select file", "", "Text Files (*.txt *.docx *.doc *.pdf *.pdf)")
        if ok:
            self.filename= os.path.basename(self.filepath)
 
            self.sxetikoEntry.setText(self.filename)
    def validatedtmexri(self):
        
        searchdtapo=self.dtapo.text()
        searchdtmexri=self.dtmexri.text() 
        if (searchdtmexri< searchdtapo):
            QMessageBox.information(self,"info","Λάθος ημερομηνίες")
            self.dtapo.clear()
            self.dtmexri.clear()
   
    def addxwsimo(self):
        perigrafi=self.drastiriotitaEntry.text().upper()
        sxetiko=self.sxetikoEntry.text().upper()
        perioxi=  self.perioxiEntry.text().upper()
        apaitiseis=self.simetoxesEntry.toPlainText().upper()
        dtapo=self.dtapo.text()
        dtmexri=self.dtmexri.text()
        klink=self.filepath
        xeiristis=self.user.text()
        try:
            userId =self.cur.execute("SELECT id FROM members WHERE name = ? ", ( xeiristis,)).fetchone()
            print(userId)
        except:
           QMessageBox.information(self, "warning", "pROBLEM το όνομα χειριστή")
           userId=0
 
        if (perigrafi!="" and sxetiko!="" and apaitiseis !=""and perioxi !="" and dtapo!=""and dtmexri!="" ):
            try:
                query="INSERT INTO upoxrewseis (perigrafi,sxetiko,dtapo,dtmexri,perioxi,apaitiseis,link,user_id) VALUES (?,?,?,?,?,?,?,?)"
                self.cur.execute(query,(perigrafi, sxetiko,dtapo, dtmexri,perioxi,apaitiseis,klink,userId[0]))
                self.con.commit()
                QMessageBox.information(self,"info","Η δραστηριότητα Καταχωρήθηκε")
            except:
                QMessageBox.information(self,"info","Δεν ολοκληρώθηκε η καταχώρηση")
        else:
           QMessageBox.information(self,"info","Συμπληρώστε τα πεδία")
    
class ChangeDrastiriotita(QWidget):
    def __init__(self,id,username):
        super().__init__()
        self.setWindowTitle("Μεταβολή δραστηριότητας")
        self.setWindowIcon(QIcon("icons/add_work.png"))
        self.setGeometry(500,300,700,700)
        self.setFixedSize(self.size())
        self.usrname=username
        self.id=id
        self.connectTODb()            
        self.findData()     
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.fillCbusers()
        self.layouts()

    def widgets(self):
        ###widgets top Layout
        self.addProducyimg=QLabel()
        self.img=QPixmap("icons/add_work.png")
        self.addProducyimg.setPixmap(self.img)
        self.titleText=QLabel("Προσθήκη Δραστηριότητας")
        ###widgets top right Layout
        self.dtdrastiriotitas=QCalendarWidget()
        self.btnapo=QPushButton("ΑΠΟ-->")
        self.btnapo.clicked.connect(self.passDttotext)
        self.btnapo.setStyleSheet(style.ListBtnStyle())
        self.btnmexri = QPushButton("ΜΕΧΡΙ-->")
        self.btnmexri.clicked.connect(self.passDttotextmexri)
        self.btnmexri.setStyleSheet(style.ListBtnStyle())
        self.dtapo=QLineEdit(self)
        self.btnapo.setStyleSheet(style.ListBtnStyle())
        self.dtapo.setInputMask('0000-00-00')
        self.dtapo.setText("{}".format(self.apo))
       
        #print(datetime.strptime(self.apo, '%Y%m%d'))
       
        self.dtmexri=QLineEdit(self)
        self.dtmexri.setText("{}".format(self.mexri))

        ####widgets of bottom layout####
        self.lbldrastiriotita=QLabel("Τίτλος Δραστηριότητας:")
        self.drastiriotitaEntry=QLineEdit()
        self.drastiriotitaEntry.setText(self.perigrafi1)
        self.lblsxetiko = QLabel("Σχετικό:")
        self.sxetikoEntry = QLineEdit(str(self.sxetiko1))
        self.lblPerioxi = QLabel("Περιοχή:")
        self.perioxiEntry = QLineEdit()
        self.perioxiEntry.setText(self.perioxi1)
        self.simetoxesLbl = QLabel("Απαιτήσεις:")
        self.simetoxesEntry = QTextEdit(str(self.apaitiseis1))
        self.simetoxesEntry.setStyleSheet(style.textEditStyle())
        self.uploadBtn=QPushButton("COMPLETED")
        self.uploadBtn.clicked.connect(self.completed)
        self.uploadBtn.setStyleSheet(style.ListBtnStyle())
        self.submitBtn = QPushButton("Update")
        self.submitBtn.setStyleSheet(style.ListBtnStyle())
        self.submitBtn.clicked.connect(self.updateElement)
        self.btnDel = QPushButton("Delete")
        self.btnDel.setStyleSheet(style.ListBtnStyle())
        self.btnDel.clicked.connect(self.deleteteElement) 
        self.closeBtn = QPushButton("Κλείσιμο")
        self.closeBtn.setStyleSheet(style.ListBtnStyle())
        self.closeBtn.clicked.connect(self.uiclose)
        self.lbluser=QLabel("Χειριστής:")
        self.user=QLineEdit(self.xeirisths)

    def layouts(self):

        self.totalmainLayout=QHBoxLayout()
        self.mainLayout=QVBoxLayout()

        self.topLayout=QHBoxLayout()
        self.topright=QVBoxLayout()

        self.frmrighttop=QFormLayout()
        self.bottomLayout=QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.productbottomFrame())

        ######add widgets######
        ### widget top Layout#####
        self.topLayout.addWidget(self.addProducyimg)
        self.topright.addWidget(self.dtdrastiriotitas)
        self.frmrighttop.addRow(self.btnapo,self.dtapo)
        self.frmrighttop.addRow(self.btnmexri,self.dtmexri)
        self.topright.addLayout(self.frmrighttop)
        self.topLayout.addLayout(self.topright)

        self.topFrame.setLayout(self.topLayout)

        ### widget form Layout#####
        self.bottomLayout.addRow(self.lbldrastiriotita,self.drastiriotitaEntry)
        self.bottomLayout.addRow(self.lblsxetiko, self.sxetikoEntry)
        self.bottomLayout.addRow(self.lblPerioxi, self.perioxiEntry)
        self.bottomLayout.addRow(self.lbluser, self.user)
        self.bottomLayout.addRow(self.simetoxesLbl, self.simetoxesEntry)
        self.bottomLayout.addRow("Upload", self.uploadBtn)
        self.bottomLayout.addRow("Submit", self.submitBtn)
        self.bottomLayout.addRow("Delete", self.btnDel)
        self.bottomLayout.addRow("close",  self.closeBtn)       
         
        self.bottomFrame.setLayout( self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)
    def connectTODb(self):
            self.con=sqlite3.connect("3o_grafeio.db")
            self.cur=self.con.cursor()

    def findData(self):
        query=("SELECT * FROM upoxrewseis WHERE id=?")
        stoixeia=self.cur.execute("SELECT upoxrewseis.id,perigrafi,sxetiko,dtapo,dtmexri,perioxi,apaitiseis,completence,members.name FROM upoxrewseis INNER JOIN members ON upoxrewseis.user_id = members.id WHERE upoxrewseis.id= ?""",(self.id,)).fetchone() 
        self.perigrafi1=  stoixeia[1]
        self.sxetiko1=  stoixeia[2]
        self.apo=  stoixeia[3]
        self.mexri=  stoixeia[4]
        self.perioxi1=  stoixeia[5]
        self.apaitiseis1=  stoixeia[6]
        #self.link1=  stoixeia[7]
        self.completence= stoixeia[7]
        self.xeirisths=stoixeia[8]

    def passDttotext(self):
        self.dtapo.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))

    def passDttotextmexri(self):
        self.dtmexri.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))
        self.validatedtmexri()
            
    def uiclose(self):
         self.close()
    def validatedtmexri(self):  
        searchdtapo=self.dtapo.text()
        searchdtmexri=self.dtmexri.text() 
        if (searchdtmexri< searchdtapo):
            QMessageBox.information(self,"info","Λάθος ημερομηνίες")
            self.dtapo.clear()
            self.dtmexri.clear()
   
    def updateElement(self):
        self.perigrafi1=  self.drastiriotitaEntry.text()
        self.sxetiko1=    self.sxetikoEntry.text()
        self.apo=  self.dtapo.text()
        self.mexri=  self.dtmexri.text()
        self.perioxi1=    self.perioxiEntry.text()
        self.apaitiseis1=  self.simetoxesEntry.toPlainText() 
        self.xeiristis=self.user.text()
        try:
            userId =self.cur.execute("SELECT id FROM members WHERE name = ? ", ( self.xeiristis,)).fetchone()
            print(userId[0])
        except:
           QMessageBox.information(self, "warning", "pROBLEM το όνομα χειριστή")
           userId=0
        try:
            query="UPDATE upoxrewseis set perigrafi=?, sxetiko=?, dtapo=?, dtmexri=?, perioxi=?, apaitiseis=?,link=?,user_id=?  WHERE id=?"
            self.cur.execute(query,(self.perigrafi1,self.sxetiko1,self.apo,self.mexri,self.perioxi1,self.apaitiseis1,"x",userId[0],self.id))
            self.con.commit()
            QMessageBox.information(self,"info","product has been updated")
        except:
            QMessageBox.information(self, "info", "product has not been updated")

    def deleteteElement(self):
        mbox =QMessageBox.question(self,"warning","Are you sure to delete this element ?",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if (mbox==QMessageBox.Yes):
            try:
                self.cur.execute("Delete FROM upoxrewseis WHERE id=?",(self.id ,))
                self.con.commit()
                QMessageBox.information(self,"info","Element has been Deleted")
                self.close()
            except:
                QMessageBox.information(self,"info","Element has not been Deleted")
    def completed(self):
        try:
            query="UPDATE upoxrewseis set completence=? WHERE id=?"
            self.cur.execute(query,("TRUE",self.id))
            self.con.commit()
            QMessageBox.information(self,"info","product has been updated")
        except:
            QMessageBox.information(self, "info", "product has not been updated")
            
    def fillCbusers(self):
        
        # for data in query:
        #     self.user.addItem(data[0]+" "+ data[1]+" "+ data[2])
        query = self.cur.execute("SELECT name from members ORDER BY name ASC" ).fetchall() 
        print(query)
        lst=list()
        for entry in query:
            lst.append(entry[0])
        #wordList = ["alpha", "omega", "omicron", "zeta"]
        print(lst)
        completer = QCompleter(lst, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.user.setCompleter(completer)

        