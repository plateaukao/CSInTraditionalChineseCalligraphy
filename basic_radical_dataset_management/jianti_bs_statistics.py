# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET

jianti_xml_path = "../../../Data/Characters/jian_fan_merge_basic_radical_stroke_complement.xml"
fanti_xml_path = "../../../Data/Characters/fanti_2.xml"


def jianti_bs_statistics():

    bs_set = set()

    jianti_chars = []

    tree = ET.parse(jianti_xml_path)
    root = tree.getroot()

    for i in range(len(root)):
        radical_elem = root[i]
        print(radical_elem)
        tag = radical_elem.attrib["TAG"].strip()
        jianti_chars.append(tag)

        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_id = bs_item.attrib["ID"].strip()
                    bs_tag = bs_item.attrib["TAG"].strip()
                    bs_set.add(bs_tag)
    bs_set_not_single = set()
    for s in bs_set:
        if s not in jianti_chars:
            bs_set_not_single.add(s)
        if len(s) > 1:
            bs_set_not_single.add(s)
    print(bs_set_not_single)

    # parse fanti bs
    fanti_chars = []
    bs_set = set()
    tree = ET.parse(fanti_xml_path)
    root = tree.getroot()

    print(len(root))

    for i in range(len(root)):
        radical_elem = root[i]

        if radical_elem.tag == "BASIC_RADICALS":
            continue

        tag = radical_elem.attrib["TAG"].strip()
        fanti_chars.append(tag)

        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_id = bs_item.attrib["ID"].strip()
                    bs_tag = bs_item.attrib["TAG"].strip()
                    bs_set.add(bs_tag)
    bs_set_not_single = set()
    for s in bs_set:
        if s not in fanti_chars and s not in jianti_chars:
            bs_set_not_single.add(s)
        if len(s) > 1:
            bs_set_not_single.add(s)
    print(bs_set_not_single)


def fanti_bs_statistics():
    bs_set = set()

    chars = []

    tree = ET.parse(fanti_xml_path)
    root = tree.getroot()

    print(len(root))

    for i in range(len(root)):
        radical_elem = root[i]

        if radical_elem.tag == "BASIC_RADICALS":
            continue

        tag = radical_elem.attrib["TAG"].strip()
        chars.append(tag)

        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_id = bs_item.attrib["ID"].strip()
                    bs_tag = bs_item.attrib["TAG"].strip()
                    bs_set.add(bs_tag)
    bs_set_not_single = set()
    for s in bs_set:
        if s not in chars:
            bs_set_not_single.add(s)
    print(bs_set_not_single)



if __name__ == '__main__':
    jianti_bs_statistics()
    # fanti_bs_statistics()

    # tree = ET.parse(fanti_xml_path)
    # root = tree.getroot()
    # for i in range(len(root)):
    #     print(root[i].tag)

        # if root[i].tag == "RADICALS"

