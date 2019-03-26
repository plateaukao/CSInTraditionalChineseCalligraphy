# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1391, 945)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_btn.setGeometry(QtCore.QRect(20, 10, 191, 32))
        self.open_btn.setObjectName("open_btn")
        self.images_listView = QtWidgets.QListView(self.centralwidget)
        self.images_listView.setGeometry(QtCore.QRect(20, 80, 191, 801))
        self.images_listView.setObjectName("images_listView")
        self.char_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.char_graphicsView.setGeometry(QtCore.QRect(230, 80, 601, 601))
        self.char_graphicsView.setObjectName("char_graphicsView")
        self.result_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.result_graphicsView.setGeometry(QtCore.QRect(850, 80, 381, 381))
        self.result_graphicsView.setObjectName("result_graphicsView")
        self.name_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.name_lineEdit.setGeometry(QtCore.QRect(900, 480, 331, 31))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setGeometry(QtCore.QRect(1080, 530, 151, 41))
        self.save_btn.setObjectName("save_btn")
        self.extract_btn = QtWidgets.QPushButton(self.centralwidget)
        self.extract_btn.setGeometry(QtCore.QRect(710, 700, 114, 32))
        self.extract_btn.setObjectName("extract_btn")
        self.clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_btn.setGeometry(QtCore.QRect(290, 700, 114, 32))
        self.clear_btn.setObjectName("clear_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1391, 22))
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
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.save_btn.setText(_translate("MainWindow", "Save"))
        self.extract_btn.setText(_translate("MainWindow", "Extract"))
        self.clear_btn.setText(_translate("MainWindow", "Clear"))

