# coding: utf-8
import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from calligraphyJiZiByStrokeCompose.mainwindow import Ui_MainWindow


class CalligraphyJiZiByStrokeCompse(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CalligraphyJiZiByStrokeCompse, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CalligraphyJiZiByStrokeCompse()
    mainWindow.show()
    sys.exit(app.exec_())

