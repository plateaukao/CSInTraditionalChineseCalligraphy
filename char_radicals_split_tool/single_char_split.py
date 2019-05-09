# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET
import shutil

from utils.Functions import getAllMiniBoundingBoxesOfImage, getConnectedComponentsOfGrayScale, \
    createBlankGrayscaleImageWithSize, getSingleMaxBoundingBoxOfImage


def single_char_split():
    root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp"
    save_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_single_char"
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

    tree = ET.parse(xml_path)
    if tree is None:
        print("Tree is none!")
        return

    root = tree.getroot()

    # file path
    file_names = [f for f in os.listdir(root_path) if "." not in f]
    print("files num: ", len(file_names))


    for i in range(len(file_names)):
        fn = file_names[i]

        fn_struct = get_structure_info(root, fn)
        print(fn_struct)

        if fn_struct == "Single Character":

            # copy char path to save path
            if not os.path.exists(os.path.join(save_path, fn)):
                # shutil.copytree(os.path.join(root_path, fn), os.path.join(save_path, fn))
                shutil.move(os.path.join(root_path, fn), os.path.join(save_path, fn))

            # open char image
            img_names = [f for f in os.listdir(os.path.join(save_path, fn)) if ".png" in f]
            if len(img_names) == 0:
                print("root path no image ")
                continue

            img = cv2.imread(os.path.join(save_path, fn, img_names[0]), 0)

            radical_name = img_names[0].replace(".png", "") + "_0_" + fn

            radical_path = os.path.join(save_path, fn, "basic radicals", radical_name)
            if not os.path.exists(radical_path):
                os.mkdir(radical_path)
            cv2.imwrite(os.path.join(save_path, fn, "basic radicals", "{}.png".format(radical_name)), img)

            # move strokes to radicals
            sk_names = [f for f in os.listdir(os.path.join(save_path, fn, "strokes")) if ".png" in f]
            for sn in sk_names:
                shutil.copy2(os.path.join(save_path, fn, "strokes", sn), os.path.join(radical_path))




def get_structure_info(root, char):
    if root is None or char == "":
        print("root or char is none!")
        return ""

    for i in range(len(root)):
        elem = root[i]
        tag = elem.attrib["TAG"].strip()
        if tag != char:
            continue

        struct_info = ""
        struct_elems = elem.findall("STRUCTURE")
        if struct_elems:
            struct_info = struct_elems[0].text
        return struct_info


def merge_two_images(bk, img):
    if bk is None or img is None:
        print("bk or img is none!")
        return
    if bk.shape != img.shape:
        print("two images are not same shape")
        return
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] == 0:
                bk[y][x] = 0

    return bk


if __name__ == '__main__':
    single_char_split()