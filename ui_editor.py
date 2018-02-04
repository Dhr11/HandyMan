# -*- coding: utf-8 -*-
import sys,os
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory 
from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QFontDialog, QColorDialog, QCalendarWidget, QTextEdit, QFileDialog

import common as cm
#ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
#LOGO_DIR = os.path.join(ROOT_DIR, 'images')

class Editwindow(QMainWindow):

    def __init__(self,parent=None):
        super(Editwindow, self).__init__(parent)
        self.setGeometry(700, 50, 700, 700)
        self.setWindowTitle('Scratchpad')
        
        
        self.statusBar()
        newFile = QAction(QIcon(os.path.join(cm.LOGO_DIR,'newfile_logo.png')), 'exit', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('Ctrl+N || Open File')
        newFile.triggered.connect(self.new_file)
        
        openFile = QAction(QIcon(os.path.join(cm.LOGO_DIR,'openfile_logo.png')), 'exit', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Ctrl+O || Open File')
        openFile.triggered.connect(self.file_open)
        
        saveFile = QAction(QIcon(os.path.join(cm.LOGO_DIR,'savefile_logo.png')), 'exit', self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Ctrl+S || Save File')
        saveFile.triggered.connect(self.file_save)
        
        exitAction = QAction(QIcon(os.path.join(cm.LOGO_DIR,'exit.png')), 'exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('leave the app')
        exitAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar('Extraction')
        self.toolBar.addAction(newFile)
        self.toolBar.addAction(openFile)
        self.toolBar.addAction(saveFile)
        self.toolBar.addAction(exitAction)
        

        self.show()
        
        
    def file_save(self):
        name, _ = QFileDialog.getSaveFileName(self,'Save File', options=QFileDialog.DontUseNativeDialog)
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
    def editor(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.move(50,150)    
        self.resize(500,500)    
    
    def new_file(self):
        self.editor()
        
        
    def file_open(self):
        # need to make name an tupple otherwise i had an error and app crashed
        name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)
        file = open(name, 'r')
        self.editor()
        
        with file:
            text = file.read()
            self.textEdit.setText(text)
    
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
        