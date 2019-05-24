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

import xml.etree.ElementTree as ET

from utils.Functions import prettyXml

from xml_query_edit_tool.xml_query_edit_mainwindow import Ui_MainWindow
from xml_query_edit_tool.model import ChineseCharacter, BasicRadical

class XMLQueryAndEditAppGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(XMLQueryAndEditAppGUI, self).__init__()
        self.setupUi(self)

        self.xml_path = ""

        self.search_char = ""

        self.xml_tree = None
        self.xml_root = None

        self.target_radical_element = None
        self.target_ch_obj = None

        self.open_pushButton.clicked.connect(self.handle_open_button)
        self.search_pushButton.clicked.connect(self.handle_search_button)
        self.save_pushButton.clicked.connect(self.handle_save_button)

    def handle_open_button(self):
        print("Open button clicked!")

        self.xml_path, _ = QFileDialog.getOpenFileName(None, "Open file", QDir.currentPath())
        if self.xml_path != "":
            print(self.xml_path)

        if not os.path.exists(self.xml_path):
            print("Xml not existed!")
            return

        self.xml_main_webEngineView.load(QUrl.fromLocalFile(self.xml_path))
        self.xml_main_webEngineView.show()

        # parse xml data
        self.xml_tree = ET.parse(self.xml_path)
        if self.xml_tree is None:
            print("Xml tree is none!")
            return
        self.xml_root = self.xml_tree.getroot()
        if self.xml_root is None:
            print("Xml root is none!")
            return

    def handle_search_button(self):
        print("Search button clicked!")
        self.search_char = self.search_lineEdit.text().strip()
        print("search: {}".format(self.search_char))

        if self.search_char == "":
            print("Search char is none!")
            return

        # find target radical element
        self.target_radical_element = None

        for i in range(len(self.xml_root)):
            radical_elem = self.xml_root[i]
            tag = radical_elem.attrib["TAG"].strip()
            if tag == self.search_char:
                self.target_radical_element = radical_elem
                break

        if self.target_radical_element is None:
            print("not find target radical element")
            return

        self.target_ch_obj = self.radical_elememt_to_chinese_character_object(self.target_radical_element)
        if self.target_ch_obj is None:
            print("target ch obj is none!")
            return

        if len(self.target_ch_obj.basic_radicals) > 0:
            # update bs 1
            if self.target_ch_obj.basic_radicals[0]:
                bs_obj = self.target_ch_obj.basic_radicals[0]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_0_id_lineEdit.setText(bs_id)
                self.bs_0_tag_lineEdit.setText(bs_tag)
                self.bs_0_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_0_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)

        # update bs 2
        if len(self.target_ch_obj.basic_radicals) > 1:
            # update bs 1
            if self.target_ch_obj.basic_radicals[1]:
                bs_obj = self.target_ch_obj.basic_radicals[1]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_1_id_lineEdit.setText(bs_id)
                self.bs_1_tag_lineEdit.setText(bs_tag)
                self.bs_1_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_1_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)


        # update bs 3
        if len(self.target_ch_obj.basic_radicals) > 2:
            # update bs 1
            if self.target_ch_obj.basic_radicals[2]:
                bs_obj = self.target_ch_obj.basic_radicals[2]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_2_id_lineEdit.setText(bs_id)
                self.bs_2_tag_lineEdit.setText(bs_tag)
                self.bs_2_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_2_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)

        # update bs 4
        if len(self.target_ch_obj.basic_radicals) > 3:
            # update bs 1
            if self.target_ch_obj.basic_radicals[3]:
                bs_obj = self.target_ch_obj.basic_radicals[3]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_3_id_lineEdit.setText(bs_id)
                self.bs_3_tag_lineEdit.setText(bs_tag)
                self.bs_3_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_3_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)

        # update bs 5
        if len(self.target_ch_obj.basic_radicals) > 4:
            # update bs 1
            if self.target_ch_obj.basic_radicals[4]:
                bs_obj = self.target_ch_obj.basic_radicals[4]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_4_id_lineEdit.setText(bs_id)
                self.bs_4_tag_lineEdit.setText(bs_tag)
                self.bs_4_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_4_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)

        # update bs 6
        if len(self.target_ch_obj.basic_radicals) > 5:
            # update bs 1
            if self.target_ch_obj.basic_radicals[5]:
                bs_obj = self.target_ch_obj.basic_radicals[5]

                bs_id = bs_obj.id
                bs_tag = bs_obj.tag
                bs_strokes = bs_obj.strokes
                bs_similar_tags = bs_obj.similar_tags

                self.bs_5_id_lineEdit.setText(bs_id)
                self.bs_5_tag_lineEdit.setText(bs_tag)
                self.bs_5_strokes_lineEdit.setText(str(bs_strokes).replace("[", "").replace("]", "").replace("'", ""))
                self.bs_5_similar_tag_plainTextEdit.setPlainText(bs_similar_tags)



        self.unicode_label.setText(self.target_ch_obj.ucode)
        self.char_label.setText(self.target_ch_obj.tag)
        self.type_lineEdit.setText(self.target_ch_obj.type)
        self.struct_lineEdit.setText(self.target_ch_obj.struct)
        self.key_radical_lineEdit.setText(self.target_ch_obj.key_radical)
        self.stroke_count_lineEdit.setText(self.target_ch_obj.stroke_count)
        self.stroke_order_lineEdit.setText(self.target_ch_obj.stroke_order)



    def get_type_info(self, target_radical_element):
        if target_radical_element is None:
            return ""
        type_elems = target_radical_element.findall("TYPE")
        if type_elems:
            return type_elems[0].text.strip()

        return ""

    def get_struct_info(self, target_radical_element):
        if target_radical_element is None:
            return ""
        struct_elems = target_radical_element.findall("STRUCTURE")
        if struct_elems:
            return struct_elems[0].text.strip()

        return ""

    def get_key_radical_info(self, target_radical_element):
        if target_radical_element:
            key_radical_elems = target_radical_element.findall("KEY_RADICAL")
            if key_radical_elems:
                return key_radical_elems[0].text.strip()

        return ""

    def get_stroke_count_info(self, target_radical_element):
        if target_radical_element:
            stroke_count_elems = target_radical_element.findall("STROKE_COUNT")
            if stroke_count_elems:
                return stroke_count_elems[0].text.strip()

        return ""

    def get_stroke_order_info(self, target_radical_element):
        if target_radical_element:
            stroke_order_elems = target_radical_element.findall("STROKE_ORDER")
            if stroke_order_elems:
                return stroke_order_elems[0].text.replace("|", ", ").strip()

        return ""

    def radical_elememt_to_chinese_character_object(self, target_radical_element):
        if target_radical_element is None:
            return

        # update radical element information display
        id_str = target_radical_element.attrib["ID"].strip()
        tag_str = target_radical_element.attrib["TAG"].strip()

        type_str = self.get_type_info(target_radical_element)
        struct_str = self.get_struct_info(target_radical_element)
        key_radical_str = self.get_key_radical_info(target_radical_element)
        stroke_count_str = self.get_stroke_count_info(target_radical_element)
        stroke_order_str = self.get_stroke_order_info(target_radical_element)

        # basic radicals
        basic_radicals_obj_list = []  # [{id:'', tag:'', strokes;[0,1,2], similar_tag:['一'，'二']}]

        basic_radicals_root_elems = target_radical_element.findall("BASIC_RADICALS")
        if basic_radicals_root_elems:
            bs_elems = basic_radicals_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                bs_dict = {}

                for bs_id in range(len(bs_elems)):
                    bs_item = bs_elems[bs_id]
                    bs_id = bs_item.attrib["ID"].strip()
                    bs_tag = bs_item.attrib["TAG"].strip()

                    bs_strokes = []
                    bs_sk_root_elems = bs_item.findall("STROKES")
                    if bs_sk_root_elems:
                        bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                        for bs_sk_item in bs_sk_elems:
                            bs_sk_id = bs_sk_item.attrib["ID"].strip()
                            bs_strokes.append(bs_sk_id)

                    bs_similar_tags = ""
                    bs_similar_tag_elems = bs_item.findall("SIMILAR_TAG")
                    if bs_similar_tag_elems:
                        bs_similar_tags = bs_similar_tag_elems[0].text.replace("[", "").replace("]", "").replace(
                            "'", "").strip()

                    bs_dict["bs_id"] = bs_id
                    bs_dict["bs_tag"] = bs_tag
                    bs_dict["bs_strokes"] = str(bs_strokes)
                    bs_dict["bs_similar_tags"] = str(bs_similar_tags)

                    bs_obj = BasicRadical()
                    bs_obj.id = bs_id
                    print(bs_id)
                    bs_obj.tag = bs_tag
                    bs_obj.strokes = bs_strokes.copy()
                    bs_obj.similar_tags = bs_similar_tags

                    basic_radicals_obj_list.append(copy.deepcopy(bs_obj))

        print("bs len: {}".format(len(basic_radicals_obj_list)))

        # chinese character obj
        ch_obj = ChineseCharacter()
        ch_obj.ucode = id_str
        ch_obj.tag = tag_str
        ch_obj.type = type_str
        ch_obj.struct = struct_str
        ch_obj.key_radical = key_radical_str
        ch_obj.stroke_count = stroke_count_str
        ch_obj.stroke_order = stroke_order_str

        ch_obj.basic_radicals = basic_radicals_obj_list.copy()

        return copy.deepcopy(ch_obj)

    def handle_save_button(self):
        print("Save button clicked!")

        # update target radical element
        self.update_target_radical_element()

        # save to original xml file
        prettyXml(self.xml_root, '\t', '\n')
        self.xml_tree.write(self.xml_path, encoding='utf-8')

        # reload main xml display
        self.xml_main_webEngineView.load(QUrl.fromLocalFile(self.xml_path))
        self.xml_main_webEngineView.show()


    def update_target_radical_element(self):
        type_str = self.type_lineEdit.text().strip()
        struct_str = self.type_lineEdit.text().strip()
        key_radical_str = self.key_radical_lineEdit.text().strip()
        stroke_count_str = self.stroke_count_lineEdit.text().strip()
        stroke_order_str = self.stroke_order_lineEdit.text().strip()

        # update the info of character
        # type
        type_elems = self.target_radical_element.findall("TYPE")
        if type_elems:
            type_elems[0].text = type_str

        # struct
        struct_elems = self.target_radical_element.findall("STRUCTURE")
        if struct_elems:
            struct_elems[0].text = struct_str

        # key_radical
        key_radical_elems = self.target_radical_element.findall("KEY_RADICAL")
        if key_radical_elems:
            key_radical_elems[0].text = key_radical_str

        # stroke count
        stroke_count_elems = self.target_radical_element.findall("STROKE_COUNT")
        if stroke_count_elems:
            stroke_count_elems[0].text = stroke_count_str

        # stroke order
        stroke_order_elems = self.target_radical_element.findall("STROKE_ORDER")
        if stroke_order_elems:
            stroke_order_elems[0].text = stroke_order_str

        # basic radicals info
        bs_root_elems = self.target_radical_element.findall("BASIC_RADICALS")
        if bs_root_elems is None or len(bs_root_elems) == 0:
            return

        bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
        if bs_elems is None or len(bs_elems) == 0:
            return

        bs_0_id_str = self.bs_0_id_lineEdit.text().strip()
        bs_0_tag_str = self.bs_0_tag_lineEdit.text().strip()
        bs_0_strokes_list = self.bs_0_strokes_lineEdit.text().split(",")
        bs_0_strokes_list = [bs.strip() for bs in bs_0_strokes_list]
        bs_0_similar_tags = self.bs_0_similar_tag_plainTextEdit.toPlainText().strip()

        if bs_0_id_str == "":
            return
        else:
            # update the basic radical 0
            bs_elems[0].set("ID", bs_0_id_str)
            bs_elems[0].set("TAG", bs_0_tag_str)

            # not need update strokes
            bs_0_similar_tags_elems = bs_elems[0].findall("SIMILAR_TAG")
            if bs_0_similar_tags_elems:
                bs_0_similar_tags_elems[0].text = bs_0_similar_tags


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = XMLQueryAndEditAppGUI()
    MainWindow.show()
    sys.exit(app.exec_())