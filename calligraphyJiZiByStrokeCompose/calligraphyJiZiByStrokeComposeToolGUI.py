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
from calligraphyJiZiByStrokeCompose.util import query_char_info, query_char_target_strokes, stroke_recompose, \
                    load_stroke_library_dataset, query_char_info_from_chars_list, query_char_target_stroke_by_dataset


class CalligraphyJiZiByStrokeCompse(QMainWindow, Ui_MainWindow):
    __library_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"
    __xml_dataset_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"
    __input_content = ""
    __chars_info_list = []
    __chars_tag_list = []
    __chars_stroke_list = []
    __char_target_strokes_list = []

    __recomposed_results = []
    __recomposed_stroke_results = []

    __target_char_strokes = []

    __stroke_dataset = None

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
        self.svg_extraction_pushButton.clicked.connect(self.handle_SVG_extraction_btn)

        self.load_dataset_thread = LoadStrokeDatasetThread()

        self.load_dataset_thread.signal.connect(self.handle_load_dataset_thread)

    def handle_setting_btn(self):
        print("Setting button clicked!")
        # start load dataset thread
        self.load_dataset_thread.start()
        self.statusbar.showMessage("Begin to load strokes dataset......")

    def handle_load_dataset_thread(self, dataset):
        if dataset:
            self.__stroke_dataset = dataset
            self.statusbar.showMessage("Load strokes dataset Success!")
        else:
            print("Load dataset failed!")
            self.statusbar.showMessage("Load strokes dataset Failed!")

    def handle_generate_btn(self):
        print("Generate button clicked!")

        # process input content
        input_conent = self.input_textEdit.toPlainText()
        input_conent = input_conent.replace(' ', '').replace('\n', '').replace('\t', '')

        self.__input_content = input_conent
        print(input_conent)

        # query chars info list
        self.__chars_info_list = query_char_info_from_chars_list(input_conent)
        print(self.__chars_info_list)

        # add to chars list
        self.__chars_tag_list = []
        for cc in self.__chars_info_list:
            self.__chars_tag_list.append(cc.tag)
        # update the chars tag list
        self.chars_tag_slm.setStringList(self.__chars_tag_list)

        # query chars target strokes
        self.__char_target_strokes_list = query_char_target_stroke_by_dataset(self.__stroke_dataset, self.__chars_info_list)

        # stroke recompose
        self.__recomposed_results, self.__recomposed_stroke_results = stroke_recompose(self.__chars_info_list, self.__char_target_strokes_list)

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

    def handle_SVG_extraction_btn(self):
        print("SVG extraction button clicked!")
        if self.__recomposed_stroke_results is None or len(self.__recomposed_stroke_results) == 0:
            self.statusbar.showMessage("Stroke templates is None")
            return

        filename = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        # convert bitmap to svg file
        temp_path = './temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        for char_id in range(len(self.__recomposed_stroke_results)):
            strokes_list = self.__recomposed_stroke_results[char_id]

            svg_content = '<?xml version="1.0" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" ' \
                          '"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> <svg version="1.0" xmlns="http://www.w3.org/2000/svg" ' \
                          'width="400.000000pt" height="400.000000pt" viewBox="0 0 400.000000 400.000000" preserveAspectRatio="xMidYMid meet"> ' \
                          '<g transform="translate(0.000000,400.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> \n'

            for stroke_id in range(len(strokes_list)):
                stroke_img = strokes_list[stroke_id]

                # save narray to png
                png_img_path = os.path.join(temp_path, self.__chars_info_list[char_id].tag + "_{}.png".format(stroke_id))
                cv2.imwrite(png_img_path, stroke_img)

                # convert png to bmp
                bmp_img_path = os.path.join(temp_path, self.__chars_info_list[char_id].tag + "_{}.bmp".format(stroke_id))
                img_ = Image.open(png_img_path)
                img_.save(bmp_img_path)

                # convert bmp to svg
                svg_img_path = os.path.join(temp_path, self.__chars_info_list[char_id].tag + "_{}.svg".format(stroke_id))
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

            with open(os.path.join(filename, self.__chars_info_list[char_id].tag + ".svg"), 'w') as f:
                f.write(svg_content)

        self.statusbar.showMessage("SVG files extracted success!")


class LoadStrokeDatasetThread(QThread):
    signal = pyqtSignal(object)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        dataset = None

        stroke_lib_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"
        dataset = load_stroke_library_dataset(stroke_lib_path)

        self.signal.emit(dataset)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CalligraphyJiZiByStrokeCompse()
    mainWindow.show()
    sys.exit(app.exec_())

