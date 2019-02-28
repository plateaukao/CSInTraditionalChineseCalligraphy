# coding: utf-8
import os
import shutil
import xml.etree.ElementTree as ET
from utils.Functions import prettyXml


xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"

def stroke_order_count_check():
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    for child in root:
        tag = child.attrib["TAG"]
        if len(tag) > 1:
            continue
        # print(tag)
        stroke_count = 0
        stroke_count_elems = child.findall('STROKE_COUNT')
        if stroke_count_elems:
            stroke_count = int(stroke_count_elems[0].text)
            # print(stroke_count)

        stroke_orders = []
        stroke_order_elems = child.findall('STROKE_ORDER')
        if stroke_order_elems:
            s_order = stroke_order_elems[0].text

            if s_order != "" and s_order:
                stroke_orders = s_order.split("|")
            else:
                print('tag', tag, ' s_order is None')
        else:
            print("not find stroke order of ", tag)

        if len(stroke_orders) != stroke_count:
            print("tag: ", tag , 'not same storke count and storke order')


if __name__ == '__main__':
    stroke_order_count_check()

