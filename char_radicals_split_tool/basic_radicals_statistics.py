# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET
import shutil


def basic_radicals_statistics():
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

    tree = ET.parse(xml_path)

    if tree is None:
        print("Tree is none!")
        return

    root = tree.getroot()

    key_radical_set = set()

    for i in range(len(root)):
        elem = root[i]

        key_radical_elems = elem.findall("KEY_RADICAL")
        if key_radical_elems:
            key_radical_set.add(key_radical_elems[0].text)

    print(key_radical_set)


if __name__ == '__main__':
    basic_radicals_statistics()