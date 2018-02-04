# -*- coding: utf-8 -*-
import sys,os
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QAction, QMessageBox, QCheckBox, QProgressBar, QComboBox, QLabel, QStyleFactory 
from PyQt5.uic.properties import QtGui
from PyQt5.QtWidgets import QFontDialog, QColorDialog, QCalendarWidget, QTextEdit, QFileDialog
from ui_editor import Editwindow
import common as cm

class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 500, 100)
        self.setWindowTitle('Handyman')
        self.setWindowIcon(QIcon('logo.png'))
        

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        #fileMenu.addAction(exitAction)
        
        exitAction = QAction(QIcon(os.path.join(cm.LOGO_DIR,'exit.png')), 'exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('leave the app')
        exitAction.triggered.connect(self.close_application)

        editorAction = QAction(QIcon(os.path.join(cm.LOGO_DIR,'editor_logo.png')), 'exit', self)
        editorAction.setShortcut('Ctrl+E')
        editorAction.setStatusTip('Open Editor')
        editorAction.triggered.connect(self.editopen)
        

        self.toolBar = self.addToolBar('Extraction')
        self.toolBar.addAction(exitAction)
        self.toolBar.addAction(editorAction)

        self.show() 
       
    def editopen(self):
        editor= Editwindow(self)
            
    def close_application(self):
        choice = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass    

if __name__ == "__main__":
    def run():
        app = QApplication(sys.argv)
        Gui = window()
        sys.exit(app.exec_())

run()