# coding: utf-8
import cv2
import os
from xml.dom import minidom
import xml.etree.ElementTree as ET


def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


def getSingleMaxBoundingBoxOfImage(image):
    """
    Calculate the coordinates(x, y, w, h) of single maximizing bounding rectangle boxing of grayscale image
    of character, in order to using this bounding box to select the region of character.
    :param image: grayscale image of character.
    :return: coordinates(x, y, w, h) of single maximizing bounding boxing.
    """
    if image is None:
        return None

    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]

    # moments
    im2, contours, hierarchy = cv2.findContours(image, 1, 2)

    minx = WIDTH
    miny = HEIGHT
    maxx = 0
    maxy = 0
    # Bounding box
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])

        if w > 0.95 * WIDTH and h > 0.95 * HEIGHT:
            continue
        minx = min(x, minx);
        miny = min(y, miny)
        maxx = max(x + w, maxx);
        maxy = max(y + h, maxy)

    return minx, miny, maxx - minx, maxy - miny


def add_stroke_postion_infor_to_radical_xml():
    radical_path = "../../Data/Characters/radicals.xml"

    stroke_png_path = "../../Data/Strokes_png"

    # load radical data
    tree = ET.parse(radical_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    # load stroke png names
    stroke_png_names = []
    file_list = os.listdir(stroke_png_path)
    for fl in file_list:
        if ".png" in fl:
            stroke_png_names.append(fl)
    print("stroke png len:", len(stroke_png_names))

    # find tag in radical
    for i in range(len(root)):
        element = root[i]
        ch = element.attrib["TAG"]

        stroke_img_names = []

        for j in range(len(stroke_png_names)):
            if ch in stroke_png_names[j]:
                stroke_img_names.append(stroke_png_names[j])
        if len(stroke_img_names) == 0:
            print("not find strokes")
            continue
        stroke_img_names_sorted = []
        for k in range(len(stroke_img_names)):
            for m in range(len(stroke_img_names)):
                if "_" + str(k) + ".png" in stroke_img_names[m]:
                    stroke_img_names_sorted.append(stroke_img_names[m])
                    break
        # print(stroke_img_names_sorted)

        strokes_post_element = ET.Element("STROKES_POSITION")

        for j in range(len(stroke_img_names_sorted)):
            sk_path = os.path.join(stroke_png_path, stroke_img_names_sorted[j])
            img_ = cv2.imread(sk_path, 0)
            if img_ is None:
                print("Can not open stroke img !")
                continue

            x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)
            print(x, y, w, h)
            sk_post_elem = ET.Element("STROKE_POSITION")
            sk_post_elem.set("TAG", "STROKE_" + str(j+1))
            sk_post_elem.text = str([x, y, w, h])
            strokes_post_element.append(sk_post_elem)
        element.append(strokes_post_element)

        # if i == 1000:
        #     break

    prettyXml(root, '\t', '\n')
    tree.write('test.xml', encoding='utf-8')


if __name__ == '__main__':
    add_stroke_postion_infor_to_radical_xml()
