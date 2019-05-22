import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from character_synthesis_tool.character_synthesis_mainwindow import Ui_MainWindow

class CharacterSynthesisGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CharacterSynthesisGUI, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        MainWindow = CharacterSynthesisGUI()
        MainWindow.show()
        sys.exit(app.exec_())