import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import drastiriotita,diaxeirisieggrafou
import datetime
import style

from PyQt5 import QtCore
import components.addmember
#os.path.join(os.path.abspath("../../../"), "lib")
con = sqlite3.connect("3o_grafeio.db")
cur = con.cursor()
months={1:"Ιανουάριος",
        2:"Φεβρουάριος",
        3:"Μάρτιος",
        4:"Απρίλιος",
        5:"ΜάΙος",
        6:"Ιούνιος",
        7:"Ιούλιος",
        8:"Αύγουστος",
        9:"Σεπτέβριος",
        10:"Οκτώβριο;",
        11:"Νοέμβριος",
        12:"Δεκέμβριος"
        }

global data
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Βοηθός 3ου Γραφείου ")
        #self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450, 150, 1050, 700)
        self.setFixedSize(self.size())
        self.users=dict()
        self.fillusers()       
        self.UI()
        self.show()


    def UI(self):
        self.toolBar()
        self.tabWigdet()
        self.widgets()
        self.layouts()
        self.displaydrasthriotites()


    # ToolButtonTextUnderIcon
    def toolBar(self):
        self.tb = self.addToolBar("toolBar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ##############Toolbar Btn#############

        ##############Add member ##############

        ##############Add drastiriotita##############
        self.adddrastriotita = QAction(QIcon('icons/add_file.png'), "Προσθήκη \nΔραστηριότητας", self)
        self.tb.addAction(self.adddrastriotita)
        self.adddrastriotita.triggered.connect(self.addnewdrastriotita)
        self.tb.addSeparator()
        ##############Add member ##############
        self.addMember = QAction(QIcon('icons/users.png'), "Add Member", self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()
        
    def tabWigdet(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)
        # self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Δραστηριότητες")
        self.tabs.addTab(self.tab2, "Hμερολόγιο")
        #self.tabs.addTab(self.tab3, "Statistics")

    def widgets(self):
        #### tab1 Widgets######
        ##### Product table widget######
        ######main left layout#######
        self.dispdrastiriotites = QTableWidget()
        self.dispdrastiriotites.setWordWrap(True)
        self.dispdrastiriotites.setColumnCount(5)
        self.dispdrastiriotites.setColumnHidden(0, True)
        self.dispdrastiriotites.setHorizontalHeaderItem(0, QTableWidgetItem("id"))
        self.dispdrastiriotites.setHorizontalHeaderItem(1, QTableWidgetItem("ΠΕΡΙΓΡΑΦΗ"))
        self.dispdrastiriotites.setHorizontalHeaderItem(2, QTableWidgetItem("ΑΠΟ"))
        self.dispdrastiriotites.setHorizontalHeaderItem(3, QTableWidgetItem("ΜΕΧΡΙ"))
        self.dispdrastiriotites.setHorizontalHeaderItem(4, QTableWidgetItem("ΧΕΙΡΙΣΤΗΣ"))       
        #self.dispdrastiriotites.setHorizontalHeaderItem(4, QTableWidgetItem("ΠΕΡΙΟΧΗ"))
        #self.dispdrastiriotites.setHorizontalHeaderItem(5, QTableWidgetItem("ΑΠΑΙΤΗΣΕΙΣ"))
        self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)       
        #self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        #self.dispdrastiriotites.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.dispdrastiriotites.doubleClicked.connect(self.selectdrastiriotita )
        #self.dispdrastiriotites.doubleClicked.connect(self.searchdrastiriotita)

        ######main right top  layout#######
        self.searchText = QLabel()
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Αναζήτηση Βάση περιγραφής..?")
        self.searchButton = QPushButton("Αναζήτηση")
        self.searchButton.clicked.connect(self.searchdrastiriotita)
        self.searchButton.setStyleSheet(style.searchBtnStyle())

        ######main right middle  layout#######
        self.AtoZ = QRadioButton("A--->Z")
        self.dtsort = QRadioButton("Ημέρα έναρξης")
        self.OnlyMonth = QRadioButton("Ολόκληρου Μήνα")
        self.OnlyMonth.clicked.connect(self.findDataMonth)
        self.SpecPeriod = QRadioButton("Συγκεκριμένης Περιόδου")
        self.SpecPeriod.clicked.connect(self.selectRangeOfDates)
        self.totalDrastiriotita = QRadioButton("Ολοκληρωμένες")
        self.ListBtn=QPushButton("Δημιουργία")
        self.ListBtn.clicked.connect(self.createListDrastiriotita)
        self.ListBtn.setStyleSheet(style.ListBtnStyle())
#### tab2 Widgets######
        self.imerologio= QCalendarWidget()
        self.imerologio.clicked.connect(self.sorttolist)
        self.tasks=QListWidget()
        self.nextDt=QPushButton("Next")
            
    def layouts(self):
        #######tab1 Layouts #####
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.rightTopLayout = QVBoxLayout()
        self.rightMiddleLayout = QVBoxLayout()
        self.topGroupBox = QGroupBox("Αναζήτηση")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox = QGroupBox("")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())
        self.bottomGroupBox = QGroupBox()
        ###add widgets#####
        ###Left main layout widgets###
        self.mainLeftLayout.addWidget(self.dispdrastiriotites)
        ###right top layout widgets###
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)

        ###right middle layout widgets###
        self.rightMiddleLayout.addWidget(self.AtoZ)
        self.rightMiddleLayout.addWidget( self.dtsort)
        self.rightMiddleLayout.addWidget(self.OnlyMonth)
        self.rightMiddleLayout.addWidget(self.SpecPeriod)
        self.rightMiddleLayout.addWidget(self.totalDrastiriotita)
        self.rightMiddleLayout.addWidget(self.ListBtn)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)
        self.mainRightLayout.addWidget(self.topGroupBox, 40)
        self.mainRightLayout.addWidget(self.middleGroupBox, 60)
        #self.mainRightLayout.addWidget(self.bottomGroupBox, 60)
        self.mainLayout.addLayout(self.mainLeftLayout, 80)
        self.mainLayout.addLayout(self.mainRightLayout, 20)
        self.tab1.setLayout(self.mainLayout)  
        self.mainLayout2 = QHBoxLayout()
        self.mainLeftLayout2 = QVBoxLayout()
        self.mainRightLayout2 = QVBoxLayout()
        self.mainLeftLayout2.addWidget(self.imerologio)
        self.mainRightLayout2.addWidget(self.tasks)
        #self.mainRightLayout2.addWidget(self.nextDt)
        self.mainLayout2.addLayout(self.mainLeftLayout2, 40)
        self.mainLayout2.addLayout(self.mainRightLayout2, 60)
        self.tab2.setLayout(self.mainLayout2) 
        self.tabs.blockSignals(False)

    def selectdrastiriotita(self):
         
        listDrastiriotita=[]
        for i in range(0,4):
            listDrastiriotita.append(self.dispdrastiriotites.item(self.dispdrastiriotites.currentRow(),i).text())
        drastiriotitaId=listDrastiriotita[0]
        username=listDrastiriotita[3]
        self.displayMember=drastiriotita.ChangeDrastiriotita(drastiriotitaId,username)

    def sorttolist(self):
        self.tasks.clear()
        self.tasks.wordWrap()
        dtOfInterest=self.imerologio.selectedDate().toString(QtCore.Qt.ISODate)
        i=0
        query = cur.execute("SELECT perigrafi,dtapo,dtmexri,apaitiseis from upoxrewseis where completence=? ORDER BY perigrafi ASC",("FALSE",) ).fetchall()        
        
        for row_data in query:
            if  row_data[1]<=dtOfInterest and row_data[2]>=dtOfInterest:
                i+=1 
                self.tasks.setWordWrap(True)
                self.tasks.addItem( str(i) +" "+ row_data[0]+"\n"+"Εναρξη:" +row_data[1]+"\n"+" Λήξη: "+row_data[2]+"\n"+"Απαιτήσεις:"+row_data[3]+"\n")
                
    def funcAddMember(self):
        self.newMember= components.addmember.AddMember()
        
    def addnewdrastriotita(self):
        self.newdrastitita = drastiriotita.addDrastiriotita()

    def searchdrastiriotita(self):
        value = self.searchEntry.text().upper()
        if value == "":
            QMessageBox.information(self, "warning", "Συμπηρώστε το κείμενο αναζήτησης")
        else:
            self.searchEntry.setText("")
            query = (
                "SELECT id,perigrafi,dtapo,dtmexri, user_id FROM upoxrewseis WHERE perigrafi LIKE ? or perioxi LIKE ? "
                "or apaitiseis LIKE ? ")
            results = cur.execute(query, ("%" + value + "%","%" + value + "%", "%" + value + "%")).fetchall()
            if results == []:
                QMessageBox.information(self, "warning", "Δεν υπάρχει τέτοια Δραστηριότητα")
            else:
                for i in reversed(range(self.dispdrastiriotites.rowCount())):
                    self.dispdrastiriotites.removeRow(i)
                for row_data in results:
                    row_number = self.dispdrastiriotites.rowCount()
                    self.dispdrastiriotites.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def displaydrasthriotites(self):
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        #query = cur.execute("SELECT id,perigrafi,dtapo,dtmexri,user_id from upoxrewseis where completence=?",("FALSE",) ).fetchall()
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri , members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ?""",("FALSE",))
        query=cur.fetchall()
       
        for row_data in query:
            #userNAme=self.finduser(row_data[4])
            #row_data[4]=userNAme
            row_number = self.dispdrastiriotites.rowCount()
            self.dispdrastiriotites.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displaydrasthriotitesAtoZ(self):
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri ,members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ? ORDER BY perigrafi ASC",("FALSE",))
        query=cur.fetchall()
        for row_data in query:
            row_number = self.dispdrastiriotites.rowCount()
            self.dispdrastiriotites.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def createListDrastiriotita(self):
        global data
        if self.AtoZ.isChecked()== True:
            self.displaydrasthriotitesAtoZ()
        elif self.dtsort.isChecked() == True:            
            self.displaydrasthriotitesdtsorted()
        elif self.OnlyMonth.isChecked() == True:
            self.displayOnlyMonth()
        elif self.SpecPeriod.isChecked() == True:
            self.displaySpecPeriod()

        elif  self.totalDrastiriotita.isChecked() == True:
            self.displayCompleteddrasthriotites()
        
    def displayCompleteddrasthriotites(self):
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri ,members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ?""",("TRUE",))
        query=cur.fetchall()       
       
        for row_data in query:
            row_number = self.dispdrastiriotites.rowCount()
            self.dispdrastiriotites.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displayOnlyMonth(self):
        global data
        key_list = list(months.keys())
        val_list = list(months.values())
        position = val_list.index(data[0][1])
        etos=data[0][0]
        minas=key_list[position]
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri ,members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ?""",("FALSE",))
        query=cur.fetchall()          
        for row_data in query:
            datee = datetime.datetime.strptime(row_data[2], "%Y-%m-%d")
            if datee.month==minas and datee.year==int(etos):
                row_number = self.dispdrastiriotites.rowCount()
                self.dispdrastiriotites.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displaydrasthriotitesdtsorted(self):
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri ,members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ? ORDER BY dtapo""",("FALSE",))
        query=cur.fetchall()          
        for row_data in query:
            row_number = self.dispdrastiriotites.rowCount()
            self.dispdrastiriotites.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)
                
    def displaySpecPeriod(self):
        global data
        searchdtapo=datetime.datetime.strptime(data[0][0], "%Y-%m-%d")
        searchdtmexri=datetime.datetime.strptime(data[0][1], "%Y-%m-%d")
        self.dispdrastiriotites.setFont(QFont("Times", 12))
        for i in reversed(range(self.dispdrastiriotites.rowCount())):
            self.dispdrastiriotites.removeRow(i)
        cur.execute("SELECT upoxrewseis.id,perigrafi, dtapo , dtmexri ,members.name FROM upoxrewseis  INNER JOIN members ON upoxrewseis.user_id = members.id WHERE completence= ?""",("FALSE",))
        query=cur.fetchall()
        for row_data in query:
            dateApo = datetime.datetime.strptime(row_data[2], "%Y-%m-%d")
            dateMexri = datetime.datetime.strptime(row_data[3], "%Y-%m-%d") 
                      
            if (searchdtapo>=dateApo and searchdtmexri<=dateMexri):
                row_number = self.dispdrastiriotites.rowCount()
                self.dispdrastiriotites.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)                 
            elif (searchdtapo<=dateApo and searchdtmexri>=dateApo and searchdtmexri<=dateMexri):
                row_number = self.dispdrastiriotites.rowCount()
                self.dispdrastiriotites.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)  
            elif(searchdtapo>=dateApo and searchdtapo<=dateMexri and searchdtmexri>=dateMexri): #or (searchdtapo<dateApo   and searchdtmexri>dateMexri) :
                row_number = self.dispdrastiriotites.rowCount()
                self.dispdrastiriotites.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)  
            elif (searchdtapo<= dateApo and searchdtmexri>=dateMexri):
                row_number = self.dispdrastiriotites.rowCount()
                self.dispdrastiriotites.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.dispdrastiriotites.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.dispdrastiriotites.setEditTriggers(QAbstractItemView.NoEditTriggers)           
                               
    def fillusers(self):
        query = cur.execute("SELECT * from members " ).fetchall()
        
        for data in query:
            
            self.users.update({data[0]:data[1]+" "+data[2]+" "+data[3]})            
    
    def  findDataMonth(self):
        global data
        data=list()
        self.selectionmina = selctMonth()
        
    def selectRangeOfDates(self):
        global data
        data=list()
        self.selectionmina = selectRangeOfDates()

class selctMonth(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Επιλογή Μήνα")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(500,300,300,300)
        self.setFixedSize(self.size())
        self.packetOfData=list()
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.Layouts()

    def widgets(self):
        self.addMemberImg=QLabel()
        #self.img=QPixmap('icons/addmember.png')

        #self.addMemberImg.setPixmap(self.img)
        #self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText=QLabel("Επιλέξτε Μήνα-Έτος")
        self.titleText.setAlignment(Qt.AlignCenter)
        ####### Widgets for bottom Layouts#######
        self.MonthEntry=QComboBox()
        self.EtosEntry=QComboBox()
        for month in months:
            self.MonthEntry.addItem(str(months[month]))
        for i in range(-1, 2):
            self.EtosEntry.addItem(str(datetime.datetime.now().year+i))
        self.EtosEntry.setCurrentText(str(datetime.datetime.now().year))
        self.MonthEntry.setCurrentText(str(months[datetime.datetime.now().month]))
        self.bltepilogi=QPushButton("Επιλογή")
        self.bltepilogi.clicked.connect(self.returnValues)
        self.bltepilogi.setStyleSheet(style.ListBtnStyle())

    
    
    def Layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()

        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.productbottomFrame())
        ######## add widgets####
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget( self.MonthEntry)


        self.topLayout.addWidget( self.EtosEntry)

        self.topLayout.addWidget( self.bltepilogi)
        self.setLayout(self.topLayout)
        
    def returnValues(self):
        global data        
        minas = self.MonthEntry.currentText()
        etos=self.EtosEntry.currentText()
        self.packetOfData.append([etos, minas])
        data= self.packetOfData
        self.close()
        
class selectRangeOfDates(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Προσθήκη δραστηριότητας")
        self.setWindowIcon(QIcon("icons/add_work.png"))
        self.setGeometry(450,150,700,550)
        self.setFixedSize(self.size())
        self.UI()
        self.show()
        self.connectTODb()
        self.filepath=""
        self.filename=""

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
        self.btnmexri.setStyleSheet(style.ListBtnStyle())
        self.btnmexri.clicked.connect(self.passDttotextmexri)
        self.dtapo=QLineEdit(self)
        self.dtapo.setPlaceholderText("Ημέρα Έναρξης")
        self.dtmexri=QLineEdit(self)
        self.dtmexri.setPlaceholderText("Ημέρα Πέρατος")
        self.submitBtn = QPushButton("Επιλογή")
        self.submitBtn.setStyleSheet(style.ListBtnStyle())
        self.submitBtn.clicked.connect(self.returnValues)

    def layouts(self):
        self.totalmainLayout=QHBoxLayout()
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.topright=QVBoxLayout()
        self.frmrighttop=QFormLayout()
        self.bottomLayout=QFormLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()  

        ######add widgets######
        ### widget top Layout#####
        self.topLayout.addWidget(self.addProducyimg)
        self.topright.addWidget(self.dtdrastiriotitas)
        self.frmrighttop.addRow(self.btnapo,self.dtapo)
        self.frmrighttop.addRow(self.btnmexri,self.dtmexri)
        self.topright.addLayout(self.frmrighttop)
        self.topLayout.addLayout(self.topright)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow("Submit", self.submitBtn)
        self.bottomFrame.setLayout( self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)
        
    def connectTODb(self):
        self.con=sqlite3.connect("3o_grafeio.db")
        self.cur=self.con.cursor()
        
    def Layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.topFrame=QFrame()
        self.bottomFrame=QFrame()
        ######## add widgets####
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget( self.MonthEntry)
        self.topLayout.addWidget( self.EtosEntry)
        self.topLayout.addWidget( self.bltepilogi)
        self.setLayout(self.topLayout)
        
    def passDttotext(self):
        self.dtapo.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))

    def passDttotextmexri(self):
        self.dtmexri.setText(self.dtdrastiriotitas.selectedDate().toString(QtCore.Qt.ISODate))

    def returnValues(self):
        global data
        self.packetOfData=list()        
        selectedDTapo=self.dtapo.text()
        selectedDTmexri=self.dtmexri.text()
        self.packetOfData.append([selectedDTapo, selectedDTmexri])
        data= self.packetOfData
        self.close()

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()