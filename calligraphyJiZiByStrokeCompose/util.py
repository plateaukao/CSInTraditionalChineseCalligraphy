# coding: utf-8
import os
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
from calligraphyJiZiByStrokeCompose.stroke_image import StrokeImage
import xml.etree.ElementTree as ET
import ast
import cv2
import timeit

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize


def load_stroke_library_dataset(path="../../../Data/Stroke_recomposed_tool/strokes dataset"):
    if path == "":
        print('Stroke library path should not be None!')
        return
    if not os.path.exists(path):
        print("Stroke path is not existed!")
        return
    type_names = [f for f in os.listdir(path) if '.DS_Store' not in f]
    print('type name num: ', len(type_names))

    dataset = {}
    count = 0
    for tn in type_names:
        path_ = os.path.join(path, tn)

        img_obj_list = []
        img_names = [os.path.join(path_, f) for f in os.listdir(path_) if '.png' in f]

        for p in img_names:
            img_ = cv2.imread(p, 0)
            img_ = cv2.resize(img_, (256, 256))
            stroke_obj = StrokeImage(p, img_)
            img_obj_list.append(stroke_obj)
            count += 1
        dataset[tn] = img_obj_list

    print('load image num: ', count)
    return dataset


def query_target_strokes_by_postion_size(position, stroke_obj_list):
    if position is None or stroke_obj_list is None or len(stroke_obj_list) == 0:
        print("Position or stroke object list should not be None!")
        return

    target_strokes_path = []

    # find target strokes with almost same position and size
    center_x0 = int(position[0] + position[2] / 2)
    center_y0 = int(position[1] + position[3] / 2)

    w0 = position[2]
    h0 = position[3]

    strokes_same_post_and_size = []  # almost same position and size
    strokes_same_size = []  # almost same only size

    THRESHOLD_POSITION = 10
    THRESHOLD_SIZE = 15
    THRESHOLD_CONDITION = 1.88

    sorted_condition = {}
    for i in range(len(stroke_obj_list)):
        stroke_obj = stroke_obj_list[i]
        img_ = stroke_obj.image_bytes

        if img_ is None:
            print("stroke obj is None")
            continue

        rect_ = getSingleMaxBoundingBoxOfImage(img_)

        center_x = int(rect_[0] + rect_[2] / 2)
        center_y = int(rect_[1] + rect_[3] / 2)

        w = rect_[2]
        h = rect_[3]

        # calcuate the sorted condition
        val = abs((w - w0) / w0 * 1.) + abs((h - h0) / h0 * 1.) + abs((w * h - w0 * h0) / (w0 * h0) * 1.)
        sorted_condition[i] = val

        # Rule 1: almost same the position and size
        if abs(center_x - center_x0) <= THRESHOLD_POSITION and abs(center_y - center_y0) <= THRESHOLD_POSITION and \
                abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_post_and_size.append(stroke_obj.image_path)
            continue

    if len(strokes_same_post_and_size) > 0:
        target_strokes_path += strokes_same_post_and_size
        return target_strokes_path
    else:
        print("Not find same postion and size strokes")

    # Rule2: Almost same the position and size
    if len(sorted_condition) == 0:
        print("Sorted condition is null!")

    sorted_condition_sorted = sorted(sorted_condition.items(), key=lambda x: x[1])
    print(sorted_condition_sorted)
    for s in sorted_condition_sorted:
        if s[1] > THRESHOLD_CONDITION:
            break
        strokes_same_size.append(stroke_obj_list[s[0]].image_path)

    # return target strokes
    if len(strokes_same_size) > 0:
        target_strokes_path += strokes_same_size
        # return target_strokes_path
    else:
        print("Not find same size strokes")
    return target_strokes_path


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

    s_time = timeit.default_timer()
    type_path = os.path.join(library_path, type)
    file_names = [f for f in os.listdir(type_path) if ".png" in f]
    print("lib file num: ", len(file_names))
    print('List stroke image file name time: ', timeit.default_timer()-s_time)

    # search target strokes with position info (x, y, w, h) and return the target image paths
    target_strokes_path = []
    s_time = timeit.default_timer()
    # stroke images
    all_stroke_imgs = []
    for fn in file_names:
        img_path = os.path.join(type_path, fn)
        img = cv2.imread(img_path, 0)
        img = cv2.resize(img, (256, 256))
        all_stroke_imgs.append(img)
    print('all stroke images len: ', len(all_stroke_imgs))
    print('list all stroke image of one target-type time: ', timeit.default_timer() - s_time)

    # find target strokes with almost same position and size
    center_x0 = int(position[0] + position[2] / 2)
    center_y0 = int(position[1] + position[3] / 2)

    s_time = timeit.default_timer()

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
            strokes_same_post_and_size.append(os.path.join(type_path, file_names[i]))
            continue

        # Rule 2: almost same the size
        if abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_size.append(os.path.join(type_path, file_names[i]))
            continue

    print('find target strokes time: ', timeit.default_timer() - s_time)

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


def query_char_info_from_chars_list(chars):
    if chars is None or len(chars) == 0:
        return []

    # reterival xml to find character info
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"

    # load radical data
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return

    root = tree.getroot()
    print("root len:", len(root))

    char_info_list = []
    for child in root:

        tag = ""
        u_code = ""
        stroke_orders = []
        stroke_position = []

        ch = child.attrib["TAG"].strip()
        if len(ch) > 1:
            continue

        if ch in chars:
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

        if tag == "" and u_code == "":
            # print("Not find this char: ", ch)
            continue
        if len(stroke_orders) != len(stroke_position):
            print(tag, "Stroke order and position are not same length!")
            continue

        # create ChineseCharacter object
        cc_obj = ChineseCharacter(tag, u_code, stroke_orders, stroke_position)
        char_info_list.append(cc_obj)
    return char_info_list


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

        target_strokes = []
        for i in range(len(cc.stroke_orders)):
            targ_strokes_ = query_taget_strokes(cc.stroke_orders[i], cc.stroke_position[i])
            target_strokes.append(targ_strokes_)
            if len(targ_strokes_) == 0:
                print(cc.tag, "stroke ", i, "not fond target strokes")

        char_target_strokes_list.append(target_strokes)
    return char_target_strokes_list


def query_char_target_stroke_by_dataset(dataset, char_info_list):
    if dataset is None or char_info_list is None:
        print("Dataset or char info list should be not None!")
        return

    char_target_strokes_list = []
    for cc in char_info_list:
        target_strokes = []
        for i in range(len(cc.stroke_orders)):
            lib_stroke_obj_list = dataset[cc.stroke_orders[i]]
            print("this type stroke num: ", len(lib_stroke_obj_list))
            targ_strokes_ = query_target_strokes_by_postion_size(cc.stroke_position[i], lib_stroke_obj_list)
            target_strokes.append(targ_strokes_)
            if len(targ_strokes_) == 0:
                print(cc.tag, "stroke ", i, "not fond target strokes")

        char_target_strokes_list.append(target_strokes)
    return char_target_strokes_list


def stroke_recompose(char_info_list, char_target_strokes_list):
    generated_result = []
    generated_strokes_result = []
    generated_result_index_list = []

    for i in range(len(char_info_list)):
        ch_obj = char_info_list[i]
        ch_stroke_imgs = char_target_strokes_list[i]
        bk = createBlankGrayscaleImageWithSize((400, 400))

        # strokes template
        strokes_temp_imgs = []
        stroke_img_index = []

        # merge all stroke with center alignment
        if len(ch_stroke_imgs) == ch_obj.stroke_orders:
            print("imgs of stroke are same length")

        for j in range(len(ch_stroke_imgs)):
            if len(ch_stroke_imgs[j]) > 0:
                img_path = ch_stroke_imgs[j][0]
                stroke_img_index.append(0)
                img_ = cv2.imread(img_path, 0)
                img_ = cv2.resize(img_, (256, 256))
                rect_ = getSingleMaxBoundingBoxOfImage(img_)

                # resize stroke template image
                s_temp_img = createBlankGrayscaleImageWithSize((400, 400))
                # s_temp_img[72: 72+256, 72: 72+256] = img_


                cent_x0 = int(ch_obj.stroke_position[j][0] + ch_obj.stroke_position[j][2] / 2)
                cent_y0 = int(ch_obj.stroke_position[j][1] + ch_obj.stroke_position[j][3] / 2)

                # only copy the valid pixels
                for x_ in range(rect_[2]):
                    for y_ in range(rect_[3]):
                        if img_[rect_[1] + y_][rect_[0] + x_] == 0:
                            bk[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                            img_[rect_[1] + y_][rect_[0] + x_]
                            s_temp_img[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                                img_[rect_[1] + y_][rect_[0] + x_]
                strokes_temp_imgs.append(s_temp_img)
        generated_result.append(bk)
        generated_strokes_result.append(strokes_temp_imgs)
        generated_result_index_list.append(stroke_img_index)

    return generated_result, generated_strokes_result, generated_result_index_list


def render_generated_image(char_info_list, char_target_strokes_list, generated_result_index_list, char_id=0):
    """
    Re-render generated result image with char id, stroke id, and stroke image id.
    :param char_target_strokes_list:
    :param generated_result_index_list: [][]
    :param char_id:
    :param stroke_id:
    :param stroke_image_id:
    :return:
    """
    if len(char_target_strokes_list) == 0:
        print('Char target stroke list is None!')
        return

    ch_obj = char_info_list[char_id]

    bk = createBlankGrayscaleImageWithSize((400, 400))

    # get the target strokes info of char based on the char_id.
    target_strokes_list = char_target_strokes_list[char_id]  # [stroke_id][stroke_names]
    target_strokes_index_list = generated_result_index_list[char_id]  # [stroke_img_id]

    strokes_temp_imgs = []
    for i in range(len(target_strokes_list)):
        stroke_imgs_ = target_strokes_list[i]
        stroke_img_path = stroke_imgs_[target_strokes_index_list[i]]

        img_ = cv2.imread(stroke_img_path, 0)
        img_ = cv2.resize(img_, (256, 256))
        rect_ = getSingleMaxBoundingBoxOfImage(img_)

        # resize stroke template image
        s_temp_img = createBlankGrayscaleImageWithSize((400, 400))
        # s_temp_img[72: 72 + 256, 72: 72 + 256] = img_

        strokes_temp_imgs.append(s_temp_img)

        cent_x0 = int(ch_obj.stroke_position[i][0] + ch_obj.stroke_position[i][2] / 2)
        cent_y0 = int(ch_obj.stroke_position[i][1] + ch_obj.stroke_position[i][3] / 2)

        # only copy the valid pixels
        for x_ in range(rect_[2]):
            for y_ in range(rect_[3]):
                if img_[rect_[1] + y_][rect_[0] + x_] == 0:
                    bk[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                        img_[rect_[1] + y_][rect_[0] + x_]
                    s_temp_img[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                        img_[rect_[1] + y_][rect_[0] + x_]
        strokes_temp_imgs.append(s_temp_img)
    return bk, strokes_temp_imgs


if __name__ == '__main__':
    dataset = load_stroke_library_dataset()
    print(dataset)