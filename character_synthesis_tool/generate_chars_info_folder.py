# coding: utf-8
import os
import cv2
import shutil
import xml.etree.ElementTree as ET

chars_path = "../../../Data/Calligraphy_database/Chars_dataset"
xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids.xml"
strokes_png_path = "../../../Data/Calligraphy_database/Stroke_pngs"
chars_png_path = "../../../Data/Calligraphy_database/Chars_pngs"
def generate_chars_info_folder():

    chars_names = [f for f in os.listdir(chars_path) if "." not in f]

    strokes_png_names = [f for f in os.listdir(strokes_png_path) if ".png" in f]
    chars_png_names = [f for f in os.listdir(chars_png_path) if ".png" in f]

    tree = ET.parse(xml_path)
    root = tree.getroot()

    not_process_chars = []
    for child in root:
        tag = child.attrib["TAG"].strip()
        if len(tag) > 1:
            continue

        if tag not in chars_names:
            not_process_chars.append(tag.strip())

    # make folder and copy char image and stroke images
    for ch in not_process_chars:
        if not os.path.exists(os.path.join(chars_path, ch)):
            os.mkdir(os.path.join(chars_path, ch))
            os.mkdir(os.path.join(chars_path, ch, "basic radicals"))
            os.mkdir(os.path.join(chars_path, ch, "strokes"))

            # find single char png
            char_png_name = ""
            for cpn in chars_png_names:
                if ch in cpn:
                    char_png_name = cpn
                    break
            shutil.copy2(os.path.join(chars_png_path, char_png_name), os.path.join(chars_path, ch))

            # find all strokes png
            sk_png_names = []
            for skn in strokes_png_names:
                if ch in skn:
                    sk_png_names.append(skn)

            for spn in sk_png_names:
                shutil.copy2(os.path.join(strokes_png_path, spn), os.path.join(chars_path, "strokes", ch))






if __name__ == '__main__':
    generate_chars_info_folder()