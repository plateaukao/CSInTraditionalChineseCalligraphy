# coding: utf-8
import sys
import math
import cv2
import os
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image
from xml.dom import minidom

from char_radicals_split_tool.mainwindow import Ui_MainWindow


class CharRadicalsSplitByBasicRadicals(QMainWindow, Ui_MainWindow):

    __label = "basic radicals"
    __image_path = ""

    __image_name_list = []

    __char_image = None

    __extracted_image = None

    def __init__(self):
        super(CharRadicalsSplitByBasicRadicals, self).__init__()
        self.setupUi(self)

        self.image_names_slm = QStringListModel()
        self.image_names_slm.setStringList(self.__image_name_list)
        self.images_listView.setModel(self.image_names_slm)
        self.images_listView.clicked.connect(self.handle_image_list_item_clicked)

        self.char_scene = GraphicsScene()
        self.char_scene.setBackgroundBrush(Qt.gray)
        self.char_graphicsView.setScene(self.char_scene)

        self.result_scene = QGraphicsScene()
        self.result_scene.setBackgroundBrush(Qt.gray)
        self.result_graphicsView.setScene(self.result_scene)

        self.open_btn.clicked.connect(self.handle_open_button_clicked)
        self.extract_btn.clicked.connect(self.handle_extract_btn_clicked)
        self.save_btn.clicked.connect(self.handle_save_btn_clicked)

    def handle_open_button_clicked(self):
        self.__image_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        file_names = [f for f in os.listdir(self.__image_path) if "." not in f]

        for fn in file_names:
            names_ = [f for f in os.listdir(os.path.join(self.__image_path, fn)) if ".png" in f]
            if len(names_) == 0:
                print("No char image found in {}!".format(os.path.join(self.__image_path, fn)))
            self.__image_name_list.append(names_[0])

        self.image_names_slm.setStringList(self.__image_name_list)

    def handle_image_list_item_clicked(self, qModelIndex):
        index = qModelIndex.row()

        image_path = os.path.join(self.__image_path, self.__image_name_list[index].split("_")[0], self.__image_name_list[index])
        # image_name = self.__image_name_list[index]

        img_ = cv2.imread(image_path, 0)
        self.__char_image = img_.copy()

        qimg_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)

        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.char_scene.addPixmap(qimg_pix_)
        self.char_scene.update()

        self.name_lineEdit.setText(self.__image_name_list[index])

    def handle_extract_btn_clicked(self):

        # extracted image
        img_ = None
        if self.char_scene.points is None or len(self.char_scene.points) == 0:
            img_ = self.__char_image.copy()
        else:
            img_ = extractStorkeByPolygon(self.__char_image, self.char_scene.points)

        self.__extracted_image = img_.copy()

        # update the extracted scene
        qimg_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.result_scene.addPixmap(qimg_pix_)
        self.result_scene.update()

        self.char_scene.lastPoint = None
        self.char_scene.endPoint = None
        self.char_scene.points = []

        qimg_ = QImage(self.__char_image.data, self.__char_image.shape[1], self.__char_image.shape[0],
                       self.__char_image.shape[1], QImage.Format_Indexed8)

        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.char_scene.addPixmap(qimg_pix_)
        self.char_scene.update()

    def handle_save_btn_clicked(self):
        img_name = self.name_lineEdit.text()
        img_path = os.path.join(self.__image_path, img_name.split("_")[0], self.__label, img_name)

        cv2.imwrite(img_path, self.__extracted_image)

        self.statusbar.showMessage("Save successed!")


class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)

        self.lastPoint = None
        self.endPoint = None

        self.points = []
        self.strokes = []
        self.T_DISTANCE = 10

    def setOption(self, opt):
        self.opt = opt


    def mousePressEvent(self, event):
        """
            Mouse press clicked!
        :param event:
        :return:
        """
        pen = QPen(Qt.red)
        brush = QBrush(Qt.red)
        x = event.scenePos().x()
        y = event.scenePos().y()

        if len(self.points) == 0:
            self.addEllipse(x, y, 2, 2, pen, brush)
            self.endPoint = event.scenePos()
        else:
            x0 = self.points[0][0]
            y0 = self.points[0][1]

            dist = math.sqrt((x - x0) * (x - x0) + (y - y0) * (y - y0))
            if dist < self.T_DISTANCE:
                # end and close point
                pen_ = QPen(Qt.green)
                brush_ = QBrush(Qt.green)
                self.addEllipse(x0, y0, 2, 2, pen_, brush_)
                self.endPoint = event.scenePos()
                x = x0
                y = y0
            else:
                self.addEllipse(x, y, 4, 4, pen, brush)
                self.endPoint = event.scenePos()
        self.points.append((x, y))


    def mouseReleaseEvent(self, event):
        """
            Mouse release event!
        :param event:
        :return:
        """
        pen = QPen(Qt.red)

        if self.lastPoint is not None and self.lastPoint is not None:
            self.addLine(self.endPoint.x(), self.endPoint.y(), self.lastPoint.x(), self.lastPoint.y(), pen)

        self.lastPoint = self.endPoint


def extractStorkeByPolygon(image, polygon):

    image_ = image.copy()

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if not ray_tracing_method(x, y, polygon):
                image_[y][x] = 255

    return image_


# Ray tracing check point in polygon
def ray_tracing_method(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CharRadicalsSplitByBasicRadicals()
    mainWindow.show()
    sys.exit(app.exec_())