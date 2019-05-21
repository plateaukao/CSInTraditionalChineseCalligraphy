# coding: utf-8
import math
import os
import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cdr_to_svg_by_batch.cdr_to_svg_mainwindow import Ui_MainWindow


class CdrToSVGByBatchApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CdrToSVGByBatchApp, self).__init__()
        self.setupUi(self)

        self.cdr_path = ""

        self.cdr_name_list = []

        self.save_path = ""

        self.open_pushButton.clicked.connect(self.handle_open_button)
        self.convert_pushButton.clicked.connect(self.handle_convert_button)

        self.cdr_listWidget.itemClicked.connect(self.handle_cdr_list_widget_click)

    def handle_open_button(self):
        print("open clicked")

        self.cdr_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.cdr_name_list = [f for f in os.listdir(self.cdr_path) if ".cdr" in f]
        if self.cdr_name_list is None or len(self.cdr_name_list) == 0:
            print("not cdr file found")
            return

        for i in range(len(self.cdr_name_list)):
            item = QListWidgetItem(self.cdr_name_list[i])
            self.cdr_listWidget.addItem(item)

    def handle_convert_button(self):
        print("convert clicked")

        # set the save path
        self.save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        # convert all cdr files
        for i in range(len(self.cdr_name_list)):
            cdr_path = os.path.join(self.cdr_path, self.cdr_name_list[i])
            svg_path = os.path.join(self.save_path, self.cdr_name_list[i].replace(".cdr", ".svg"))

            os.system("/Applications/Inkscape.app/Contents/Resources/bin/inkscape-bin -z -D --file={} " 
                      "--export-plain-svg={} --export-latex".format(cdr_path, svg_path))
            print("process {} successed!".format(i))



    def handle_cdr_list_widget_click(self, item):
        print("list item click")
        cdr_name = item.text().strip()
        svg_name = cdr_name.replace(".cdr", ".svg")

        cdr_path = os.path.join(self.cdr_path, cdr_name)
        svg_path = os.path.join(self.save_path, svg_name)

        if os.path.exists(cdr_path):
            self.cdr_webEngineView.load(QUrl.fromLocalFile(cdr_path))

        if os.path.exists(svg_path):
            self.svg_webEngineView.load(QUrl.fromLocalFile(svg_path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CdrToSVGByBatchApp()
    mainWindow.show()
    sys.exit(app.exec_())