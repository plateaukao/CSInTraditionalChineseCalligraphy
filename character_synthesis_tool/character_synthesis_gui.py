import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import xml.etree.ElementTree as ET

from character_synthesis_tool.character_synthesis_mainwindow import Ui_MainWindow
from character_synthesis_tool.generate_template_folders import generate_template_folders
from character_synthesis_tool.character_synthesis import character_synthesis

class CharacterSynthesisGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CharacterSynthesisGUI, self).__init__()
        self.setupUi(self)

        self.xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position_add_stroke_order.xml"
        self.xml_tree = None
        self.xml_root = None

        if self.xml_path != "":
            self.xml_tree = ET.parse(self.xml_path)
            self.xml_root = self.xml_tree.getroot()

        self.template_chars_path = ""
        self.template_chars = []

        self.template_images_save_path = "../../../Data/Calligraphy_database/Chars_tempalte_library"

        self.stroke_image_path = "../../../Data/Calligraphy_database/Stroke_pngs"

        self.input_chars = ""

        self.generated_results_images = []

        self.grayscale_scene = QGraphicsScene()
        self.grayscale_scene.setBackgroundBrush(Qt.gray)
        self.grayscale_graphicsView.setScene(self.grayscale_scene)
        self.grayscale_scene.setSceneRect(QRectF())
        self.grayscale_graphicsView.fitInView(self.grayscale_scene.sceneRect(), Qt.KeepAspectRatio)

        self.open_xml_pushButton.clicked.connect(self.handle_load_xml_button)
        self.open_chars_pushButton.clicked.connect(self.handle_load_tempalte_chars_button)
        self.tempate_generate_pushButton.clicked.connect(self.handle_generate_template_button)
        self.synthesis_pushButton.clicked.connect(self.handle_synthesis_button)
        self.generated_results_listWidget.itemClicked.connect(self.handle_generated_listwidget_item_click)

    def handle_load_xml_button(self):
        print("load xml clicked")
        self.xml_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if self.xml_path != "":
            print(self.xml_path)

        if not os.path.exists(self.xml_path):
            print("Xml not existed!")
            return


        # parse xml data
        self.xml_tree = ET.parse(self.xml_path)
        if self.xml_tree is None:
            print("xml tree is none!")
            return
        self.xml_root = self.xml_tree.getroot()
        if self.xml_root is None:
            print("xml root is none")
            return

    def handle_load_tempalte_chars_button(self):
        print("load template chars clicked")

        # clean cache
        self.template_chars = []

        self.template_chars_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if not os.path.exists(self.template_chars_path):
            print("template chars not existed!")
            return

        with open(self.template_chars_path, "r") as f:
            for ch in f.readlines():
                self.template_chars.append(ch.strip())

        # show in gui
        self.temp_chars_plainTextEdit.setPlainText(str(self.template_chars))

    def handle_generate_template_button(self):
        print("generate template clicked")
        if self.template_chars is None or len(self.template_chars) == 0:
            print("template chars is none")
            return
        # get template save path
        self.template_images_save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.template_images_save_path == "":
            print("template images save path is none")
            return

        generate_template_folders(self.template_chars, self.xml_path, self.stroke_image_path, self.template_images_save_path)

        print("template generation successed!")

    def handle_synthesis_button(self):
        print("synthesis button clicked")

        # clean cache
        self.generated_results_listWidget.clear()

        self.input_chars = self.input_plainTextEdit.toPlainText().strip()
        print(self.input_chars)

        self.generated_results_images = character_synthesis(self.input_chars, self.xml_root, self.template_images_save_path, self.stroke_image_path)

        if self.generated_results_images is None or len(self.generated_results_images) == 0:
            print("generated failed")
            return

        for img_id in range(len(self.generated_results_images)):
            item = QListWidgetItem("{}.png".format(self.input_chars[img_id]))
            self.generated_results_listWidget.addItem(item)

    def handle_generated_listwidget_item_click(self, item):
        print(self.generated_results_listWidget.currentRow())

        if len(self.generated_results_images) == 0:
            print("not generated results")
            return
        img_id = self.generated_results_listWidget.currentRow()
        img = self.generated_results_images[img_id].copy()

        qimg = QImage(img.data, img.shape[1], img.shape[0], img.shape[1], QImage.Format_Indexed8)
        qimg_pix = QPixmap.fromImage(qimg)

        self.grayscale_scene.addPixmap(qimg_pix)
        self.grayscale_scene.update()

if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        MainWindow = CharacterSynthesisGUI()
        MainWindow.show()
        sys.exit(app.exec_())