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
    query_char_info_from_chars_list, query_similar_basic_radicals_and_strokes, render_generated_image

from utils.Functions import createBlankGrayscaleImageWithSize, getSingleMaxBoundingBoxOfImage


class CalligraphyJiZiByStrokeCompse(QMainWindow, Ui_MainWindow):

    __library_root_path = "../../../Data/Calligraphy_database/char_generate_lib/"
    library_bs_root_path = "../../../Data/Calligraphy_database/char_generate_lib/basic radicals dataset"
    library_stroke_root_path = "../../../Data/Calligraphy_database/char_generate_lib/strokes dataset"
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

    current_char_obj = None

    current_bs_id = 0
    current_bs_img_id = 0
    current_stroke_id = 0
    current_stroke_img_id = 0

    select_char_id = 0

    select_stroke_image_path = ""

    similar_basic_radicals_dict = None
    similar_strokes_dict = None





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

        temp_path = './temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        svg_content = '<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" ' \
                      '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> <svg version="1.0" xmlns="http://www.w3.org/2000/svg" ' \
                      'width="400.000000pt" height="400.000000pt" viewBox="0 0 400.000000 400.000000" preserveAspectRatio="xMidYMid meet"> ' \
                      '<g transform="translate(0.000000,400.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> \n'
        for key in self.__select_strokes_dict.keys():
            stroke_img_path = self.__select_strokes_dict[key]

            stroke_img = cv2.imread(stroke_img_path, 0)

            # save narray to png
            png_img_path = os.path.join(temp_path, "stroke_{}.png".format(key))
            cv2.imwrite(png_img_path, stroke_img)

            # convert png to bmp
            bmp_img_path = os.path.join(temp_path, "stroke_{}.bmp".format(key))
            img_ = Image.open(png_img_path)
            img_.save(bmp_img_path)

            # convert bmp to svg
            svg_img_path = os.path.join(temp_path, "stroke_{}.svg".format(key))
            os.system("potrace  --svg {} -o {}".format(bmp_img_path, svg_img_path))

            # parse svg file to extract path
            # open svg file
            dom = minidom.parse(svg_img_path)

            # find path element in original svg file
            root = dom.documentElement
            path_elems = root.getElementsByTagName("path")
            if path_elems is None:
                print("not find path elements")
                return
            print("path elements len: ", len(path_elems))

            for i in range(len(path_elems)):
                d = path_elems[i].getAttribute('d')
                svg_content += '<path d="' + d + '"></path> \n'

            # del temp files
            os.system('rm {}'.format(png_img_path))
            os.system('rm {}'.format(bmp_img_path))
            os.system('rm {}'.format(svg_img_path))

        svg_content += '</g></svg>'

        with open(os.path.join(filename, self.current_char_obj.tag + ".svg"), 'w') as f:
            f.write(svg_content)

    def handle_chars_tag_listview_item_clicked(self, qModelIndex):
        print(qModelIndex.row())
        id_ = qModelIndex.row()

        self.select_char_id = id_

        # get char object
        char_obj_ = self.__chars_info_list[id_]
        self.current_char_obj = char_obj_

        # get similar basic radicals and strokes
        similar_basic_radicals_dict_, similar_strokes_dict_ = self.__similar_radicals_and_strokes_list[id_]
        self.similar_basic_radicals_dict, self.similar_strokes_dict = self.__similar_radicals_and_strokes_list[id_]

        # update the basic radicals tree view
        self.handle_char_basic_radicals_treeview_update(self.target_basic_radicals_treeView, similar_basic_radicals_dict_)
        self.target_basic_radicals_treeView.expandAll()

        # update the strokes tree view
        self.handle_char_strokes_treeview_update(self.target_strokes_treeView, similar_strokes_dict_)
        self.target_strokes_treeView.expandAll()

        # select strokes to selected strokes
        for sk in char_obj_.strokes:
            self.__select_strokes_dict[int(sk.id)] = ""

        # get all default basic radicals strokes
        for k in similar_basic_radicals_dict_.keys():

            # char bs strokes id
            ch_bs_obj = None
            for ch_bs in char_obj_.basic_radicals:
                if ch_bs.id == k:
                    ch_bs_obj = ch_bs
            if ch_bs_obj is None:
                continue

            ch_strokes_id = ch_bs_obj.strokes_id  # here!!!!!!!!
            print("char strokes id: ", ch_strokes_id)

            if len(similar_basic_radicals_dict_[k]) == 0:
                continue

            bs_obj = similar_basic_radicals_dict_[k][0]    # first element of bs
            print(bs_obj)
            print(type(bs_obj))
            bs_obj_path = bs_obj["path"]
            bs_obj_tag = bs_obj_path.split("/")[-1].split("_")[0]
            bs_obj_strokes_id = bs_obj["strokes_id"]
            print("bs strokes id: ", bs_obj_strokes_id)

            bs_char_path_ = os.path.join(self.__char_root_path, bs_obj_tag, "strokes")
            bs_stroke_img_names_ = [f for f in os.listdir(bs_char_path_) if ".png" in f]

            if len(ch_strokes_id) != len(bs_obj_strokes_id):
                print("char strokes id not same similar bs!")
                continue

            # find stroke path of similar bs
            for i in range(len(ch_strokes_id)):
                for bn in bs_stroke_img_names_:
                    if "_" + str(bs_obj_strokes_id[i]) + "." in bn:
                        self.__select_strokes_dict[int(ch_strokes_id[i])] = os.path.join(bs_char_path_, bn)
                        break
        print(self.__select_strokes_dict)

        # get all default stroke
        for k in similar_strokes_dict_.keys():
            strokes_path_ = similar_strokes_dict_[k]
            self.__select_strokes_dict[int(k)] = strokes_path_[0]
        print(self.__select_strokes_dict)

        # recompose default basic radicals and strokes
        size = 400
        image = createBlankGrayscaleImageWithSize((size, size))
        offset_base = int(abs(size - 256) / 2)


        for key in self.__select_strokes_dict.keys():

            # get real position of stroke
            print(char_obj_.strokes)
            real_post = char_obj_.strokes[int(key)].position

            cent_x0 = int(real_post[0] + real_post[2] / 2)
            cent_y0 = int(real_post[1] + real_post[3] / 2)

            # get position of similar stroke
            stroke_path = self.__select_strokes_dict[key]
            stroke_img = cv2.imread(stroke_path, 0)
            stroke_rect = getSingleMaxBoundingBoxOfImage(stroke_img)
            if stroke_rect is None:
                continue

            for x in range(stroke_rect[2]):
                for y in range(stroke_rect[3]):
                    if stroke_img[stroke_rect[1] + y][stroke_rect[0] + x] == 0:
                        image[cent_y0-int(stroke_rect[3]/2)+offset_base+y][cent_x0-int(stroke_rect[2]/2)+offset_base+x] = \
                        stroke_img[stroke_rect[1] + y][stroke_rect[0] + x]

        # display generated image
        qimg_ = QImage(image.data, image.shape[1], image.shape[0], image.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.result_scene.addPixmap(qimg_pix_)
        self.result_scene.setSceneRect(QRectF())
        self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)
        self.result_scene.update()

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

        bs_id = self.target_basic_radicals_treeView.currentIndex().parent().row()
        bs_img_id = self.target_basic_radicals_treeView.currentIndex().row()
        print(bs_id, " ", bs_img_id)

        if bs_id == -1:
            print("Clicked invalid content, not update the image!")
            return

        # update the stroke list
        select_bs_dict = self.similar_basic_radicals_dict[str(bs_id)][bs_img_id]
        print(select_bs_dict)
        select_bs_strokes_id = select_bs_dict["strokes_id"]
        select_bs_path = select_bs_dict["path"]
        print("select strokes id: ", select_bs_strokes_id)

        # real char strokes id
        real_strokes_id = []
        for bs in self.current_char_obj.basic_radicals:
            if bs.id == str(bs_id):
                real_strokes_id = bs.strokes_id
        print("real strokes id: ", real_strokes_id)

        if len(select_bs_strokes_id) != len(real_strokes_id):
            print("select and real strokes id not same size!")
            return

        # find stroke names of select bs char
        select_bs_char_tag = select_bs_path.split("/")[-1].split("_")[0]
        select_bs_strokes_name = [f for f in os.listdir(os.path.join(self.__char_root_path, select_bs_char_tag, "strokes")) if ".png" in f]
        print(select_bs_strokes_name)

        for i in range(len(real_strokes_id)):
            for sn in select_bs_strokes_name:
                if "_" + str(select_bs_strokes_id[i]) + "." in sn:
                    self.__select_strokes_dict[str(real_strokes_id[i])] = os.path.join(self.__char_root_path, select_bs_char_tag, "strokes", sn)

        image = render_generated_image(self.current_char_obj, self.__select_strokes_dict)
        # display generated image
        qimg_ = QImage(image.data, image.shape[1], image.shape[0], image.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.result_scene.addPixmap(qimg_pix_)
        self.result_scene.setSceneRect(QRectF())
        self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)
        self.result_scene.update()

        # display select bs
        bs_img = cv2.imread(select_bs_path, 0)
        qimg_ = QImage(bs_img.data, bs_img.shape[1], bs_img.shape[0], bs_img.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.basic_radical_scene.addPixmap(qimg_pix_)
        self.basic_radical_scene.setSceneRect(QRectF())
        self.basic_radical_graphicsView.fitInView(self.basic_radical_scene.sceneRect(), Qt.KeepAspectRatio)
        self.basic_radical_scene.update()




        # update the generated image

    def handle_char_strokes_tree_view_item_clicked(self, qModelIndex):
        print(qModelIndex.row())

        # update the generated image
        stroke_id = self.target_strokes_treeView.currentIndex().parent().row()
        stroke_img_id = self.target_strokes_treeView.currentIndex().row()
        print(stroke_id, " ", stroke_img_id)

        # click invaild content of stroke_id, not update image
        if stroke_id == -1:
            print("Click invaild content, not update the image!")
            return
        # get the select stroke path
        self.current_stroke_id = stroke_id
        self.current_stroke_img_id = stroke_img_id

        stroke_img_name = self.target_strokes_treeView.currentIndex().data()
        print(stroke_id, " ", stroke_img_name)
        stroke_type = stroke_img_name.split("_")[2]
        stroke_img_path = os.path.join(self.library_stroke_root_path, stroke_type, stroke_img_name)
        self.select_stroke_image_path = stroke_img_path
        self.__select_strokes_dict[stroke_id] = stroke_img_path

        image = render_generated_image(self.current_char_obj, self.__select_strokes_dict)
        # display generated image
        qimg_ = QImage(image.data, image.shape[1], image.shape[0], image.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.result_scene.addPixmap(qimg_pix_)
        self.result_scene.setSceneRect(QRectF())
        self.result_graphicsView.fitInView(self.result_scene.sceneRect(), Qt.KeepAspectRatio)
        self.result_scene.update()

        # display select stroke image
        stroke_img = cv2.imread(self.select_stroke_image_path, 0)
        qimg_ = QImage(stroke_img.data, stroke_img.shape[1], stroke_img.shape[0], stroke_img.shape[1], QImage.Format_Indexed8)
        qimg_pix_ = QPixmap.fromImage(qimg_)
        self.stroke_scene.addPixmap(qimg_pix_)
        self.stroke_scene.setSceneRect(QRectF())
        self.stroke_graphicsView.fitInView(self.stroke_scene.sceneRect(), Qt.KeepAspectRatio)
        self.stroke_scene.update()










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