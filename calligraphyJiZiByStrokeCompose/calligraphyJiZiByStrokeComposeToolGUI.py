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
from calligraphyJiZiByStrokeCompose.util import query_char_info, query_char_target_strokes, stroke_recompose


class CalligraphyJiZiByStrokeCompse(QMainWindow, Ui_MainWindow):
    __library_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"
    __xml_dataset_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"
    __input_content = ""
    __chars_info_list = []
    __chars_tag_list = []
    __chars_stroke_list = []
    __char_target_strokes_list = []

    __recomposed_results = []

    __target_char_strokes = []

    def __init__(self):
        super(CalligraphyJiZiByStrokeCompse, self).__init__()
        self.setupUi(self)

        self.chars_tag_slm = QStringListModel()
        self.chars_tag_slm.setStringList(self.__chars_tag_list)
        self.chars_listView.setModel(self.chars_tag_slm)
        self.chars_listView.clicked.connect(self.handle_chars_tag_listview_item_clicked)

        self.char_strokes_slm = QStringListModel()
        self.strokes_listView.setModel(self.char_strokes_slm)
        self.strokes_listView.clicked.connect(self.handle_char_stroke_listview_item_clicked)

        self.result_scene = QGraphicsScene()
        self.result_scene.setBackgroundBrush(Qt.gray)
        self.result_graphicsView.setScene(self.result_scene)
        self.result_scene.setSceneRect(QRectF())
        self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)

        self.stroke_scene = QGraphicsScene()
        self.stroke_scene.setBackgroundBrush(Qt.gray)
        self.stroke_graphicsView.setScene(self.stroke_scene)
        self.stroke_scene.setSceneRect(QRectF())
        self.stroke_graphicsView.fitInView(self.stroke_scene.sceneRect(), Qt.KeepAspectRatio)

        self.set_pushButton.clicked.connect(self.handle_setting_btn)
        self.generate_pushButton.clicked.connect(self.handle_generate_btn)

    def handle_setting_btn(self):
        print("Setting button clicked!")

    def handle_generate_btn(self):
        print("Generate button clicked!")

        # process input content
        input_conent = self.input_textEdit.toPlainText()
        input_conent = input_conent.replace(' ', '').replace('\n', '').replace('\t', '')

        self.__input_content = input_conent
        print(input_conent)

        # query chars info list
        self.__chars_info_list = query_char_info(input_conent)
        print(self.__chars_info_list)

        # add to chars list
        self.__chars_tag_list = []
        for cc in self.__chars_info_list:
            self.__chars_tag_list.append(cc.tag)
        # update the chars tag list
        self.chars_tag_slm.setStringList(self.__chars_tag_list)

        # query chars target strokes
        self.__char_target_strokes_list = query_char_target_strokes(self.__chars_info_list)

        # stroke recompose
        self.__recomposed_results = stroke_recompose(self.__chars_info_list, self.__char_target_strokes_list)

        # update result gview
        if len(self.__recomposed_results) > 0:
            img_ = self.__recomposed_results[0]
            qimg_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)

            qimg_pix_ = QPixmap.fromImage(qimg_)
            self.result_scene.addPixmap(qimg_pix_)
            self.result_scene.setSceneRect(QRectF())
            self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)
            self.result_scene.update()
        else:
            print("Not generate results")
            return

    def handle_chars_tag_listview_item_clicked(self, qModelIndex):
        print(qModelIndex.row())

        index = qModelIndex.row()
        select_char_info = self.__chars_info_list[index]
        select_char_strokes = self.__char_target_strokes_list[index]
        print(select_char_strokes)

        self.__target_char_strokes = []
        for lt in select_char_strokes:
            if len(lt) == 0:
                self.__target_char_strokes.append("")
            else:
                self.__target_char_strokes.append(lt[0])

        self.char_strokes_slm.setStringList(self.__target_char_strokes)
        self.stroke_info_label.setText(select_char_info.stroke_orders_to_string)

        # update result gview
        if len(self.__recomposed_results) > 0:
            img_ = self.__recomposed_results[index]
            qimg_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)

            qimg_pix_ = QPixmap.fromImage(qimg_)
            self.result_scene.addPixmap(qimg_pix_)
            self.result_scene.setSceneRect(QRectF())
            self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)
            self.result_scene.update()
        else:
            print("Not generate results")
            return

    def handle_char_stroke_listview_item_clicked(self, qModelIndex):
        print(qModelIndex.row())
        index = qModelIndex.row()

        if len(self.__target_char_strokes) > 0:
            img_path = self.__target_char_strokes[index]
            if img_path != "":
                img_ = cv2.imread(img_path, 0)
                qimage_ = QImage(img_.data, img_.shape[1], img_.shape[0], img_.shape[1], QImage.Format_Indexed8)
                qimage_pix_ = QPixmap.fromImage(qimage_)
                self.stroke_scene.addPixmap(qimage_pix_)
                self.stroke_scene.setSceneRect(QRectF())
                self.stroke_graphicsView.fitInView(self.stroke_scene.sceneRect(), Qt.KeepAspectRatio)
                self.stroke_scene.update()
        else:
            print("Not strokes existing!")
            return




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CalligraphyJiZiByStrokeCompse()
    mainWindow.show()
    sys.exit(app.exec_())

