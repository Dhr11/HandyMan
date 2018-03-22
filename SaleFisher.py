# -*- coding: utf-8 -*-


import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QWidget,QFileDialog, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QTableView, QCalendarWidget, QDoubleSpinBox, QLabel, QVBoxLayout, QHBoxLayout, QMdiSubWindow, QAction, QMdiArea, QScrollArea
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtCore import QCoreApplication, Qt, QDateTime, QTime, QDate, QRect
from sys import argv, exit
from functools import partial
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel,QSqlRecord

import sale_amazon_asst as Az_ast

from bs4 import BeautifulSoup
import requests

import common as cm


class sale_fisher_window(QMainWindow):
    count = 0
    
    def __init__(self,parent=None):
        super(sale_fisher_window, self).__init__(parent)
        self.setWindowTitle('Sale Fisher')
        self.setGeometry(100, 100, 840, 840)
        self.setWindowIcon(QIcon(os.path.join(cm.LOGO_DIR,'sale_fisher.png')))
        
        
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName( "centralwidget" )
        
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName( "verticalLayout" )
        
        
        self.mdiarea = QMdiArea(self.centralwidget)

#        self.setCentralWidget(self.mdiarea)
        self.mdiarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.mdiarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mdiarea.setActivationOrder(QMdiArea.CreationOrder)
        self.mdiarea.setObjectName('mdiArea')
        self.verticalLayout.addWidget(self.mdiarea)
        self.setCentralWidget(self.centralwidget)
        
        
        self.home()
        
    def home(self):
        
        exitAction = QAction(QIcon(os.path.join(cm.LOGO_DIR,'exit.png')), 'exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('leave the app')
        exitAction.triggered.connect(self.close_application)

        self.searchbox = QLineEdit()
        self.searchbox.setMaxLength(150)
        self.searchbox.setMaximumWidth(300)
        self.searchbox.setFont(QFont("Arial",11))
        self.searchbutton = QPushButton('Begin Search')
        self.searchbutton.clicked[bool].connect(self.begin_search)
        self.statusBar()
        self.toolBar = self.addToolBar('Extraction')
        self.toolBar.addAction(exitAction)
        self.toolBar.addWidget(self.searchbox)
        self.toolBar.addWidget(self.searchbutton)
        self.mdiarea.tileSubWindows()
        self.amazon_init()
        self.flipkart_init()
        
        self.show()
    
    def begin_search(self):
        word = str(self.searchbox.text())
        print(word)
        if word :   self.amazon_search(word)

    def amazon_init(self):
        self.Asubwindow = QMdiSubWindow()
        self.Asubwindow.setFixedSize(500,500)     
        self.Asubwindow.setWindowTitle("Amazon Listings")
        #widget = QWidget()
        self.mdiarea.addSubWindow(self.Asubwindow)
    
    def amazon_search(self, word):    
    
        Itemset = Az_ast.main_scraping(word) 
        print(len(Itemset)," items retreived")

        self.amazonwidget = QWidget()
        self.amazonwidget.setObjectName( "amazonwidget" )
        print("before 1 layout")
        self.AverticalLayout = QVBoxLayout(self.amazonwidget)
        self.AverticalLayout.setObjectName( "verticalLayout" )
        
        self.Ascrollarea = QScrollArea(self.amazonwidget)
        print("before 2nd layout")
        self.AverticalLayout.addWidget(self.Ascrollarea)        
        
        self.Ascrollareacontents = QWidget()
        self.Ascrollareacontents.setGeometry(QRect(100, 100, 512, 3712))
        
        self.Ascrollarea.setWidget(self.Ascrollareacontents)

        self.AverticalLayout = QVBoxLayout(self.Ascrollareacontents)
        self.Asubwindow.setWidget(self.amazonwidget)
        
        
        
        
        
        
        
        
        
        
        for i in Itemset:
            itemcontainer = QHBoxLayout()
            url = i.imagelink
            response = requests.get(url)
            image= QImage()
            image.loadFromData(response.content)
            ImgLbl = QLabel(self)
            pixmap = QPixmap(image)
            ImgLbl.setPixmap(pixmap.scaled(128,128))
            itemcontainer.addWidget(ImgLbl)
            textcontainer = QVBoxLayout()
            price2lbl = QLabel(''.join([u'\u0336{}'.format(c) for c in i.price2]))
            price1lbl = QLabel(i.price1)
            pricebox = QHBoxLayout()
            pricebox.addWidget(price1lbl)
            pricebox.addWidget(price2lbl)
            titlelbl = QLabel(i.title)
            ratingbox = QHBoxLayout()
            ratinglbl = QLabel(i.rating)
            reviewlbl = QLabel(i.reviewcount + " reviews")
            ratingbox.addWidget(ratinglbl)
            ratingbox.addWidget(reviewlbl)
            textcontainer.addLayout(pricebox)
            textcontainer.addWidget(titlelbl)
            textcontainer.addLayout(ratingbox)
            itemcontainer.addLayout(textcontainer)
            self.AverticalLayout.addLayout(itemcontainer)
         
        self.Asubwindow.show()
       

        
    def flipkart_init(self):
        subwindow = QMdiSubWindow()
        subwindow.setFixedSize(500,500)     
        subwindow.setWindowTitle("Flipkart Listings")
        self.mdiarea.addSubWindow(subwindow)
        subwindow.show()
   
    def connect_db(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('events.sqlite3')
        
        if not db.open():
            QMessageBox.critical(None, qApp.tr("Cannot open database"),qApp.tr("Unable to establish a database connection.\n", QMessageBox.Cancel))
            return False

        
        query = QSqlQuery()
        if not query.exec_("SELECT * FROM SALETABLE"):
            query.exec_("create table EVENTDIARY (Id varchar(20) , Item-Desc varchar(50)) ,Website varchar(10))")
        
        return db
    
    def close_application(self):
        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            #QCloseEvent.__init__(self)
            self.hide()
            #sys.exit(self)
        else:
            pass    
          