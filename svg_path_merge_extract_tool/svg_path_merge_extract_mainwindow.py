# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'svg_path_merge_extract_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1149, 1003)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(40, 60, 211, 461))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 209, 459))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.svg_paths_listWidget = QtWidgets.QListWidget(self.scrollAreaWidgetContents_2)
        self.svg_paths_listWidget.setGeometry(QtCore.QRect(0, 0, 211, 461))
        self.svg_paths_listWidget.setObjectName("svg_paths_listWidget")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.merge_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.merge_pushButton.setGeometry(QtCore.QRect(810, 470, 211, 32))
        self.merge_pushButton.setObjectName("merge_pushButton")
        self.save_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.save_pushButton.setGeometry(QtCore.QRect(40, 540, 211, 32))
        self.save_pushButton.setObjectName("save_pushButton")
        self.original_webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.original_webEngineView.setGeometry(QtCore.QRect(280, 20, 400, 400))
        self.original_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.original_webEngineView.setObjectName("original_webEngineView")
        self.merged_webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.merged_webEngineView.setGeometry(QtCore.QRect(710, 20, 400, 400))
        self.merged_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.merged_webEngineView.setObjectName("merged_webEngineView")
        self.open_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.open_pushButton.setGeometry(QtCore.QRect(40, 20, 211, 32))
        self.open_pushButton.setObjectName("open_pushButton")
        self.select_path_webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.select_path_webEngineView.setGeometry(QtCore.QRect(280, 470, 400, 400))
        self.select_path_webEngineView.setUrl(QtCore.QUrl("about:blank"))
        self.select_path_webEngineView.setObjectName("select_path_webEngineView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(420, 430, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(430, 880, 111, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(880, 430, 101, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1149, 22))
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
        self.merge_pushButton.setText(_translate("MainWindow", "Merge"))
        self.save_pushButton.setText(_translate("MainWindow", "Save"))
        self.open_pushButton.setText(_translate("MainWindow", "Open"))
        self.label.setText(_translate("MainWindow", "Original SVG File"))
        self.label_2.setText(_translate("MainWindow", "Selected Path"))
        self.label_3.setText(_translate("MainWindow", "Merged Result"))

from PyQt5 import QtWebEngineWidgets
