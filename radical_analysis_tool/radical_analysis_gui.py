import os
import sys

import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from radical_analysis_tool.radical_analysis_mainwindow import Ui_MainWindow
from utils.Functions import creatBlankRGBImageWithSize, rgb2qimage, get_3_point_water_radical_img, drawline


class RadicalAnalysisGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RadicalAnalysisGUI, self).__init__()
        self.setupUi(self)

        self.open_pushButton.clicked.connect(self.handle_open_button)
        self.analyze_pushButton.clicked.connect(self.handle_analyze_button)
        self.a_listWidget.itemClicked.connect(self.handle_a_list_widgt_item_click)
        self.b_listWidget.itemClicked.connect(self.handle_b_list_widgt_item_click)

        self.merged_scene = QGraphicsScene()
        self.merged_scene.setBackgroundBrush(Qt.gray)
        self.merged_graphicsView.setScene(self.merged_scene)
        self.merged_scene.setSceneRect(QRectF())
        self.merged_graphicsView.fitInView(self.merged_scene.sceneRect(), Qt.KeepAspectRatio)

        self.a_scene = QGraphicsScene()
        self.a_scene.setBackgroundBrush(Qt.gray)
        self.a_graphicsView.setScene(self.a_scene)
        self.a_scene.setSceneRect(QRectF())
        self.a_graphicsView.fitInView(self.a_scene.sceneRect(), Qt.KeepAspectRatio)

        self.b_scene = QGraphicsScene()
        self.b_scene.setBackgroundBrush(Qt.gray)
        self.b_graphicsView.setScene(self.b_scene)
        self.b_scene.setSceneRect(QRectF())
        self.b_graphicsView.fitInView(self.b_scene.sceneRect(), Qt.KeepAspectRatio)


        self.image_path = ""

        self.a_image = None
        self.b_image = None


    def handle_open_button(self):
        print("open clicked")
        self.image_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        image_names = [f for f in os.listdir(self.image_path) if ".png" in f or ".jpg" in f or ".jpeg" in f]
        for i in range(len(image_names)):
            item_a = QListWidgetItem(image_names[i])
            self.a_listWidget.addItem(item_a)
            item_b = QListWidgetItem(image_names[i])
            self.b_listWidget.addItem(item_b)

    def handle_analyze_button(self):
        print("analyze clicked")

        if self.a_image is None or self.b_image is None:
            print("a image or b image is none")
            return

        a_radical = get_3_point_water_radical_img(self.a_image)
        b_radical = get_3_point_water_radical_img(self.b_image)

        if a_radical is None or b_radical is None:
            print("a or b radical is none")
            return

        bk_rgb = creatBlankRGBImageWithSize(self.a_image.shape)

        # draw mizi grid
        drawline(bk_rgb, (0,0), (bk_rgb.shape[0]-1, bk_rgb.shape[1]-1), (0, 0, 255), 1, gap=4)
        drawline(bk_rgb, (0, bk_rgb.shape[1] - 1), (bk_rgb.shape[0] - 1, 0), (0, 0, 255), 1, gap=4)
        drawline(bk_rgb, (0, int(bk_rgb.shape[1]/2)), (bk_rgb.shape[0]-1, int(bk_rgb.shape[1]/2)), (0, 0, 255), 1, gap=4)
        drawline(bk_rgb, (int(bk_rgb.shape[0]/2), 0), (int(bk_rgb.shape[0]/2), bk_rgb.shape[1] - 1), (0, 0, 255), 1, gap=4)


        for x in range(self.a_image.shape[0]):
            for y in range(self.a_image.shape[1]):
                if a_radical[x][y] == 0 and b_radical[x][y] == 0:
                    bk_rgb[x][y] = (0, 0, 0)    # black
                if a_radical[x][y] == 0 and b_radical[x][y] != 0:
                    bk_rgb[x][y] = (0, 0, 255)  # red
                if a_radical[x][y] != 0 and b_radical[x][y] == 0:
                    bk_rgb[x][y] = (0, 255, 0)  # green

        qimg = rgb2qimage(bk_rgb)
        qimg_pix = QPixmap.fromImage(qimg)

        self.merged_scene.addPixmap(qimg_pix)
        self.merged_scene.setSceneRect(QRectF())
        self.merged_graphicsView.fitInView(self.merged_scene.sceneRect(), Qt.KeepAspectRatio)
        self.merged_scene.update()

    def handle_a_list_widgt_item_click(self, item):
        print("item b clicked")
        img_name = item.text().strip()
        img_path = os.path.join(self.image_path, img_name)
        if not os.path.exists(img_path):
            print("not a image found!")
            return

        self.a_image = cv2.imread(img_path, 0)

        a_qimg = QImage(img_path)
        a_qimg_pix = QPixmap.fromImage(a_qimg)
        # self.a_scene.addPixmap(a_qimg_pix)
        self.a_scene.addPixmap(a_qimg_pix)
        self.a_scene.setSceneRect(QRectF())
        self.a_graphicsView.fitInView(self.a_scene.sceneRect(), Qt.KeepAspectRatio)
        self.a_scene.update()

    def handle_b_list_widgt_item_click(self, item):
        print("item b clicked")
        img_name = item.text().strip()
        img_path = os.path.join(self.image_path, img_name)
        if not os.path.exists(img_path):
            print("not a image found!")
            return

        self.b_image = cv2.imread(img_path, 0)

        b_qimg = QImage(img_path)
        b_qimg_pix = QPixmap.fromImage(b_qimg)
        # self.b_scene.addPixmap(b_qimg_pix)
        self.b_scene.addPixmap(b_qimg_pix)
        self.b_scene.setSceneRect(QRectF())
        self.b_graphicsView.fitInView(self.b_scene.sceneRect(), Qt.KeepAspectRatio)
        self.b_scene.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = RadicalAnalysisGUI()
    MainWindow.show()
    sys.exit(app.exec_())





    # img_path = "./temp/瀛.png"
    #
    # threshold = 1. / 4
    #
    # img = cv2.imread(img_path, 0)
    #
    # bk = get_3_point_water_radical_img(img)
    #
    # # rects = getAllMiniBoundingBoxesOfImage(img)
    # # print(len(rects))
    #
    # # cv2.line(img, (int(threshold*img.shape[0]), 0), (int(threshold*img.shape[0]), img.shape[1]), 0, 2 )
    # #
    # # for rect in rects:
    # #     cent_x = rect[0] + int(rect[2] / 2)
    # #
    # #     if cent_x <= threshold * img.shape[1]:
    # #         cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), 0, 2)
    #
    #
    #
    #
    # cv2.imshow("1", bk)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()