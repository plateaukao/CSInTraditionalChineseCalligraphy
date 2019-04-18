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

from calligraphyJiZiByStrokeCompose.mainwindow import Ui_MainWindow
from calligraphyJiZiByStrokeCompose.util import load_basic_radicals_library_dataset, load_stroke_library_dataset, \
    query_char_info_from_chars_list, query_similar_basic_radicals_and_strokes, recompose_chars

class CalligraphyJiZiByStrokeCompse(QMainWindow, Ui_MainWindow):

    __library_root_path = "../../../Data/Calligraphy_database/char_generate_lib/"
    __char_root_path = "/Users/liupeng/Documents/Data/Calligraphy_database/Chars_775"
    __xml_dataset_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

    __input_content = ""

    __chars_info_list = []
    __chars_tag_list = []

    __chars_stroke_list = []
    __chars_basic_radicals_list = []

    __char_target_strokes_list = []
    __char_target_basic_radicals_list = []

    # strokes and basic radicals libray dataset
    __strokes_dataset = None
    __basic_radicals_dataset = None

    __similar_radicals_and_strokes_list = []

    __select_strokes_dict = {}  # select strokes from similar basic radicals and strokes. used to draw result.






    def __init__(self):
        super(CalligraphyJiZiByStrokeCompse, self).__init__()
        self.setupUi(self)

        self.chars_tag_slm = QStringListModel()
        self.chars_tag_slm.setStringList(self.__chars_tag_list)
        self.chars_listView.setModel(self.chars_tag_slm)
        self.chars_listView.clicked.connect(self.handle_chars_tag_listview_item_clicked)

        self.result_scene = QGraphicsScene()
        self.result_scene.setBackgroundBrush(Qt.gray)
        self.result_graphicsView.setScene(self.result_scene)
        self.result_scene.setSceneRect(QRectF())
        self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)

        self.basic_radical_scene = QGraphicsScene()
        self.basic_radical_scene.setBackgroundBrush(Qt.gray)
        self.basic_radical_graphicsView.setScene(self.basic_radical_scene)
        self.basic_radical_scene.setSceneRect(QRectF())
        self.basic_radical_graphicsView.fitInView(self.basic_radical_scene.sceneRect(), Qt.KeepAspectRatio)

        self.stroke_scene = QGraphicsScene()
        self.stroke_scene.setBackgroundBrush(Qt.gray)
        self.stroke_graphicsView.setScene(self.stroke_scene)
        self.stroke_scene.setSceneRect(QRectF())
        self.stroke_graphicsView.fitInView(self.stroke_scene.sceneRect(), Qt.KeepAspectRatio)



        self.set_pushButton.clicked.connect(self.handle_load_library_btn)

        self.load_dataset_thread = LoadDatasetThread()
        self.load_dataset_thread.signal.connect(self.handle_load_library_thread)

        self.generate_pushButton.clicked.connect(self.handle_generate_btn)
        self.svg_extraction_pushButton.clicked.connect(self.handle_SVG_extraction_btn)

        self.target_basic_radicals_treeView.clicked.connect(self.handle_char_basic_radicals_treeview_item_clicked)
        self.target_strokes_treeView.clicked.connect(self.handle_char_strokes_tree_view_item_clicked)


    def handle_load_library_btn(self):
        print("Load library button clicked!")

        self.load_dataset_thread.start()
        self.statusbar.showMessage("Begin to load basic radicals and strokes dataset.....")

    def handle_load_library_thread(self, dataset):
        if dataset:
            self.__strokes_dataset = dataset["strokes"]
            self.__basic_radicals_dataset = dataset["basic_radicals"]
            self.statusbar.showMessage("Load dataset successed!")
        else:
            print("Load basic radicals and strokes dataset failed!")
            self.statusbar.showMessage("Load basic radicals and strokes dataset failed!")

    def handle_generate_btn(self):
        print("Generate button clicked!")

        # Process the input content: remove space, no-chinese characters
        input_conent = self.input_textEdit.toPlainText()
        input_conent = input_conent.replace(" ", "").replace("\n", "").replace("\t", "")

        self.__input_content = input_conent

        # query chars info list
        self.__chars_info_list = query_char_info_from_chars_list(input_conent, xml_path=self.__xml_dataset_path)

        # show found chars in chars listview
        self.__chars_tag_list = []
        for cc in self.__chars_info_list:
            self.__chars_tag_list.append(cc.tag)
        # update the chars listview
        self.chars_tag_slm.setStringList(self.__chars_tag_list)

        # # find similar basic radicals and strokes
        self.__similar_radicals_and_strokes_list = query_similar_basic_radicals_and_strokes(self.__basic_radicals_dataset, self.__strokes_dataset,
                                                                 self.__chars_info_list)
        print("Similar chars len: ", len(self.__similar_radicals_and_strokes_list))



    def handle_SVG_extraction_btn(self):
        print("SVG extraction button clicked")


    def handle_chars_tag_listview_item_clicked(self, qModelIndex):
        print(qModelIndex.row())
        id_ = qModelIndex.row()

        # get char object
        char_obj_ = self.__chars_info_list[id_]

        # get similar basic radicals and strokes
        similar_basic_radicals_dict_, similar_strokes_dict_ = self.__similar_radicals_and_strokes_list[id_]

        # update the basic radicals tree view
        self.handle_char_basic_radicals_treeview_update(self.target_basic_radicals_treeView, similar_basic_radicals_dict_)
        self.target_basic_radicals_treeView.expandAll()

        # update the strokes tree view
        self.handle_char_strokes_treeview_update(self.target_strokes_treeView, similar_strokes_dict_)
        self.target_strokes_treeView.expandAll()

        # select strokes to selected strokes
        for sk in char_obj_.strokes:
            self.__select_strokes_dict[sk.id] = ""

        # get all default basci radicals strokes
        for k in similar_strokes_dict_.keys():

            # char bs strokes id
            ch_bs_obj = char_obj_.basic_radicals[k]
            ch_strokes_id = ch_bs_obj.strokes_id  # here!!!!!!!!

            bs_obj = similar_strokes_dict_[k][0]    # first element of bs
            bs_obj_path = bs_obj["path"]
            bs_obj_tag = bs_obj_path.split("/")[-1].split("_")[0]
            bs_obj_strokes_id = bs_obj["strokes_id"]

            char_path_ = os.path.join(self.__char_root_path, bs_obj_tag, "strokes")
            stroke_img_names_ = [f for f in os.listdir(char_path_) if ".png" in f]




        # recompose default basic radicals and strokes




    def handle_char_basic_radicals_treeview_update(self, controls, similar_basic_radicals_dict, title="Similar basic radicals"):
        model = QStandardItemModel(controls)
        model.setColumnCount(1)

        for k in similar_basic_radicals_dict.keys():
            bs_objs = similar_basic_radicals_dict[k]

            bs_root_item = QStandardItem("Basic radical {}".format(k))

            bs_tag = ""
            for bs_obj in bs_objs:
                path_ = bs_obj["path"]
                simi_bs_name_ = path_.split("/")[-1]
                bs_tag = path_.split("/")[-2]

                bs_sub_item = QStandardItem(simi_bs_name_)
                bs_root_item.appendRow(bs_sub_item)
            bs_root_item.setText("Basic radical {}: {}".format(k, bs_tag))
            model.setItem(int(k), 0, bs_root_item)
        controls.setModel(model)



    def handle_char_strokes_treeview_update(self, controls, similar_strokes_dict, title="Similar strokes"):
        model = QStandardItemModel(controls)
        model.setColumnCount(1)

        for k in similar_strokes_dict.keys():

            sk_root_item = QStandardItem("Stroke {}".format(k))

            simi_sk_paths = similar_strokes_dict[k]

            for path_ in simi_sk_paths:
                simi_sk_name = path_.split("/")[-1]
                sk_sub_item = QStandardItem(simi_sk_name)
                sk_root_item.appendRow(sk_sub_item)
            model.setItem(int(k), 0, sk_root_item)
        controls.setModel(model)


    def handle_char_basic_radicals_treeview_item_clicked(self, qModelIndex):
        print(qModelIndex.row())

    def handle_char_strokes_tree_view_item_clicked(self, qModelIndex):
        print(qModelIndex.row())



class LoadDatasetThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        dataset = {}

        strokes_dataset = load_stroke_library_dataset("../../../Data/Calligraphy_database/char_generate_lib/strokes dataset")

        basic_radicals_dataset = load_basic_radicals_library_dataset("../../../Data/Calligraphy_database/char_generate_lib/basic radicals dataset")

        dataset["strokes"] = strokes_dataset
        dataset["basic_radicals"] = basic_radicals_dataset

        self.signal.emit(dataset)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CalligraphyJiZiByStrokeCompse()
    mainWindow.show()
    sys.exit(app.exec_())