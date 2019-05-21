# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cdr_to_svg_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1085, 696)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.open_pushButton.setGeometry(QtCore.QRect(10, 10, 114, 32))
        self.open_pushButton.setObjectName("open_pushButton")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 50, 201, 551))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 199, 549))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.cdr_listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.cdr_listWidget.setGeometry(QtCore.QRect(0, 0, 201, 551))
        self.cdr_listWidget.setObjectName("cdr_listWidget")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.convert_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.convert_pushButton.setGeometry(QtCore.QRect(50, 610, 114, 32))
        self.convert_pushButton.setObjectName("convert_pushButton")
        self.cdr_webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.cdr_webEngineView.setGeometry(QtCore.QRect(240, 50, 400, 400))
        self.cdr_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.cdr_webEngineView.setObjectName("cdr_webEngineView")
        self.svg_webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.svg_webEngineView.setGeometry(QtCore.QRect(670, 50, 400, 400))
        self.svg_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.svg_webEngineView.setObjectName("svg_webEngineView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 460, 59, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(840, 460, 59, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1085, 22))
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
        self.convert_pushButton.setText(_translate("MainWindow", "Convert"))
        self.label.setText(_translate("MainWindow", "CDR"))
        self.label_2.setText(_translate("MainWindow", "SVG"))

from PyQt5 import QtWebEngineWidgets
