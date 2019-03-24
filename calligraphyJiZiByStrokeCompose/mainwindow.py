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
        MainWindow.resize(1226, 724)
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
        self.svg_extraction_pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.svg_extraction_pushButton.setObjectName("svg_extraction_pushButton")
        self.verticalLayout.addWidget(self.svg_extraction_pushButton)
        self.result_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.result_graphicsView.setGeometry(QtCore.QRect(300, 20, 361, 331))
        self.result_graphicsView.setObjectName("result_graphicsView")
        self.chars_listView = QtWidgets.QListView(self.centralwidget)
        self.chars_listView.setGeometry(QtCore.QRect(680, 20, 181, 331))
        self.chars_listView.setObjectName("chars_listView")
        self.stroke_graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.stroke_graphicsView.setGeometry(QtCore.QRect(380, 380, 281, 281))
        self.stroke_graphicsView.setObjectName("stroke_graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 420, 131, 16))
        self.label.setObjectName("label")
        self.stroke_info_label = QtWidgets.QLabel(self.centralwidget)
        self.stroke_info_label.setGeometry(QtCore.QRect(20, 450, 311, 111))
        self.stroke_info_label.setObjectName("stroke_info_label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(870, 20, 291, 641))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 289, 639))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.target_strokes_treeView = QtWidgets.QTreeView(self.scrollAreaWidgetContents)
        self.target_strokes_treeView.setGeometry(QtCore.QRect(0, 0, 291, 641))
        self.target_strokes_treeView.setObjectName("target_strokes_treeView")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1226, 22))
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
        self.svg_extraction_pushButton.setText(_translate("MainWindow", "SVG extraction"))
        self.label.setText(_translate("MainWindow", "Stroke Information:"))
        self.stroke_info_label.setText(_translate("MainWindow", "TextLabel"))

