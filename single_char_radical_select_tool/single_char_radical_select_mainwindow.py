# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'single_char_radical_select_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1352, 825)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.open_pushButton.setGeometry(QtCore.QRect(10, 10, 114, 32))
        self.open_pushButton.setObjectName("open_pushButton")
        self.char_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.char_graphicsView.setGeometry(QtCore.QRect(20, 50, 700, 700))
        self.char_graphicsView.setObjectName("char_graphicsView")
        self.radical_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.radical_graphicsView.setGeometry(QtCore.QRect(740, 50, 600, 600))
        self.radical_graphicsView.setObjectName("radical_graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(740, 680, 81, 16))
        self.label.setObjectName("label")
        self.save_path_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.save_path_lineEdit.setGeometry(QtCore.QRect(810, 680, 521, 21))
        self.save_path_lineEdit.setObjectName("save_path_lineEdit")
        self.save_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.save_pushButton.setGeometry(QtCore.QRect(1220, 720, 114, 32))
        self.save_pushButton.setObjectName("save_pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(290, 30, 101, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(990, 30, 71, 16))
        self.label_3.setObjectName("label_3")
        self.clear_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.clear_pushButton.setGeometry(QtCore.QRect(950, 720, 114, 32))
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.extract_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.extract_pushButton.setGeometry(QtCore.QRect(750, 720, 114, 32))
        self.extract_pushButton.setObjectName("extract_pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1352, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_pushButton.setText(_translate("MainWindow", "Open"))
        self.label.setText(_translate("MainWindow", "Save Path:"))
        self.save_pushButton.setText(_translate("MainWindow", "Save"))
        self.label_2.setText(_translate("MainWindow", "Original Image"))
        self.label_3.setText(_translate("MainWindow", "Radicals"))
        self.clear_pushButton.setText(_translate("MainWindow", "Clear"))
        self.extract_pushButton.setText(_translate("MainWindow", "Extract"))

