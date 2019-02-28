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
        MainWindow.resize(883, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 221, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.set_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.set_pushButton.setObjectName("set_pushButton")
        self.verticalLayout.addWidget(self.set_pushButton)
        self.input_textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.input_textEdit.setObjectName("input_textEdit")
        self.verticalLayout.addWidget(self.input_textEdit)
        self.generate_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.generate_pushButton.setObjectName("generate_pushButton")
        self.verticalLayout.addWidget(self.generate_pushButton)
        self.result_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.result_graphicsView.setGeometry(QtCore.QRect(300, 20, 361, 331))
        self.result_graphicsView.setObjectName("result_graphicsView")
        self.chars_listView = QtWidgets.QListView(self.centralwidget)
        self.chars_listView.setGeometry(QtCore.QRect(680, 20, 181, 331))
        self.chars_listView.setObjectName("chars_listView")
        self.stroke_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.stroke_graphicsView.setGeometry(QtCore.QRect(380, 380, 281, 281))
        self.stroke_graphicsView.setObjectName("stroke_graphicsView")
        self.strokes_listView = QtWidgets.QListView(self.centralwidget)
        self.strokes_listView.setGeometry(QtCore.QRect(680, 381, 181, 281))
        self.strokes_listView.setObjectName("strokes_listView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 420, 131, 16))
        self.label.setObjectName("label")
        self.stroke_info_label = QtWidgets.QLabel(self.centralwidget)
        self.stroke_info_label.setGeometry(QtCore.QRect(20, 450, 311, 111))
        self.stroke_info_label.setObjectName("stroke_info_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 883, 22))
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
        self.set_pushButton.setText(_translate("MainWindow", "Stroke Library Setting"))
        self.generate_pushButton.setText(_translate("MainWindow", "Generate"))
        self.label.setText(_translate("MainWindow", "Stroke Information:"))
        self.stroke_info_label.setText(_translate("MainWindow", "TextLabel"))

