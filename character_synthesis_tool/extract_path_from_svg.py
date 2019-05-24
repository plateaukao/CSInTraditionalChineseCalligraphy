# coding: utf-8
import os
import cv2
import shutil
import xml.etree.ElementTree as ET

xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids.xml"

svg_path = "../../../Data/Calligraphy_database/Chars_svg_files"

chars_path = "../../../Data/Calligraphy_database/Chars_dataset"


def extract_paths_from_svg():
    chars_names = [f.strip() for f in os.listdir(chars_path) if "." not in f]

    svg_names = [f.split("_")[0].strip() for f in os.listdir(svg_path) if ".svg" in f]

    xml_chars = []
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for item in root:
        tag = item.attrib["TAG"].strip()

        if len(tag) > 1:
            continue

        xml_chars.append(tag.strip())

    # find not process chars
    no_processed_chars = []

    for ch in xml_chars:
        if ch not in chars_names and ch in svg_names:
            no_processed_chars.append(ch)

    print(no_processed_chars)
    print(len(no_processed_chars))

    # extract path from each svg file
    for ch in no_processed_chars:
        if not os.path.exists(os.path.join(chars_path, ch)):
            os.mkdir(os.path.join(chars_path, ch))
            os.mkdir(os.path.join(chars_path, ch, "basic radicals"))
            os.mkdir(os.path.join(chars_path, ch, "strokes"))



if __name__ == '__main__':
    # extract_paths_from_svg()

    svg_names = [f.split("_")[0].strip() for f in os.listdir(svg_path) if ".svg" in f]

    chars = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for item in root:
        tag = item.attrib["TAG"].strip()
        if len(tag) > 1:
            continue

        if tag in svg_names:
            chars.append(tag)

    print(chars)