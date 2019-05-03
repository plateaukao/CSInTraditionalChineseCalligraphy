# coding: utf-8
import os
import xml.etree.ElementTree as ET

from utils.Functions import getSingleMaxBoundingBoxOfImage, prettyXml

from pdf_generation_of_2300_9300_chars.convert_char_to_unicode_test import chars_to_unicode_list


def add_9300_chars_to_xml_dataset():
    path_xml = "9300dataset.xml"
    path_9300_chars = "9300chars.txt"

    chars = ""
    with open(path_9300_chars, "r") as f:
        chars = f.readline()

    print("chars len: ", len(chars))

    codes = chars_to_unicode_list(chars)
    print("codes len: ", len(codes))

    root = ET.Element("RADICALS")
    tree = ET.ElementTree(root)

    for i in range(len(codes)):
        char = chars[i]
        code = codes[i]

        element = ET.SubElement(root, "RADICAL")
        element.set("ID", code)
        element.set("TAG", char)



    # pretty xml
    prettyXml(root, '\t', '\n')
    tree.write(path_xml, encoding='utf-8')







if __name__ == '__main__':
    add_9300_chars_to_xml_dataset()