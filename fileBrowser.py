#!/usr/bin/python3
from genericpath import isfile
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu, QMessageBox, QWidget,QApplication,QFileSystemModel,QTreeView,QLineEdit,QPushButton
from PyQt5.uic import loadUi
from PyQt5 import QtCore
import os
import sys


class MyFileBrowser(QWidget):
    def __init__(self):
        super(MyFileBrowser,self).__init__()
        loadUi("main.ui",self)
        self.dirPath = self.findChild(QLineEdit,"lineEdit")
        self.tree = self.findChild(QTreeView,"treeView")
        self.tree.doubleClicked.connect(self.open_file)
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.showcOontextMenu)
        self.getDirBtn = self.findChild(QPushButton,"pushButton")
        self.getDirBtn.clicked.connect(self.showTreeView)
        self.showTreeView()
    
    def showTreeView(self):
        try:
            if str(self.dirPath.text()) == "":
                QMessageBox.warning(self,"Error","Directory Path Can't be Blank")
            
            else:
                self.model = QFileSystemModel()
                self.model.setRootPath(self.dirPath.text())
                self.tree.setModel(self.model)
                self.tree.setRootIndex(self.model.index(self.dirPath.text()))
                self.tree.setColumnWidth(0, 250)
                self.tree.setAlternatingRowColors(True)
                self.tree.setSortingEnabled(True)
        
        except Exception as e:
            QMessageBox.warning(self,"Error",str(e))
        
    def showcOontextMenu(self):
        self.menu = QMenu()
        self.openFIle = self.menu.addAction("Open")
        self.openFIle.triggered.connect(self.open_file)
        self.deleteFile = self.menu.addAction("Delete")
        self.deleteFile.triggered.connect(self.delete_file)
        cursor = QCursor()
        self.menu.exec_(cursor.pos())

    
    def open_file(self):
        self.getPath()
        if os.path.isdir(self.file_path):
            self.dirPath.setText(self.file_path)
            self.showTreeView()
        
        if os.path.isfile(self.file_path):
            os.startfile(self.file_path)


    def delete_file(self):
        self.getPath()
        os.remove(self.file_path)
        self.dirPath.setText("/home/hacker")
        self.showTreeView()

    def getPath(self):
        self.index = self.tree.currentIndex()
        self.file_path = self.model.filePath(self.index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyFileBrowser()
    window.show()
    sys.exit(app.exec())