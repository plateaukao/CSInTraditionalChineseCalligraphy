# coding: utf-8
import os
import xml.etree.ElementTree as ET
from utils.Functions import getSingleMaxBoundingBoxOfImage, prettyXml

from pdf_generation_of_2300_9300_chars.convert_char_to_unicode_test import char_to_unicode_str



xml_path = "../../../Data/Characters/alldataset.xml"
xml_save_path = "../../../Data/Characters/alldataset_add3000chars.xml"

path_9300_txt = "../pdf_generation_of_2300_9300_chars/9300chars_cleaned.txt"

def add_9300_chars_to_alldataset_xml():
    # check existed chars in xml
    tree = ET.parse(xml_path)
    if tree is None:
        print("Tree of xml is None!")
        return
    root = tree.getroot()
    print("root num: ", len(root))

    tree_chars = []
    for i in range(len(root)):
        elem = root[i]
        tag = elem.attrib["TAG"].strip()

        if len(tag) == 1:
            tree_chars.append(tag)

    # read chars from 9300 cleaned txt
    contents = []
    with open(path_9300_txt, "r") as f:
        contents = f.readlines()

    contents = [c.replace("\n", "") for c in contents]
    print("Contents len: ", len(contents))
    print(contents)

    # find not existed chars in contents
    not_existed_chars = []
    for c in contents:
        if not c in tree_chars:
            not_existed_chars.append(c)
    print("not existed chars num: ", len(not_existed_chars))

    # add those no-existed chars to xml
    for id in range(len(not_existed_chars)):
        tag = not_existed_chars[id]

        code = char_to_unicode_str(tag)

        if code == "":
            print(tag, " not find code!")
            continue

        radical_elem = ET.SubElement(root, "RADICAL")
        radical_elem.set("ID", code)
        radical_elem.set("TAG", tag)

    # pretty xml
    prettyXml(root, '\t', '\n')
    tree.write(xml_save_path, encoding='utf-8')


if __name__ == '__main__':
    add_9300_chars_to_alldataset_xml()