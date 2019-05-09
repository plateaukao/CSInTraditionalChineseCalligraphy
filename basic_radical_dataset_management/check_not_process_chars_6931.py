# coding: utf-8
import os
import xml.etree.ElementTree as ET
import shutil

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"
chars_path = "../../../Data/Calligraphy_database/Chars"
not_process_chars_path = "../../../Data/Calligraphy_database/Chars_not_processed"


def check_not_process_chars_6931():
    chars_names = [f for f in os.listdir(chars_path) if "." not in f]
    print("chars num: ", len(chars_names))

    # not process chars
    not_processed_chars = []

    # parse xml data to find not processed chars
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is None!")
        return

    root = tree.getroot()

    for i in range(len(root)):
        elem = root[i]

        tag = elem.attrib["TAG"].strip()

        if len(tag) > 1:
            continue

        # check existing basic radicals or not
        if len(elem.findall("BASIC_RADICALS")) == 0:
            not_processed_chars.append(tag)
        else:
            print(tag)

    print("not processed chars num: ", len(not_processed_chars))
    print(not_processed_chars)

    for nc in not_processed_chars:
        src_path = os.path.join(chars_path, nc)
        if not os.path.exists(src_path):
            continue

        tag_path = os.path.join(not_process_chars_path, nc)

        shutil.copytree(src_path, tag_path)






if __name__ == '__main__':
    check_not_process_chars_6931()