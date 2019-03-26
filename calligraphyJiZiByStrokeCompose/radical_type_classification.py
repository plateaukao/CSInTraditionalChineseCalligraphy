# coding: utf-8
import cv2
import os
import xml.etree.ElementTree as ET
import shutil

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"
save_path = "../../../Data/radical types/"

char_png_path = "../../../Data/Calligraphy_database/kai/"


def radical_type_classifer():

    radical_type_set = set()

    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    for child in root:

        structure_item = child.findall('STRUCTURE')
        if structure_item:
            structure_type = structure_item[0].text
            radical_type_set.add(structure_type)

    print(radical_type_set)

    # make type directory
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for rt in radical_type_set:
        if not os.path.exists(os.path.join(save_path, rt)):
            os.mkdir(os.path.join(save_path, rt))

    # copy png file to directory with his structure info
    png_names = [f for f in os.listdir(char_png_path) if '.png' in f]

    for child in root:
        tag = child.attrib["TAG"].strip()
        if len(tag) > 1:
            continue

        structure_type = ""
        structure_item = child.findall('STRUCTURE')
        if structure_item:
            structure_type = structure_item[0].text
        if structure_type == "":
            continue

        for pn in png_names:
            if pn.startswith(tag):
                shutil.copy2(os.path.join(char_png_path, pn), os.path.join(save_path, structure_type, pn))










if __name__ == '__main__':
    radical_type_classifer()