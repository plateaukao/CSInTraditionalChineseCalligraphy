# coding: utf-8
import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import copy
import os
import copy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom
import shutil

from single_char_radical_select_tool.single_char_radical_select_mainwindow import Ui_MainWindow
from utils.graphic_scene import GraphicsScene
from utils.polygon_extract import extractStorkeByPolygon


class SingleCharRadicalSelectApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SingleCharRadicalSelectApp, self).__init__()
        self.setupUi(self)

        self.file_path = ""
        self.file_name = ""
        self.parent_path = ""
        self.file_extension = ""

        self.char_qimg = None
        self.char_qimg_pix = None

        self.radical_qimg = None
        self.radical_qimg_pix = None

        self.char_img_gray = None

        self.extract_img_gray = None

        self.radical_save_path = ""


        self.open_pushButton.clicked.connect(self.handle_open_button)
        self.save_pushButton.clicked.connect(self.handle_save_button)
        self.clear_pushButton.clicked.connect(self.handle_clear_button)
        self.extract_pushButton.clicked.connect(self.handle_extract_button)

        self.char_scene = GraphicsScene()
        self.char_scene.setBackgroundBrush(Qt.gray)
        self.char_graphicsView.setScene(self.char_scene)

        self.radical_scene = QGraphicsScene()
        self.radical_scene.setBackgroundBrush(Qt.gray)
        self.radical_graphicsView.setScene(self.radical_scene)

    def handle_open_button(self):
        print("open clicked!")

        self.file_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath(), "*.png *.jpg *.jpeg")
        if not os.path.exists(self.file_path):
            print("not find image file")
            return

        self.file_name = self.file_path.split("/")[-1].split(".")[0]
        self.parent_path = os.path.abspath(os.path.join(self.file_path, os.pardir))
        _, self.file_extension = os.path.splitext(self.file_path)


        self.char_qimg = QImage(self.file_path)
        if self.char_qimg.isNull():
            QMessageBox.information(self, "image viewer", "can not load image")
            return

        self.char_img_gray = cv2.imread(self.file_path, 0)

        self.char_qimg_pix = QPixmap.fromImage(self.char_qimg)
        self.char_scene.addPixmap(self.char_qimg_pix)
        self.char_scene.addPixmap(self.char_qimg_pix)
        self.char_scene.setSceneRect(QRectF())
        self.char_graphicsView.fitInView(self.char_scene.sceneRect(), Qt.KeepAspectRatio)
        self.char_scene.update()
        self.statusbar.showMessage("Open image file successed!")

    def handle_extract_button(self):
        print("extract clicked")
        img_ = None
        if self.char_scene.points is None or len(self.char_scene.points) == 0:
            img_ = self.char_img_gray.copy()
        else:
            img_ = extractStorkeByPolygon(self.char_img_gray, self.char_scene.points)

        self.extract_img_gray = img_.copy()

        # create save path

        self.radical_save_path = os.path.join(self.parent_path, "{}_bs{}".format(self.file_name, self.file_extension))
        self.save_path_lineEdit.setText(self.radical_save_path)


        # update the extract result scene
        qimg_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.radical_scene.addPixmap(qimg_pix_)
        self.radical_scene.update()

        # clean char image
        self.char_scene.lastPoint = None
        self.char_scene.endPoint = None
        self.char_scene.points = []

        qimg_ = QImage(self.char_img_gray.data, self.char_img_gray.shape[1], self.char_img_gray.shape[0],
                        self.char_img_gray.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.char_scene.addPixmap(qimg_pix_)
        self.char_scene.update()


    def handle_save_button(self):
        print("save clicked")

        self.radical_save_path = self.save_path_lineEdit.text().strip()
        cv2.imwrite(self.radical_save_path, self.extract_img_gray)



    def handle_clear_button(self):
        print("clear clicked")
        self.char_scene.lastPoint = None
        self.char_scene.endPoint = None
        self.char_scene.points = []

        qimg_ = QImage(self.char_img_gray.data, self.char_img_gray.shape[1], self.char_img_gray.shape[0],
                       self.char_img_gray.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.char_scene.addPixmap(qimg_pix_)
        self.char_scene.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = SingleCharRadicalSelectApp()
    MainWindow.show()
    sys.exit(app.exec_())