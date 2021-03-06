# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'charactersegmentationmainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1128, 676)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 201, 333))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.open_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.open_btn.setObjectName("open_btn")
        self.verticalLayout.addWidget(self.open_btn)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.grayscale_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.grayscale_btn.setObjectName("grayscale_btn")
        self.verticalLayout_3.addWidget(self.grayscale_btn)
        self.convert_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.convert_btn.setObjectName("convert_btn")
        self.verticalLayout_3.addWidget(self.convert_btn)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.binary_threshold_slider = QtWidgets.QSlider(self.verticalLayoutWidget)
        self.binary_threshold_slider.setMaximum(255)
        self.binary_threshold_slider.setProperty("value", 127)
        self.binary_threshold_slider.setOrientation(QtCore.Qt.Horizontal)
        self.binary_threshold_slider.setObjectName("binary_threshold_slider")
        self.horizontalLayout_3.addWidget(self.binary_threshold_slider)
        self.threshold_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.threshold_label.setObjectName("threshold_label")
        self.horizontalLayout_3.addWidget(self.threshold_label)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.thre_width_ledit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.thre_width_ledit.setObjectName("thre_width_ledit")
        self.horizontalLayout_2.addWidget(self.thre_width_ledit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.thre_dist_ledit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.thre_dist_ledit.setObjectName("thre_dist_ledit")
        self.horizontalLayout.addWidget(self.thre_dist_ledit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.segmentation_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.segmentation_btn.setObjectName("segmentation_btn")
        self.verticalLayout.addWidget(self.segmentation_btn)
        self.extract_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.extract_btn.setObjectName("extract_btn")
        self.verticalLayout.addWidget(self.extract_btn)
        self.exit_btn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.exit_btn.setObjectName("exit_btn")
        self.verticalLayout.addWidget(self.exit_btn)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(240, 10, 871, 611))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 869, 609))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.image_gview = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents)
        self.image_gview.setGeometry(QtCore.QRect(0, 0, 871, 611))
        self.image_gview.setObjectName("image_gview")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 350, 201, 271))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.characters_list = QtWidgets.QListView(self.verticalLayoutWidget_2)
        self.characters_list.setObjectName("characters_list")
        self.verticalLayout_2.addWidget(self.characters_list)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1128, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Chinese Calligraphy Segmentation Tool"))
        self.open_btn.setText(_translate("MainWindow", "Open"))
        self.grayscale_btn.setText(_translate("MainWindow", "Grayscale"))
        self.convert_btn.setText(_translate("MainWindow", "Convert"))
        self.threshold_label.setText(_translate("MainWindow", "127"))
        self.label_3.setText(_translate("MainWindow", "Threshold of \n"
"Width:"))
        self.label.setText(_translate("MainWindow", "Threshold of \n"
"Distance:"))
        self.segmentation_btn.setText(_translate("MainWindow", "Segmentation"))
        self.extract_btn.setText(_translate("MainWindow", "Extract"))
        self.exit_btn.setText(_translate("MainWindow", "Exit"))
        self.label_2.setText(_translate("MainWindow", "Characters:"))

