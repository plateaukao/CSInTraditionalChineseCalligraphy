import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

import cv2
from PIL import Image
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from character_synthesis_tool.character_synthesis import get_similar_basic_radicals_strokes_list
from character_synthesis_tool.character_synthesis_mainwindow import Ui_MainWindow
from character_synthesis_tool.generate_template_folders import generate_template_folders
from character_synthesis_tool.merg_bs_stroke_images import get_strokes_position_dict, \
    merge_select_stroke_images, get_bs_sk_ids_list, get_similar_chars_with_same_struct_and_bs_tags
from utils.Functions import createBlankGrayscaleImageWithSize


class CharacterSynthesisGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CharacterSynthesisGUI, self).__init__()
        self.setupUi(self)

        self.xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position_add_stroke_order_recorrect_add_true_post.xml"
        self.xml_tree = None
        self.xml_root = None

        self.char_png_path = "../../../Data/Calligraphy_database/Chars_pngs"

        if self.xml_path != "":
            self.xml_tree = ET.parse(self.xml_path)
            self.xml_root = self.xml_tree.getroot()

        self.size = (500, 500)
        self.bk = None
        self.sk_bks = None

        self.char = ""
        self.char_id = 0

        self.select_bs_id = 0   # bs id
        self.select_bs_list_id = 0   # similar bs list item id
        self.select_bs_sk_id = 0     # stroke id of this bs

        self.select_sk_id = 0
        self.select_sk_img_id = 0

        self.template_chars_path = ""
        self.template_chars = []

        self.template_images_save_path = "../../../Data/Calligraphy_database/Chars_tempalte_library"

        self.stroke_image_path = "../../../Data/Calligraphy_database/Stroke_pngs"

        self.input_chars = ""

        self.bs_similar_threshold = 10
        self.sk_similar_threshold = 10

        self.bs_threshold_lineEdit.setText("10")
        self.stroke_threshold_lineEdit.setText("10")

        self.generated_results_images = []
        self.chars_similar_basic_radicals_list = []
        self.chars_similar_strokes_list = []
        self.ch_similar_sk_id_img_name_dict = None

        self.generated_results_images_strokes = []

        self.ch_stroke_post_dict = None
        self.ch_similar_sk_id_img_name_dict = None

        self.grayscale_scene = QGraphicsScene()
        self.grayscale_scene.setBackgroundBrush(Qt.gray)
        self.grayscale_graphicsView.setScene(self.grayscale_scene)
        self.grayscale_scene.setSceneRect(QRectF())
        self.grayscale_graphicsView.fitInView(self.grayscale_scene.sceneRect(), Qt.KeepAspectRatio)

        self.src_scene = QGraphicsScene()
        self.src_scene.setBackgroundBrush(Qt.gray)
        self.src_graphicsView.setScene(self.src_scene)
        self.src_scene.setSceneRect(QRectF())
        self.src_graphicsView.fitInView(self.src_scene.sceneRect(), Qt.KeepAspectRatio)

        self.open_xml_pushButton.clicked.connect(self.handle_load_xml_button)
        self.open_chars_pushButton.clicked.connect(self.handle_load_tempalte_chars_button)
        self.tempate_generate_pushButton.clicked.connect(self.handle_generate_template_button)
        self.synthesis_pushButton.clicked.connect(self.handle_synthesis_button)
        self.generated_results_listWidget.itemClicked.connect(self.handle_generated_listwidget_item_click)
        self.similar_bs_treeView.clicked.connect(self.handle_similar_bs_treeview_item_clicked)
        self.similar_stroke_treeView.clicked.connect(self.handle_similar_strokes_treeview_item_clicked)
        self.svg_extract_pushButton.clicked.connect(self.handle_svg_extract_button)

    def handle_load_xml_button(self):
        print("load xml clicked")
        self.xml_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if self.xml_path != "":
            print(self.xml_path)

        if not os.path.exists(self.xml_path):
            print("Xml not existed!")
            return


        # parse xml data
        self.xml_tree = ET.parse(self.xml_path)
        if self.xml_tree is None:
            print("xml tree is none!")
            return
        self.xml_root = self.xml_tree.getroot()
        if self.xml_root is None:
            print("xml root is none")
            return

    def handle_load_tempalte_chars_button(self):
        print("load template chars clicked")

        # clean cache
        self.template_chars = []

        self.template_chars_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if not os.path.exists(self.template_chars_path):
            print("template chars not existed!")
            return

        with open(self.template_chars_path, "r") as f:
            for ch in f.readlines():
                self.template_chars.append(ch.strip())

        # show in gui
        self.temp_chars_plainTextEdit.setPlainText(str(self.template_chars))

    def handle_generate_template_button(self):
        print("generate template clicked")
        if self.template_chars is None or len(self.template_chars) == 0:
            print("template chars is none")
            return
        # get template save path
        self.template_images_save_path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if self.template_images_save_path == "":
            print("template images save path is none")
            return

        generate_template_folders(self.template_chars, self.xml_path, self.stroke_image_path, self.template_images_save_path)

        print("template generation successed!")

    def handle_synthesis_button(self):
        print("synthesis button clicked")

        # clean cache
        self.generated_results_listWidget.clear()
        self.generated_results_images = []
        self.chars_similar_strokes_list = []
        self.chars_sk_id_to_name_dict_list = []

        self.input_chars = self.input_plainTextEdit.toPlainText().strip()
        print(self.input_chars)

        # get input threshold
        if self.bs_threshold_lineEdit.text().isdigit():
            self.bs_similar_threshold = int(self.bs_threshold_lineEdit.text())
        else:
            print("bs threshold is not digit")

        if self.stroke_threshold_lineEdit.text().isdigit():
            self.sk_similar_threshold = int(self.stroke_threshold_lineEdit.text())
        else:
            print("sk threshold is not digit")

        self.chars_similar_basic_radicals_list, self.chars_similar_strokes_list, self.chars_sk_id_to_name_dict_list = \
            get_similar_basic_radicals_strokes_list(self.input_chars, self.xml_root, self.template_images_save_path,
                                                    self.stroke_image_path, bs_threshold=self.bs_similar_threshold,
                                                    sk_threshold=self.sk_similar_threshold)

        for img_id in range(len(self.chars_similar_basic_radicals_list)):
            item = QListWidgetItem("{}.png".format(self.input_chars[img_id]))
            self.generated_results_listWidget.addItem(item)

    def handle_generated_listwidget_item_click(self, item):
        print(self.generated_results_listWidget.currentRow())

        self.char_id = self.generated_results_listWidget.currentRow()
        self.char = self.input_chars[self.char_id]

        self.ch_stroke_post_dict = get_strokes_position_dict(self.xml_root, self.char)

        self.bk = createBlankGrayscaleImageWithSize(self.size)
        self.ch_similar_sk_id_img_name_dict = self.chars_sk_id_to_name_dict_list[self.char_id]
        self.bk, self.sk_bks = merge_select_stroke_images(self.bk, self.ch_stroke_post_dict, self.ch_similar_sk_id_img_name_dict,
                                                self.stroke_image_path)

        qimg = QImage(self.bk.data, self.bk.shape[1], self.bk.shape[0], self.bk.shape[1], QImage.Format_Indexed8)
        qimg_pix = QPixmap.fromImage(qimg)

        self.grayscale_scene.addPixmap(qimg_pix)
        self.grayscale_scene.update()

        # update the similar basic radicals tree widget
        if len(self.chars_similar_basic_radicals_list) > self.char_id:
            ch_similar_bs_dict = self.chars_similar_basic_radicals_list[self.char_id]
            print(ch_similar_bs_dict)
            self.handle_char_similar_bs_treeview_update(self.similar_bs_treeView, ch_similar_bs_dict)
            self.similar_bs_treeView.expandAll()

        # update the similar strokes tree widget
        if len(self.chars_similar_strokes_list) > self.char_id:
            ch_similar_sk_dict = self.chars_similar_strokes_list[self.char_id]
            print(ch_similar_sk_dict)
            self.handle_char_similar_sk_treeview_update(self.similar_stroke_treeView, ch_similar_sk_dict)
            self.similar_stroke_treeView.expandAll()


        real_img = self.find_char_png(self.char)
        print("select char {}: ".format(self.char))

        real_qimg = QImage(real_img.data, real_img.shape[1], real_img.shape[0], real_img.shape[1], QImage.Format_Indexed8)
        real_qimg_pix = QPixmap.fromImage(real_qimg)
        self.src_scene.addPixmap(real_qimg_pix)
        self.src_scene.update()

        # update similar chars with same bs tag of this char
        ch_bs_tags_dict, similar_chars_with_same_bs_tags_dict = get_similar_chars_with_same_struct_and_bs_tags(self.xml_root, self.char)
        print(similar_chars_with_same_bs_tags_dict)

        model = QStandardItemModel(self.similar_chars_bs_treeView)
        model.setColumnCount(1)

        for bs_id in similar_chars_with_same_bs_tags_dict.keys():
            bs_root_item = QStandardItem("Basic radical {}: {}".format(bs_id, ch_bs_tags_dict[bs_id]))
            bs_item = QStandardItem(str(similar_chars_with_same_bs_tags_dict[bs_id]))
            bs_root_item.appendRow(bs_item)
            model.appendRow(bs_root_item)

        self.similar_chars_bs_treeView.setModel(model)
        self.similar_chars_bs_treeView.expandAll()






    def handle_char_similar_bs_treeview_update(self, controls, similar_bs_dict, title="Similar Basic Radicals"):
        model = QStandardItemModel(controls)
        model.setColumnCount(1)

        for k in similar_bs_dict.keys():
            bs_root_item = QStandardItem("Basic radical {}".format(k))
            simi_bs_names = similar_bs_dict[k]

            for name_list in simi_bs_names:
                ch_tag = name_list[0].split("_")[0]
                sk_sub_item = QStandardItem(ch_tag)

                for name in name_list:
                    sk_sub_sub_item = QStandardItem(name)
                    sk_sub_item.appendRow(sk_sub_sub_item)
                bs_root_item.appendRow(sk_sub_item)
            model.setItem(k, 0, bs_root_item)
        controls.setModel(model)

    def handle_char_similar_sk_treeview_update(self, controls, similar_sk_dict, title="Similar Strokes"):
        model = QStandardItemModel(controls)
        model.setColumnCount(1)

        for k in similar_sk_dict.keys():
            sk_root_item = QStandardItem("Stroke {}".format(k))
            simi_sk_names = similar_sk_dict[k]

            for name in simi_sk_names:
                sk_sub_item = QStandardItem(name)
                sk_root_item.appendRow(sk_sub_item)
            model.setItem(k, 0, sk_root_item)
        controls.setModel(model)

    def find_char_png(self, ch):
        char_names = [f for f in os.listdir(self.char_png_path) if ".png" in f]
        char_name = ""
        for name in char_names:
            if ch in name:
                char_name = name
                break
        char_img_path = os.path.join(self.char_png_path, char_name)
        print(char_img_path)
        if not os.path.exists(char_img_path):
            print("not find char image")
            return

        char_img = cv2.imread(char_img_path, 0)
        _, char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY)
        return char_img.copy()

    def render_generated_result_image(self):

        self.ch_stroke_position_dict = get_strokes_position_dict(self.xml_root, self.char)

        self.bk = createBlankGrayscaleImageWithSize(self.size)
        self.bk, self.sk_bks = merge_select_stroke_images(self.bk, self.ch_stroke_position_dict, self.ch_similar_sk_id_img_name_dict,
                                        self.stroke_image_path)

        qimg = QImage(self.bk.data, self.bk.shape[1], self.bk.shape[0], self.bk.shape[1], QImage.Format_Indexed8)
        qimg_pix = QPixmap.fromImage(qimg)

        self.grayscale_scene.addPixmap(qimg_pix)
        self.grayscale_scene.update()

    def handle_similar_strokes_treeview_item_clicked(self, qModelIndex):

        self.select_sk_id = self.similar_stroke_treeView.currentIndex().parent().row()
        self.select_sk_img_id = self.similar_stroke_treeView.currentIndex().row()

        print(self.select_sk_id, self.select_sk_img_id)

        if self.select_sk_id == -1:
            print("clicked invalid content!")
            return

        # update with select sk id and sk name
        self.ch_similar_sk_id_img_name_dict[self.select_sk_id] = \
            self.chars_similar_strokes_list[self.char_id][self.select_sk_id][self.select_sk_img_id]

        self.render_generated_result_image()




    def handle_similar_bs_treeview_item_clicked(self, qModelIndex):

        if self.similar_bs_treeView.currentIndex().row() != -1 and \
            self.similar_bs_treeView.currentIndex().parent().row() != -1 and \
            self.similar_bs_treeView.currentIndex().parent().parent().row() == -1 and \
            self.similar_bs_treeView.currentIndex().parent().parent().parent().row() == -1:

            self.select_bs_id = self.similar_bs_treeView.currentIndex().parent().row()
            self.select_bs_list_id = self.similar_bs_treeView.currentIndex().row()

            print(self.select_bs_id, self.select_bs_list_id)

            bs_img_list = self.chars_similar_basic_radicals_list[self.char_id][self.select_bs_id]
            bs_sk_img_list = bs_img_list[self.select_bs_list_id]

            print(bs_sk_img_list)

            bs_sk_ids = get_bs_sk_ids_list(self.xml_root, self.char, self.select_bs_id)

            if len(bs_sk_ids) != len(bs_sk_img_list):
                print("bs sk ids not same as bs sk image ")

            for i in range(len(bs_sk_ids)):
                sk_id = bs_sk_ids[i]
                sk_img_name = bs_sk_img_list[i]
                self.ch_similar_sk_id_img_name_dict[sk_id] = sk_img_name

            self.render_generated_result_image()

        else:
            print("click invalid content")
            return

    def handle_svg_extract_button(self):
        print("svg extract")
        if self.sk_bks is None or len(self.sk_bks) == 0:
            print("sk bks is none")
            return

        temp_path = './svg_temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        svg_content = '<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" ' \
                      '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> <svg version="1.0" xmlns="http://www.w3.org/2000/svg" ' \
                      'width="{}pt" height="{}pt" viewBox="0 0 {} {}" preserveAspectRatio="xMidYMid meet"> ' \
                      '<g transform="translate(0.000000,{}) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> \n'\
                        .format(self.size[0], self.size[1], self.size[0], self.size[1], self.size[0])
        print("stroke num: ", len(self.sk_bks))

        for i in range(len(self.sk_bks)):
            img = self.sk_bks[i]

            png_img_path = os.path.join(temp_path, "{}_stroke_{}.png".format(self.char, i))
            cv2.imwrite(png_img_path, img)

            # convert png to bmp
            bmp_img_path = os.path.join(temp_path, "{}_stroke_{}.bmp".format(self.char, i))
            img_ = Image.open(png_img_path)
            img_.save(bmp_img_path)

            # convert bmp to svg
            svg_img_path = os.path.join(temp_path, "{}_stroke_{}.svg".format(self.char, i))
            os.system("potrace --svg {} -o {}".format(bmp_img_path, svg_img_path))

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

            # del jianti_temp files
            os.system('rm {}'.format(png_img_path))
            os.system('rm {}'.format(bmp_img_path))
            os.system('rm {}'.format(svg_img_path))

        svg_content += '</g></svg>'

        # save to svg file
        with open(os.path.join(filename, self.char + ".svg"), 'w') as f:
            f.write(svg_content)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = CharacterSynthesisGUI()
    MainWindow.show()
    sys.exit(app.exec_())