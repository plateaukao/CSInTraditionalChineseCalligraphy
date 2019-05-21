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

import xml.etree.ElementTree as ET

from utils.Functions import prettyXml

from svg_path_merge_extract_tool.svg_path_merge_extract_mainwindow import Ui_MainWindow


class SVGPathMergeExtractApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(SVGPathMergeExtractApp, self).__init__()
        self.setupUi(self)

        self.svg_path = ""
        self.svg_names = []

        self.select_svg_path = ""
        self.select_svg_paths_list = []

        self.paths_num = 0

        self.file_name = ""

        self.select_svg_files = []

        self.parent_path = ""

        self.merged_svg_names = []
        self.used_svg_names = []

        self.open_pushButton.clicked.connect(self.handle_open_button)
        self.merge_pushButton.clicked.connect(self.handle_merge_button)
        self.save_pushButton.clicked.connect(self.handle_save_button)

        self.svg_paths_listWidget.itemClicked.connect(self.handle_list_widget_item_click)

        self.svg_paths_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.parent_path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))

    def handle_open_button(self):
        print("open clicked!")

        self.svg_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if self.svg_path == "":
            print("svg path is none")
            return
        print(self.svg_path)
        # check svg path is a folder or svg file
        self.original_webEngineView.load(QUrl.fromLocalFile(self.svg_path))

        self.paths_num = self.extract_path(self.svg_path)

        for i in range(self.paths_num):
            item = QListWidgetItem("{}_path_{}.svg".format(self.file_name, i))
            self.svg_paths_listWidget.addItem(item)
            self.svg_names.append("{}_path_{}.svg".format(self.file_name, i))



    def handle_merge_button(self):
        print("merge clicked!")

        svg_files = []
        for i in range(len(self.svg_paths_listWidget.selectedItems())):
            svg_files.append(self.svg_paths_listWidget.selectedItems()[i].text().strip())

        print(svg_files)

        for sf in svg_files:
            self.used_svg_names.append(sf)

        # merge multiple svg files
        merged_file_name = self.merge_svg_files(svg_files)

        self.merged_svg_names.append(merged_file_name)

        merged_path = os.path.join(self.parent_path, "temp", merged_file_name)
        self.merged_webEngineView.load(QUrl.fromLocalFile(merged_path))


    def handle_save_button(self):
        print("save clicked!")

        save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        # copy single path
        for fn in self.svg_names:
            if fn not in self.used_svg_names:
                shutil.copy2(os.path.join(self.parent_path, "temp", fn), save_path)

        # copy merged path
        for fn in self.merged_svg_names:
            shutil.copy2(os.path.join(self.parent_path, "temp", fn), save_path)


        print(save_path)

    def handle_list_widget_item_click(self, item):
        print(item.text())
        select_svg_path = os.path.join(self.parent_path, "temp", item.text())
        print(select_svg_path)

        self.select_path_webEngineView.load(QUrl.fromLocalFile(select_svg_path))

    def merge_svg_files(self, svg_files):
        if svg_files is None or len(svg_files) == 0:
            return

        dom = minidom.parse(os.path.join(self.parent_path, "temp", svg_files[0]))

        path_elems = []

        for file in svg_files:
            dom_ = minidom.parse(os.path.join(self.parent_path, "temp", file))
            root_ = dom_.documentElement
            p_elems_ = root_.getElementsByTagName("path")

            for p_e in p_elems_:
               path_elems.append(p_e)

        dom, path_parent_elem = self.create_blank_svg(copy.deepcopy(dom))
        for i in range(len(path_elems)):
            path_parent_elem.appendChild(path_elems[i])

        data_xml = dom.toxml()
        with open(os.path.join(self.parent_path, "temp", "{}_merged_{}.svg".format(self.file_name, len(self.merged_svg_names))), "w") as f:
            f.write(data_xml)

        return "{}_merged_{}.svg".format(self.file_name, len(self.merged_svg_names))




    def create_blank_svg(self, dom):
        # create blank svg file by removing path element
        root = dom.documentElement

        path_elems = root.getElementsByTagName("path")
        if path_elems is None:
            print("not find path elements")
            return
        print("path elements len: ", len(path_elems))

        # path parent element
        path_parent_elem = None

        for e in path_elems:
            # find path parent element
            path_parent_elem = e.parentNode
            break

        for e in path_elems:
            path_parent_elem.removeChild(e)

        return dom, path_parent_elem

    def extract_path(self, svg_path):
        if svg_path == "":
            print("svg path is none")
            return

        # get svg file name
        self.file_name = svg_path.split("/")[-1].replace(".svg", "")
        save_path = "./temp"

        # open svg file
        dom = minidom.parse(svg_path)

        root = dom.documentElement
        path_elems = root.getElementsByTagName("path")
        if path_elems is None or len(path_elems) == 0:
            print("not find path elements in svg file")
            return
        print("path elems num: ", len(path_elems))
        for i in range(len(path_elems)):
            dom_, path_parent_elem = self.create_blank_svg(copy.deepcopy(dom))
            path_parent_elem.appendChild(path_elems[i])

            data_xml = dom_.toxml()

            with open(os.path.join(save_path, ("%s_path_%d.svg" % (self.file_name, i))), 'w') as f:
                f.write(data_xml)

        return len(path_elems)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = SVGPathMergeExtractApp()
    MainWindow.show()
    sys.exit(app.exec_())