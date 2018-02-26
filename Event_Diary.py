# -*- coding: utf-8 -*-

import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QWidget,QFileDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QTableView, QCalendarWidget, QDoubleSpinBox, QLabel, QVBoxLayout, QHBoxLayout, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication, Qt, QDateTime, QTime, QDate
from sys import argv, exit
from functools import partial
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel,QSqlRecord
import common as cm

class event_diary_window(QMainWindow):
    def __init__(self,parent=None):
        super(event_diary_window, self).__init__(parent)
        self.db1 = self.connect_db()
        self.setWindowTitle('Event Diary')
        self.setWindowIcon(QIcon(os.path.join(cm.LOGO_DIR,'event_planner.png')))
        self.setGeometry(100, 100, 840, 740)
        self.main_layout = QWidget()
        self.grid = QGridLayout()
        self.main_layout.setLayout(self.grid)
        
        self.home()
        
    def home(self):
        
        self.grid.columnMinimumWidth(9)
        self.grid.rowMinimumHeight(8)
        #self.grid.rowStretch(8)
        #self.grid.columnStretch(8)
        self.display_contents(self.db1)
        self.button_add = QPushButton('Add', self.main_layout)
        self.button_add.clicked[bool].connect(self.insert_db)
        
        self.button_del = QPushButton('Delete', self.main_layout)
        self.button_del.clicked[bool].connect(self.del_row)
                
        self.view1.clicked.connect(self.cellclicked)
        self.view1.clicked.connect(self.cellclicked)
        self.view1.doubleClicked.connect(self.cellDBclicked)                      
        self.grid.addWidget(self.view1, 0, 0, 7, 3, Qt.AlignLeft)
        self.grid.addWidget(self.button_add, 7, 0, 1, 1, Qt.AlignLeft)
        self.grid.addWidget(self.button_del, 7, 1, 1, 1, Qt.AlignCenter)
        
        self.setCentralWidget(self.main_layout)
        
        
        self.show()

    def cellDBclicked(self, item):
        print(item.data())
        print(item.row())
        self.edit_cell()
        print(type(item))
        #view.update()
        #item.setData()

    def cellclicked(self, item):
        self.curindex = item
        
        self.button_edit = QPushButton('Edit', self.main_layout)
        self.grid.addWidget(self.button_edit, 7, 2, 1, 1, Qt.AlignRight)
        self.button_edit.clicked[bool].connect(self.edit_cell)
        if(self.curindex.column()==1):
            self.adjacent= self.curindex.sibling(self.curindex.row(),0)
        else:
            self.adjacent= self.curindex.sibling(self.curindex.row(),1)
        
        #self.show()
        pass
    
    def init_widgets(self):
        if(self.curindex.column()==0):
            givendatetime= QDateTime.fromString(self.curindex.data())
            self.cal.setSelectedDate(givendatetime.date())
            self.messageEdit.setLineWidth(140)
            self.messageEdit.setText(self.adjacent.data())
            self.hrspinbox.setValue(givendatetime.time().hour())
            self.minspinbox.setValue(givendatetime.time().minute())
            self.secspinbox.setValue(givendatetime.time().second())
        else:
            print(self.adjacent.data())
            givendatetime= QDateTime.fromString(self.adjacent.data())
            self.cal.setSelectedDate(givendatetime.date())
            self.messageEdit.setLineWidth(140)
            self.messageEdit.setText(self.curindex.data())
            self.hrspinbox.setValue(givendatetime.time().hour())
            self.minspinbox.setValue(givendatetime.time().minute())
            self.secspinbox.setValue(givendatetime.time().second())
    def edit_cell(self):
        
        self.button_add.setDisabled(True)
        self.button_del.setDisabled(True)
        self.button_edit.setDisabled(True)
        
        self.cal = QCalendarWidget()
        self.grid.addWidget(self.cal, 0, 4, 2, 2)
        print(self.cal.selectedDate())
        
        self.hrspinbox=QDoubleSpinBox()
        self.hrspinbox.setRange(0,23)
        self.hrspinbox.setDecimals(0)
        self.minspinbox=QDoubleSpinBox()
        self.minspinbox.setRange(0,59)
        self.minspinbox.setDecimals(0)
        self.secspinbox=QDoubleSpinBox()
        self.secspinbox.setRange(0,59)
        self.secspinbox.setDecimals(0)
        
        self.l1, self.l2, self.l3 = QLabel('Hrs'), QLabel('Mins'), QLabel('Sec')
        vbox1, vbox2,vbox3 = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()
        
        vbox1.addWidget(self.l1)
        vbox1.addWidget(self.hrspinbox)
        
        vbox2.addWidget(self.l2)
        vbox2.addWidget(self.minspinbox)
        
        vbox3.addWidget(self.l3)
        vbox3.addWidget(self.secspinbox)
        
        self.hbox=QHBoxLayout()
        self.hbox.addLayout(vbox1)
        self.hbox.addStretch(1)
        self.hbox.addLayout(vbox2)
        self.hbox.addStretch(1)
        self.hbox.addLayout(vbox3)
        self.grid.addLayout(self.hbox, 3, 4, 1, 1)
        
        
        self.message = QLabel('Message')

        self.messageEdit = QTextEdit()
        self.grid.addWidget(self.message, 4, 4, 1, 1)
        self.grid.addWidget(self.messageEdit, 5, 4, 1, 1)
        
        self.init_widgets()
        
        self.button_Save = QPushButton('Save', self.main_layout)
        self.button_Save.clicked[bool].connect(self.save_tempdata)
        #button_edit.clicked[bool].connect(self.edit_cell)
        self.button_Discard = QPushButton('Discard', self.main_layout)
        self.button_Discard.clicked[bool].connect(self.discard_tempdata)

        self.grid.addWidget(self.button_Save, 7, 4, 1, 1, Qt.AlignRight)
        self.grid.addWidget(self.button_Discard, 7, 5, 1, 1, Qt.AlignRight)
        
        
        
        pass
    
    
    def discard_tempdata(self):
        self.discard_widget(self.cal)
        self.discard_widget(self.l1)
        self.discard_widget(self.l2)
        self.discard_widget(self.l3)
        self.discard_widget(self.minspinbox)
        self.discard_widget(self.hrspinbox)
        self.discard_widget(self.secspinbox)
        self.discard_widget(self.message)
        self.discard_widget(self.messageEdit)
        self.discard_widget(self.button_Discard)
        self.discard_widget(self.button_Save)
        
        self.button_del.setEnabled(True)
        self.button_add.setEnabled(True)
        self.grid.update()
    
    def save_tempdata(self):
        timeselected = QTime()
        timeselected.setHMS(self.hrspinbox.value(), self.minspinbox.value(), self.secspinbox.value())        
        selected= QDateTime()
        selected.setDate(self.cal.selectedDate())
        selected.setTime(timeselected)
        
        if(self.curindex.column()==1):
            self.model1.setData(self.adjacent, str(selected.toString()))
            self.model1.setData(self.curindex, self.messageEdit.toPlainText())
        elif(self.curindex.column()==0): 
            self.model1.setData(self.curindex, str(selected.toString()))
            self.model1.setData(self.adjacent, self.messageEdit.toPlainText())
        
        self.model1.submit()
        self.discard_tempdata()
        
    def discard_widget(self, widget):
        self.grid.removeWidget(widget)
        widget.deleteLater()
        widget = None
        
    def connect_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('events.sqlite3')
        
        if not db.open():
            QMessageBox.critical(None, qApp.tr("Cannot open database"),qApp.tr("Unable to establish a database connection.\n", QMessageBox.Cancel))
            return False

        
        query = QSqlQuery()
        if not query.exec_("SELECT * FROM EVENTDIARY"):
            query.exec_("create table EVENTDIARY (Date_time varchar(20) , Message varchar(140))")
        
        return db
        
    def display_contents(self,db):
        self.model1 = QSqlTableModel()
        self.model1.setTable('EVENTDIARY')
        self.model1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model1.select()
        self.model1.setHeaderData(0, Qt.Horizontal, "DATE-TIME")
        self.model1.setHeaderData(1, Qt.Horizontal, "MESSAGE")
        self.model1.sort(0, Qt.AscendingOrder)    
        
        
        self.view1= QTableView()
        self.view1.setModel(self.model1)        
        self.view1.setWindowTitle("Current Notes")
        self.view1.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        
    def insert_db(self):
        self.model1.insertRows(self.model1.rowCount(), 1)
        return True
    
    def del_row(self):
        indices = self.view1.selectionModel().selectedRows() 
        
        for index in sorted(indices):
            self.model1.removeRow(index.row())                
        
        #self.model1.layoutChanged.emit()
        self.model1.select()        
        #self.model1.submitAll() 