import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from mainwindow import Ui_MainWindow

from utils.Utils import get_file_names
from utils.Templates import create_doufang_template


class CalligraphyCollectionToolGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CalligraphyCollectionToolGUI, self).__init__()
        self.setupUi(self)

        self.dataset_path = ""
        self.images_path = ""

        self.char_image_path = []
        self.text_content = ""
        self.font = "kai"
        self.template = "斗方"

        self.text_images = []

        self.text_images_resized = []

        self.calli_scene = QGraphicsScene()
        self.calli_scene.setBackgroundBrush(Qt.gray)
        self.image_gw.setScene(self.calli_scene)


        self.generate_btn.clicked.connect(self.calligraphy_generate)
        self.set_dataset_path_btn.clicked.connect(self.set_dataset_path)
        self.font_comboBox.currentIndexChanged.connect(self.font_combobox_selectionchange)
        self.template_comboBox.currentIndexChanged.connect(self.template_combobox_selectionchange)

    def font_combobox_selectionchange(self):
        """
        Select font
        :return:
        """
        font = self.font_comboBox.currentText()

        if font == "楷体":
            self.font = "kai"
        elif font == "宋体":
            self.font = "song"
        elif font == "启功体":
            self.font = "qigong"

        if not os.path.exists(os.path.join(self.dataset_path, self.font)):
            print(os.path.join(self.dataset_path, self.font), " is not exist!")

        print("Set font: ", self.font)
        self.images_path = os.path.join(self.dataset_path, self.font)

    def template_combobox_selectionchange(self):
        """
        Select templates
        :return:
        """
        self.template = self.template_comboBox.currentText()
        print("Set template: ", self.template)

    def set_dataset_path(self):
        """
        Set dataset path
        :return:
        """
        path = QFileDialog.getExistingDirectory(None, "Get dataset path", QDir.currentPath())
        print("Set dataset path:", path)
        self.dataset_path = path

    def calligraphy_generate(self):
        """
        Generate calligraphy based on the text contents, templates, word space and column space.
        :return:
        """
        self.calli_scene.clear()
        self.statusbar.showMessage("Generate begin......")

        text_content = self.text_content_edit.toPlainText()

        if text_content is None or text_content == "":
            self.statusbar.showMessage("Text contents should not be null!")
            return

        # process text contents
        text_content = text_content.replace("\n", "")
        self.text_content = text_content
        print("text content len:", len(self.text_content))

        # get all character images name in images path
        self.images_path = get_file_names(self.text_content, self.dataset_path, self.font)
        if self.images_path == []:
            print("not find images path!")
            return
        print("image path len:", len(self.images_path))
        print(self.images_path)

        # load images
        self.text_images = []
        for img_path in self.images_path:
            img_ = cv2.imread(img_path, 0)
            self.text_images.append(img_)
        print("text_images len:", len(self.text_images))

        # generate new calligraphy image
        word_space = self.word_space_slider.value()
        column_space = self.column_space_slider.value()

        if self.num_per_colu_lineEdit.text():
            num_per_column = int(self.num_per_colu_lineEdit.text())
        else:
            num_per_column = 5

        # select template
        calli_img = None
        if self.template == "斗方":
            calli_img = create_doufang_template(self.text_images, word_space, column_space, num_per_column=num_per_column)

        if calli_img is None:
            print("Create calligraphy iamge failed!")
            return
        calli_img = np.array(calli_img, dtype=np.uint8)

        cv2.imwrite("calli_img.png", calli_img)

        qimg = QImage(calli_img.data, calli_img.shape[1], calli_img.shape[0], calli_img.shape[1], QImage.Format_Indexed8)
        qpix = QPixmap.fromImage(qimg)

        self.calli_scene.addPixmap(qpix)
        self.calli_scene.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = CalligraphyCollectionToolGUI()
    mainwindow.show()
    sys.exit(app.exec_())
