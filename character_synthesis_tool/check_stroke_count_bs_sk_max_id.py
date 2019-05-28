# coding: utf-8
import os
import xml.etree.ElementTree as ET
from utils.Functions import prettyXml

xml_path = "../../../Data/Calligraphy_database/XML_dataset/full_pure_dataset.xml"

def check_stroke_count_bs_sk_max_id():
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for child in root:
        tag = child.attrib["TAG"].strip()

        if len(tag) > 1:
            continue

        type_elems = child.findall("TYPE")
        if type_elems:
            if type_elems[0].text == "radical":
                continue

        sk_count = 0
        sk_count_elems = child.findall("STROKE_COUNT")
        if sk_count_elems:
            sk_count = int(sk_count_elems[0].text.strip())

        # print(sk_count)

        max_sk_id = 0
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                bs_sk_root_elems = bs_item.findall("STROKES")
                if bs_sk_root_elems:
                    bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                    for bs_sk_item in bs_sk_elems:
                        sk_id = int(bs_sk_item.attrib["ID"].strip())
                        if sk_id >= max_sk_id:
                            max_sk_id = sk_id

        if sk_count - 1 != max_sk_id:
            print("{} stroke order is error".format(tag))




if __name__ == '__main__':
    check_stroke_count_bs_sk_max_id()