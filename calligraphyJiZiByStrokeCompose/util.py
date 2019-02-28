# coding: utf-8
import os
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
import xml.etree.ElementTree as ET
import ast
import cv2

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize


def query_taget_strokes(type, position, library_path="../../../Data/Stroke_recomposed_tool/strokes dataset"):
    """
    Query target strokes from library based on the stroke type and position(x, y, w, h).
    :param type:
    :param position:
    :param library_path:
    :return:
    """
    if type == "":
        print("type should not be None!")
        return
    lib_path = os.path.join(library_path, type)

    file_names = [f for f in os.listdir(lib_path) if ".png" in f]
    print("lib file num: ", len(file_names))

    # search target strokes with position info (x, y, w, h) and return the target image paths
    target_strokes_path = []

    # stroke images
    all_stroke_imgs = []
    for fn in file_names:
        img_path = os.path.join(lib_path, fn)
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (256, 256))
        all_stroke_imgs.append(img)
    print('all stroke images len: ', len(all_stroke_imgs))

    # find target strokes with almost same position and size
    center_x0 = int(position[0] + position[2] / 2)
    center_y0 = int(position[1] + position[3] / 2)

    w0 = position[2]
    h0 = position[3]

    strokes_same_post_and_size = [] # almost same position and size
    strokes_same_size = []  # almost same only size

    THRESHOLD_POSITION = 10
    THRESHOLD_SIZE = 10

    for i in range(len(all_stroke_imgs)):
        img_ = all_stroke_imgs[i]
        rect_ = getSingleMaxBoundingBoxOfImage(img_)
        center_x = int(rect_[0] + rect_[2] / 2)
        center_y = int(rect_[1] + rect_[3] / 2)

        w = rect_[2]
        h = rect_[3]

        # Rule 1: almost same the position and size
        if abs(center_x - center_x0) <= THRESHOLD_POSITION and abs(center_y - center_y0) <= THRESHOLD_POSITION and \
            abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_post_and_size.append(os.path.join(lib_path, file_names[i]))
            continue

        # Rule 2: almost same the size
        if abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_size.append(os.path.join(lib_path, file_names[i]))
            continue

    # return target strokes
    if len(strokes_same_post_and_size) > 0:
        target_strokes_path += strokes_same_post_and_size
        return target_strokes_path
    else:
        print("Not find same postion and size strokes")

    if len(strokes_same_size) > 0:
        target_strokes_path += strokes_same_size
        return target_strokes_path
    else:
        print("Not find same size strokes")

    print('Not find target stroke')
    return target_strokes_path


def query_char_info(input):
    # remove invalid characters in input
    input = input.replace(' ', '').replace('\n', '').replace('\t', '')

    if input == "":
        print("Input content should not be None!")
        return []

    # reterival xml to find character info
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"
    # load radical data
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return []

    root = tree.getroot()
    print("root len:", len(root))

    char_info_list = []
    for ins in input:
        tag = ""
        u_code = ""
        stroke_orders = []
        stroke_position = []

        for child in root:
            ch = child.attrib["TAG"]
            if ch == ins:
                tag = ch
                u_code = child.attrib["ID"]

                # stroke order
                stroke_order_elems = child.findall('STROKE_ORDER')
                if stroke_order_elems:
                    s_order = stroke_order_elems[0].text
                    stroke_orders = s_order.split("|")
                else:
                    print("not find stroke order of ", tag)

                # stroke position
                s_post_elems = child.findall('STROKES_POSITION')
                if s_post_elems:
                    ss_post_elems = s_post_elems[0].findall('STROKE_POSITION')
                    if ss_post_elems:
                        for elem in ss_post_elems:
                            stroke_position.append(ast.literal_eval(elem.text))
                else:
                    print("Not find storke position of ", tag)

                break

        if tag == "" and u_code == "":
            print("Not find this char: ", ins)
            continue
        if len(stroke_orders) != len(stroke_position):
            print(tag, "Stroke order and position are not same length!")
            continue

        # create ChineseCharacter object
        cc_obj = ChineseCharacter(tag, u_code, stroke_orders, stroke_position)
        char_info_list.append(cc_obj)
    return char_info_list


def query_char_target_strokes(char_info_list):
    char_target_strokes_list = []
    for cc in char_info_list:
        print(cc.tag, cc.u_code, cc.stroke_orders, cc.stroke_position)
        target_strokes = []
        for i in range(len(cc.stroke_orders)):
            targ_strokes_ = query_taget_strokes(cc.stroke_orders[i], cc.stroke_position[i])
            target_strokes.append(targ_strokes_)
            print('target stroken num: ', len(targ_strokes_))
            if len(targ_strokes_) == 0:
                print(cc.tag, "stroke ", i, "not fond target strokes")

        char_target_strokes_list.append(target_strokes)
    return char_target_strokes_list


def stroke_recompose(char_info_list, char_target_strokes_list):
    generated_result = []

    for i in range(len(char_info_list)):
        ch_obj = char_info_list[i]
        ch_stroke_imgs = char_target_strokes_list[i]
        bk = createBlankGrayscaleImageWithSize((400, 400))

        # merge all stroke with center alignment
        if len(ch_stroke_imgs) == ch_obj.stroke_orders:
            print("imgs of stroke are same length")

        for j in range(len(ch_stroke_imgs)):
            if len(ch_stroke_imgs[j]) > 0:
                img_path = ch_stroke_imgs[j][0]
                img_ = cv2.imread(img_path, 0)
                img_ = cv2.resize(img_, (256, 256))
                rect_ = getSingleMaxBoundingBoxOfImage(img_)

                cent_x0 = int(ch_obj.stroke_position[j][0] + ch_obj.stroke_position[j][2] / 2)
                cent_y0 = int(ch_obj.stroke_position[j][1] + ch_obj.stroke_position[j][3] / 2)

                # only copy the valid pixels
                for x_ in range(rect_[2]):
                    for y_ in range(rect_[3]):
                        if img_[rect_[1] + y_][rect_[0] + x_] == 0:
                            bk[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                            img_[rect_[1] + y_][rect_[0] + x_]
        generated_result.append(bk)

    return generated_result
