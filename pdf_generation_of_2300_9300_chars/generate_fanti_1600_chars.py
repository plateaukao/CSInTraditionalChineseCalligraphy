# coding: utf-8
import os
import cv2
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import xml.etree.ElementTree as ET
import shutil


save_path = "../../../Data/Calligraphy_database/1600_fanti_image_chars"

path_9300_txt = "9300chars_cleaned.txt"
path_6931_txt = "6931chars_xml.txt"
path_1672_fanti_txt = "1672chars_fanti.txt"

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

font_path = "../data/simkai.ttf"

def generate_fanti_1600_chars():

    total_chars = []
    xml_chars = []
    fanti_chars = []

    # get total chars
    with open(path_9300_txt, "r") as f:
        for ch in f.readlines():
            total_chars.append(ch.strip())
    print("total num: ", len(total_chars))
    print(total_chars)

    # get 6931 chars in xml
    with open(path_6931_txt, "r") as f:
        for ch in f.readlines():
            xml_chars.append(ch.strip())
    print("xml chars num: ", len(xml_chars))
    print(xml_chars)

    # total chars not in xml chars
    for ch in total_chars:
        if ch not in xml_chars:
            fanti_chars.append(ch)

    # save to txt file
    with open(path_1672_fanti_txt, "w") as f:
        for i in range(len(fanti_chars)):
            ch = fanti_chars[i]

            if i == len(fanti_chars)-1:
                f.write(ch)
            else:
                f.write(ch + "\n")

    # generate fanti char images
    font = ImageFont.truetype(font_path, size=256)

    for i in range(len(fanti_chars)):
        ch = fanti_chars[i]

        img = Image.new("L", (256, 256), 255)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), ch, 0, font=font)
        img_path = os.path.join(save_path, "{}.png".format(ch))
        img.save(img_path, "PNG")



def extract_chars_from_xml():
    tree = ET.parse(xml_path)
    if tree is None:
        print("Tree is none!")
        return

    chars = []

    root = tree.getroot()
    for child in root:
        tag = child.attrib["TAG"].strip()
        if len(tag) == 1:
            chars.append(tag)


    with open(path_6931_txt, "w") as f:
        for i in range(len(chars)):
            ch = chars[i]

            if i == len(chars)-1:
                f.write(ch)
            else:
                f.write(ch + "\n")


if __name__ == '__main__':
    generate_fanti_1600_chars()
    # extract_chars_from_xml()