# coding: utf-8
import os
import cv2
import shutil
import xml.etree.ElementTree as ET
from utils.Functions import getSingleMaxBoundingBoxOfImage, prettyXml


xml_path = "./img_merge_test/add_bs_sk_position_test_result_add_sk_ids.xml"
save_path = "./img_merge_test/add_bs_sk_position_test_result_add_sk_ids_result.xml"

strokes_png_path = "../../../Data/Calligraphy_database/Stroke_pngs"

chars_txt_path = "chars.txt"



def add_bs_stroke_position_to_xml():

    chars_in_svg = []
    with open(chars_txt_path, "r") as f:
       for ch in f.readlines():
           chars_in_svg.append(ch.strip())

    strokes_names = [f for f in os.listdir(strokes_png_path) if ".png" in f]
    print("stroke names: ", len(strokes_names))

    tree = ET.parse(xml_path)
    root = tree.getroot()

    count = 0
    for child in root:

        count += 1
        print(count)

        tag = child.attrib["TAG"].strip()
        if len(tag) > 1:
            continue
        print(tag)

        if tag not in chars_in_svg:
            continue

        # find all stroke names of this char
        sk_names = []
        for skn in strokes_names:
            if tag in skn:
                sk_names.append(skn)

        # find basic radicals
        basic_radicals_root_elems = child.findall("BASIC_RADICALS")
        if basic_radicals_root_elems:
            bs_elems = basic_radicals_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    min_x1 = min_y1 = 1000000000
                    max_w = max_h = -1

                    max_x2 = max_y2 = -1

                    sk_root_elems = bs_item.findall("STROKES")
                    if sk_root_elems:
                        sk_elems = sk_root_elems[0].findall("STROKE")
                        for sk_item in sk_elems:
                            sk_id = sk_item.attrib["ID"].strip()
                            sk_nm = ""
                            for s in sk_names:
                                if "_{}.png".format(sk_id) in s:
                                    sk_nm = s
                                    break
                            # print(sk_nm)
                            sk_img_path = os.path.join(strokes_png_path, sk_nm)
                            # print(sk_img_path)
                            sk_img = cv2.imread(sk_img_path, 0)
                            rect = getSingleMaxBoundingBoxOfImage(sk_img)

                            sk_item.set("POSITION", str(rect))

                            min_x1 = min(min_x1, rect[0])
                            min_y1 = min(min_y1, rect[1])

                            max_x2 = max(max_x2, rect[0] + rect[2])
                            max_y2 = max(max_y2, rect[1] + rect[3])

                    bs_item.set("POSITION", str((min_x1, min_y1, max_x2-min_x1, max_y2-min_y1)))

    # pretty xml
    prettyXml(root, '\t', '\n')
    tree.write(save_path, encoding='utf-8')


if __name__ == '__main__':
    add_bs_stroke_position_to_xml()