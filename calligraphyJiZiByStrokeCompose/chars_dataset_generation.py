# coding: utf-8
import os
import cv2
import shutil
import xml.etree.ElementTree as ET

from utils.Functions import splitConnectedComponents


xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"

char_png_path = "../../../Data/SVG_2_PNG_chars"

save_path = "../../../Data/Calligraphy_database/Chars/"

save_classification_path = "../../../Data/Calligraphy_database/Chars_classification/"

file_names = [f for f in os.listdir(char_png_path) if ".png" in f]

strokes_path = "../../../Data/Strokes_png/"

stroke_names = [f for f in os.listdir(strokes_path) if ".png" in f]


def chars_dataset_generationg():

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    for child in root:
        tag = child.attrib["TAG"].strip()
        if len(tag) > 1:
            continue
        # if not os.path.exists(os.path.join(save_path, tag)):
        #     os.mkdir(os.path.join(save_path, tag))
        #
        # # copy char image
        img_name = ""
        for fn in file_names:
            if fn.startswith(tag):
                shutil.copy2(os.path.join(char_png_path, fn), os.path.join(save_path, tag, fn))
                img_name = fn
                break
        if not os.path.exists(os.path.join(save_path, tag, img_name)):
            print(tag)
            continue
        #
        img_ = cv2.imread(os.path.join(save_path, tag, img_name), 0)
        #
        # # make structure directory
        # if not os.path.exists(os.path.join(save_path, tag, "structures")):
        #     os.mkdir(os.path.join(save_path, tag, "structures"))
        #
        # # make basic radicals directory
        # if not os.path.exists(os.path.join(save_path, tag, "basic radicals")):
        #     os.mkdir(os.path.join(save_path, tag, "basic radicals"))
        # #
        print(tag)
        connect_components = splitConnectedComponents(img_)
        for i in range(len(connect_components)):
            cv2.imwrite(os.path.join(save_path, tag, "basic radicals", img_name.replace(".png", "") + "_" + str(i) + ".png"), connect_components[i])


        # make strokes directory
        # if not os.path.exists(os.path.join(save_path, tag, "strokes")):
        #     os.mkdir(os.path.join(save_path, tag, "strokes"))
        #
        # for sn in stroke_names:
        #     if sn.startswith(tag):
        #         shutil.copy2(os.path.join(strokes_path, sn), os.path.join(save_path, tag, "strokes"))

        # structure_type = ""
        # structure_item = child.findall('STRUCTURE')
        # if structure_item:
        #     structure_type = structure_item[0].text
        # if structure_type == "Single Character":
        #     shutil.move(os.path.join(save_path, tag), os.path.join(save_classification_path))


def rename_basic_radical_and_add_structure_single_character():
    file_name = [f for f in os.listdir(save_classification_path) if "." not in f]
    print(file_name)

    # for fn in file_name:
    #     basic


if __name__ == '__main__':
    chars_dataset_generationg()
    # rename_basic_radical_and_add_structure_single_character()