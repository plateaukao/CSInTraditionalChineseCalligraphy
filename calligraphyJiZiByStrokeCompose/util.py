# coding: utf-8
import os
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
from calligraphyJiZiByStrokeCompose.stroke_image import StrokeImage, BasicRadicalImage
from calligraphyJiZiByStrokeCompose.basicradical import BasicRadical, Stroke
import xml.etree.ElementTree as ET
import ast
import cv2
import timeit

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize
from calligraphyJiZiByStrokeCompose.model import ChineseCharacter, BasicRadcial, Stroke


def render_generated_image(char_obj, select_strokes_dict):
    size = 400
    image = createBlankGrayscaleImageWithSize((size, size))
    offset_base = int(abs(size - 256) / 2)

    for key in select_strokes_dict.keys():

        # get real position of stroke
        print(char_obj.strokes)
        real_post = char_obj.strokes[int(key)].position

        cent_x0 = int(real_post[0] + real_post[2] / 2)
        cent_y0 = int(real_post[1] + real_post[3] / 2)

        # get position of similar stroke
        stroke_path = select_strokes_dict[key]
        print(stroke_path)
        stroke_img = cv2.imread(stroke_path, 0)
        stroke_rect = getSingleMaxBoundingBoxOfImage(stroke_img)
        if stroke_rect is None:
            continue

        for x in range(stroke_rect[2]):
            for y in range(stroke_rect[3]):
                if stroke_img[stroke_rect[1] + y][stroke_rect[0] + x] == 0:
                    image[cent_y0 - int(stroke_rect[3] / 2) + offset_base + y][
                        cent_x0 - int(stroke_rect[2] / 2) + offset_base + x] = \
                        stroke_img[stroke_rect[1] + y][stroke_rect[0] + x]

    return image


def query_similar_basic_radicals_and_strokes(basic_radicals_dataset, strokes_dataset, char_info_list):
    """
    Find similar basic radicals and strokes.

    :param basic_radicals_dataset:
    :param strokes_dataset:
    :param char_info_list:
    :return:
    """
    if basic_radicals_dataset is None or strokes_dataset is None:
        print("Basic radical dataset or stroke dataset should not be None!")
        return
    if char_info_list is None or len(char_info_list) == 0:
        print("Char info list should not be None!")
        return

    # iterative search char infor
    similar_chars = []
    for ch_id in range(len(char_info_list)):
        ch_obj = char_info_list[ch_id]

        similar_basic_radicals = {}
        similar_strokes = {}

        found_stroke_id = []    # record the found stroke id in basic radical search action.

        # search similar basic radicals.
        ch_radicals = ch_obj.basic_radicals

        if len(ch_radicals) > 0:
            # this char has basic radical
            for bs_id in range(len(ch_radicals)):
                bs_obj = ch_radicals[bs_id]
                bs_obj_post = bs_obj.position.replace("[", "").replace("]", "").replace(" ", "").split(",")
                bs_obj_post = [int(p) for p in bs_obj_post]
                bs_obj_tag = bs_obj.tag
                bs_obj_id = bs_obj.id

                similar_bss = []

                # find all library basic radical objects
                if not bs_obj_tag in basic_radicals_dataset:
                    print(bs_obj_tag, " not in 775 basic radicals")
                else:
                    basic_radicals_lib = basic_radicals_dataset[bs_obj_tag]
                    print("Basic radicals lib len: ", len(basic_radicals_lib))

                    for bsl in basic_radicals_lib:

                        # get bsl obj path
                        path_ = bsl.image_path
                        bsl_tag = path_.split("/")[-1].replace(".png", "").split("_")[0]
                        bsl_id = path_.split("/")[-1].replace(".png", "").split("_")[2]

                        x, y, w, h = getSingleMaxBoundingBoxOfImage(bsl.image_bytes)

                        sim_bs_dict = {}

                        # rule1
                        if abs(x - bs_obj_post[0]) <= 5 and abs(y - bs_obj_post[1]) <= 5 and abs(w - bs_obj_post[2]) <= 5 and abs(h - bs_obj_post[3]) <= 5:
                            sim_bs_dict["path"] = bsl.image_path

                            # target bs obj strokes id
                            print("bsl tag: ", bsl_tag)
                            targ_bs_obj_list = query_char_info_from_chars_list([bsl_tag])
                            if len(targ_bs_obj_list) == 0:
                                print("template bs objs not found!")
                            else:
                                targ_bs_obj = targ_bs_obj_list[0]

                                for bs_ in targ_bs_obj.basic_radicals:
                                    if bs_.id == bsl_id:
                                        sim_bs_dict["strokes_id"] = bs_.strokes_id

                                print("sim strokes id: ", sim_bs_dict["strokes_id"])

                            sim_bs_dict["position"] = (x, y, w, h)

                            similar_bss.append(sim_bs_dict)

                similar_basic_radicals[bs_obj_id] = similar_bss

        print(similar_basic_radicals)

        # identify the found strokes in found basic radical
        for bs_id in similar_basic_radicals.keys():
            if len(similar_basic_radicals[bs_id]) > 0:
                # this basic radical found similar basic radicals, add stroke ids of this bs to found strokes list

                for bs in ch_obj.basic_radicals:
                    if bs_id == bs.id:
                      found_stroke_id += bs.strokes_id
        found_stroke_id = [int(f) for f in found_stroke_id]
        print(found_stroke_id)

        # find similar strokes for those not found strokes
        for sk in ch_obj.strokes:
            if sk.id in found_stroke_id:
                continue
            # find similar stroke
            post_ = sk.position
            id_ = sk.id
            type_ = sk.tag

            sm_strokes = find_similar_strokes(type_, post_, strokes_dataset)

            # sorted similar strokes based on the similarity
            sm_strokes = sorted_strokes_based_on_similarity(post_, sm_strokes)

            similar_strokes[id_] = sm_strokes

        similar_chars.append((similar_basic_radicals, similar_strokes))

    return similar_chars





def recompose_chars(chars_info_list, similar_chars, char_root_path="/Users/liupeng/Documents/Data/Calligraphy_database/Chars_775", size=400):
    """
    Recompose chars to 400 x 400 image from 256 x 256 to avoid out of size of image (256, 256)
    :param chars_info_list:
    :param similar_chars:
    :param char_root_path:
    :return:
    """
    generated_images = []

    if len(similar_chars) == 0:
        return generated_images

    for sc in similar_chars:
        similar_basic_radicals, similar_strokes = sc

        ch_id = similar_chars.index(sc)
        ch_obj = chars_info_list[ch_id]
        ch_strokes_list = ch_obj.strokes

        print("process: ", ch_obj.tag)

        # get basic radicals info and his strokes images
        similar_bs_dict = {}
        for bs_id in similar_basic_radicals.keys():

            bs_obj = []
            for bs_ in similar_basic_radicals[bs_id]:

                bs_obj_dict = {}

                path_ = bs_["path"]
                strokes_id_ = bs_["strokes_id"]
                postion_ = bs_["position"]

                print("path: ", path_)
                print("strokes id: ", strokes_id_)

                char_tag = path_.split('/')[-1].replace(".png", "").split("_")[0]
                char_path_ = os.path.join(char_root_path, char_tag, "strokes")
                stroke_img_names = [f for f in os.listdir(char_path_) if ".png" in f]

                stroke_img_dict = {}
                for s_id in strokes_id_:
                    for nm in stroke_img_names:
                        if "_" + str(s_id) + "." in nm:
                            stroke_img_dict[s_id] = os.path.join(char_path_, nm)
                            break

                bs_obj_dict["path"] = path_
                bs_obj_dict["strokes"] = stroke_img_dict
                bs_obj_dict["position"] = postion_
                bs_obj.append(bs_obj_dict)

            if bs_obj != []:
                similar_bs_dict[bs_id] = bs_obj

        print(similar_bs_dict)

        # recompose basic radicals and strokes
        bk = createBlankGrayscaleImageWithSize((size, size))
        offset_base = int(abs(size - 256) / 2)

        # load basic radicals stroke images and center alignment
        for bs_id in similar_bs_dict.keys():
            for bs_obj in similar_bs_dict[bs_id]:

                bk_bs = createBlankGrayscaleImageWithSize((size, size))  # merge strokes of this basic radical together to get single connected component

                stroke_objs = bs_obj["strokes"]
                post_ = bs_obj["position"]

                cent_x0 = int(post_[0] + post_[2] / 2)
                cent_y0 = int(post_[1] + post_[3] / 2)

                for s_id in stroke_objs.keys():
                    path_ = stroke_objs[s_id]

                    img_ = cv2.imread(path_, 0)

                    for x in range(img_.shape[0]):
                        for y in range(img_.shape[1]):
                            if img_[x][y] == 0:
                                bk_bs[x+offset_base][y+offset_base] = 0

                x, y, w, h = getSingleMaxBoundingBoxOfImage(bk_bs)

                cent_x = int(x + w / 2)
                cent_y = int(y + h / 2)

                offset_x = cent_x0 - cent_x + offset_base
                offset_y = cent_y0 - cent_y + offset_base

                for x in range(bk_bs.shape[0]):
                    for y in range(bk_bs.shape[1]):
                        if bk_bs[x][y] == 0:
                            if x+offset_x < 0 or x+offset_x >= 400 or y+offset_y < 0 and y+offset_y >= 400 or \
                                    x < 0 or x >= 400 or y < 0 or y >= 400:
                                continue
                            bk[x + offset_x][y + offset_y] = bk_bs[x][y]

                break

        # load stroke images
        for s_id in similar_strokes.keys():

            # get template stroke position
            print(s_id)

            real_post = None
            for stk_obj in ch_strokes_list:
                if s_id == stk_obj.id:
                    real_post = stk_obj.position
                    break

            if real_post == None:
                print("Not find temp position!")
                continue

            cent_x0 = int(real_post[0] + real_post[2] / 2)
            cent_y0 = int(real_post[1] + real_post[3] / 2)

            # path_ = similar_strokes[s_id][0]   # use the most match stroke
            path_ = find_most_match_stroke(real_post, similar_strokes[s_id])

            img_ = cv2.imread(path_, 0)
            rect_ = getSingleMaxBoundingBoxOfImage(img_)

            for x_ in range(rect_[2]):
                for y_ in range(rect_[3]):
                    if img_[rect_[1] + y_][rect_[0] + x_] == 0:
                        bk[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
                            img_[rect_[1] + y_][rect_[0] + x_]


        generated_images.append(bk)
    return generated_images


def sorted_strokes_based_on_similarity(position, paths, alpha=0.8):
    x0, y0, w0, h0 = position

    # similar distance:  ssim = alpha * size_distance + (1-alpha) * location_distance
    ssim_distance_dict = {}

    for i in range(len(paths)):
        p_ = paths[i]
        if p_ == "":
            continue

        img_ = cv2.imread(p_, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)

        # calculate the size similar distance
        size_dist = abs(w - w0) + abs(h - h0)

        # calcluate the location similar distance
        location_dist = abs(x - x0) + abs(y - y0)

        similar_dist = alpha * size_dist + (1 - alpha) * location_dist
        ssim_distance_dict[i] = similar_dist

    # sort the size and location similar distance
    ssim_distance_dict_sorted = [(k, ssim_distance_dict[k]) for k in
                                 sorted(ssim_distance_dict, key=ssim_distance_dict.get)]

    new_paths = []
    for item in ssim_distance_dict_sorted:
        new_paths.append(paths[item[0]])

    return new_paths


def find_most_match_stroke(position, paths, alpha=0.8):
    """
    Find the most match stroke
    :param position:
    :param paths:
    :return:
    """
    x0, y0, w0, h0 = position

    # similar distance:  ssim = alpha * size_distance + (1-alpha) * location_distance
    ssim_distance_dict = {}

    for i in range(len(paths)):
        p_ = paths[i]
        if p_ == "":
            continue

        img_ = cv2.imread(p_, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)

        # calculate the size similar distance
        size_dist = abs(w - w0) + abs(h - h0)

        # calcluate the location similar distance
        location_dist = abs(x - x0) + abs(y - y0)

        similar_dist = alpha * size_dist + (1 - alpha) * location_dist
        ssim_distance_dict[i] = similar_dist

    # sort the size and location similar distance
    ssim_distance_dict_sorted = [(k, ssim_distance_dict[k]) for k in sorted(ssim_distance_dict, key=ssim_distance_dict.get)]

    most_similar_stroke_id = ssim_distance_dict_sorted[0][0]
    print("most ssim distance: ", ssim_distance_dict_sorted[0][1])

    return paths[most_similar_stroke_id]


def find_similar_strokes(type, position, strokes_dataset):
    """
    Find similar strokes based on the type, position and strokes dataset.
    :param type:
    :param position:
    :param strokes_dataset:
    :return:
    """
    similar_strokes = []

    THRESHOLD_POSITION = 10
    THRESHOLD_SIZE = 15
    THRESHOLD_CONDITION = 1.88

    x = position[0]
    y = position[1]
    w = position[2]
    h = position[3]

    center_x = int(x + w / 2)
    center_y = int(y + h / 2)

    strokes_same_post_and_size = []
    strokes_same_size = []

    sorted_condition = {}
    for i in range(len(strokes_dataset[type])):
        stroke_obj = strokes_dataset[type][i]
        img_ = stroke_obj.image_bytes
        x0, y0, w0, h0 = getSingleMaxBoundingBoxOfImage(img_)

        center_x0 = int(x0 + w0 / 2)
        center_y0 = int(y0 + h0 / 2)

        # calcuate the sorted condition
        val = abs((w - w0) / w0 * 1.) + abs((h - h0) / h0 * 1.) + abs((w * h - w0 * h0) / (w0 * h0) * 1.)
        sorted_condition[i] = val

        # Rule 1: almost same the postion and size
        if abs(center_x - center_x0) <= THRESHOLD_POSITION and abs(center_y - center_y0) <= THRESHOLD_POSITION and \
            abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_post_and_size.append(stroke_obj.image_path)

    if len(strokes_same_post_and_size) > 0:
        # find the strokes with same position and size
        similar_strokes += strokes_same_post_and_size
        return similar_strokes
    else:
        print("Not find strokes with same position and size!")

    # Rule 2: Find strokes with same size
    if len(sorted_condition) == 0:
        print("Sorted condition is null!")

    sorted_condition_sorted = sorted(sorted_condition.items(), key=lambda x: x[1])
    print(sorted_condition_sorted)
    for s in sorted_condition_sorted:
        if s[1] > THRESHOLD_CONDITION:
            break
        strokes_same_size.append(strokes_dataset[type][s[0]].image_path)

    if len(strokes_same_size) > 0:
        similar_strokes += strokes_same_size
    else:
        print("Not find same size strokes")

    return similar_strokes


def query_char_info_from_chars_list(chars, xml_path="../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"):
    """
    Query the char info list.
    :param chars:
    :param xml_path:
    :return:
    """
    if chars is None or len(chars) == 0:
        return []

    # load radical data
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return

    root = tree.getroot()
    print("root len:", len(root))

    char_info_list = []

    for ch in chars:
        ch_obj = query_char_info_from_char(ch, root)
        char_info_list.append(ch_obj)

    return char_info_list


def query_char_info_from_char(char, root):
    if char == '':
        return []
    if root is None or len(root) <= 0:
        print('Root is None!')
        return []

    char_info_obj = None

    tag = ""
    u_code = ""
    stroke_orders = []
    stroke_position = []
    basic_radicals = []
    strokes = []

    for child in root:

        ch = child.attrib["TAG"].strip()
        if len(ch) > 1 or ch != char:
            continue

        # tag
        tag = ch

        # unicode
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

        if len(stroke_orders) != len(stroke_position):
            print(tag, " storke order and stroke position not same length!")
        else:
            for id_ in range(len(stroke_orders)):
                stk_tag = stroke_orders[id_]
                stk_post = stroke_position[id_]
                stk_id = id_

                stk_obj = Stroke(id=stk_id, tag=stk_tag, path="", position=stk_post)
                strokes.append(stk_obj)

        # basic radicals
        basic_radicals_elems = child.findall("BASIC_RADICALS")
        if basic_radicals_elems:
            bs_elems = basic_radicals_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs in bs_elems:
                    bs_id = bs.attrib["ID"]
                    bs_tag = bs.attrib["TAG"]
                    bs_post = bs.attrib["POSITION"]

                    # basic radical object list
                    bs_strokes_id = []

                    bs_strokes_elems = bs.findall("STROKES")
                    if bs_strokes_elems:
                        bs_stk_elems = bs_strokes_elems[0].findall("STROKE")
                        if bs_stk_elems:
                            for bs_stk in bs_stk_elems:
                                bs_stroke_id = bs_stk.attrib["ID"]
                                bs_strokes_id.append(bs_stroke_id)

                    bs_obj = BasicRadcial(id=bs_id, tag=bs_tag, path="", position=bs_post, strokes_id=bs_strokes_id)
                    print("bs_id: ", bs_id, " ", bs_strokes_id)

                    basic_radicals.append(bs_obj)

        # strokes
        break

    char_info_obj = ChineseCharacter(id=u_code, tag=tag, basic_radicals=basic_radicals, strokes=strokes)
    return char_info_obj


def load_stroke_library_dataset(path="../../../Data/Calligraphy_database/char_generate_lib/strokes dataset"):
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


def load_basic_radicals_library_dataset(path="../../../Data/Calligraphy_database/char_generate_lib/basic radicals dataset"):
    if path == "" or not os.path.exists(path):
        print("Basic radicals library path is None!")
        return
    type_names = [f for f in os.listdir(path) if "." not in f]
    print("Type name num: ", len(type_names))

    dataset = {}
    count = 0
    for tn in type_names:
        tn_path = os.path.join(path, tn)

        img_obj_list = []
        img_names = [os.path.join(tn_path, f) for f in os.listdir(tn_path) if ".png" in f]

        for img_name in img_names:
            img_ = cv2.imread(img_name, 0)
            basic_radical_obj = BasicRadicalImage(img_name, img_)
            img_obj_list.append(basic_radical_obj)
            count += 1
        dataset[tn] = img_obj_list
    print("load image num: ", count)
    return dataset


# def query_char_info_from_chars_list(chars, xml_path):
#     """
#     Query the char info list.
#     :param chars:
#     :param xml_path:
#     :return:
#     """
#     if chars is None or len(chars) == 0:
#         return []
#
#     # load radical data
#     tree = ET.parse(xml_path)
#     if tree is None:
#         print("tree is none!")
#         return
#
#     root = tree.getroot()
#     print("root len:", len(root))
#
#     char_info_list = []
#
#     for ch in chars:
#         ch_obj = query_char_info_from_char(ch, root)
#         char_info_list.append(ch_obj)
#
#     return char_info_list
#
#
# def query_char_info_from_char(char, root):
#     if char == '':
#         return []
#     if root is None or len(root) <= 0:
#         print('Root is None!')
#         return []
#
#     char_info_obj = None
#
#     tag = ""
#     u_code = ""
#     stroke_orders = []
#     stroke_position = []
#     basic_radicals = []
#     strokes = []
#
#     for child in root:
#
#         ch = child.attrib["TAG"].strip()
#         if len(ch) > 1 or ch != char:
#             continue
#
#         # tag
#         tag = ch
#
#         # unicode
#         u_code = child.attrib["ID"]
#
#         # stroke order
#         stroke_order_elems = child.findall('STROKE_ORDER')
#         if stroke_order_elems:
#             s_order = stroke_order_elems[0].text
#             stroke_orders = s_order.split("|")
#         else:
#             print("not find stroke order of ", tag)
#
#         # stroke position
#         s_post_elems = child.findall('STROKES_POSITION')
#         if s_post_elems:
#             ss_post_elems = s_post_elems[0].findall('STROKE_POSITION')
#             if ss_post_elems:
#                 for elem in ss_post_elems:
#                     stroke_position.append(ast.literal_eval(elem.text))
#         else:
#             print("Not find storke position of ", tag)
#
#         # basic radicals
#         basic_radicals_elems = child.findall("BASIC_RADICALS")
#         if basic_radicals_elems:
#             bs_elems = basic_radicals_elems[0].findall("BASIC_RADICAL")
#             if bs_elems:
#                 for bs in bs_elems:
#                     bs_id = bs.attrib["ID"]
#                     bs_tag = bs.attrib["TAG"]
#                     bs_post = bs.attrib["POSITION"]
#
#                     # basic radical object list
#                     bs_strokes = []
#
#                     bs_strokes_elems = bs.findall("STROKES")
#                     if bs_strokes_elems:
#                         bs_stk_elems = bs_strokes_elems[0].findall("STROKE")
#                         if bs_stk_elems:
#                             for bs_stk in bs_stk_elems:
#                                 bs_stroke_tag = bs_stk.attrib["TAG"]
#                                 bs_stroke_post = bs_stk.text
#
#                                 bs_stroke_obj = Stroke(id=bs_stroke_tag, tag=bs_stroke_tag, position=bs_stroke_post)
#
#                                 bs_strokes.append(bs_stroke_obj)
#
#                     bs_obj = BasicRadical(id=bs_id, tag=bs_tag, position=bs_post, strokes=bs_strokes)
#
#                     basic_radicals.append(bs_obj)
#
#         # strokes
#         break
#
#     char_info_obj = ChineseCharacter(tag=tag, u_code=u_code, stroke_orders=stroke_orders, stroke_position=stroke_position, basic_radicals=basic_radicals, strokes=strokes)
#     return char_info_obj


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


# def render_generated_image(char_info_list, char_target_strokes_list, generated_result_index_list, char_id=0):
#     """
#     Re-render generated result image with char id, stroke id, and stroke image id.
#     :param char_target_strokes_list:
#     :param generated_result_index_list: [][]
#     :param char_id:
#     :param stroke_id:
#     :param stroke_image_id:
#     :return:
#     """
#     if len(char_target_strokes_list) == 0:
#         print('Char target stroke list is None!')
#         return
#
#     ch_obj = char_info_list[char_id]
#
#     bk = createBlankGrayscaleImageWithSize((400, 400))
#
#     # get the target strokes info of char based on the char_id.
#     target_strokes_list = char_target_strokes_list[char_id]  # [stroke_id][stroke_names]
#     target_strokes_index_list = generated_result_index_list[char_id]  # [stroke_img_id]
#
#     strokes_temp_imgs = []
#     for i in range(len(target_strokes_list)):
#         stroke_imgs_ = target_strokes_list[i]
#         stroke_img_path = stroke_imgs_[target_strokes_index_list[i]]
#
#         img_ = cv2.imread(stroke_img_path, 0)
#         img_ = cv2.resize(img_, (256, 256))
#         rect_ = getSingleMaxBoundingBoxOfImage(img_)
#
#         # resize stroke template image
#         s_temp_img = createBlankGrayscaleImageWithSize((400, 400))
#         # s_temp_img[72: 72 + 256, 72: 72 + 256] = img_
#
#         strokes_temp_imgs.append(s_temp_img)
#
#         cent_x0 = int(ch_obj.stroke_position[i][0] + ch_obj.stroke_position[i][2] / 2)
#         cent_y0 = int(ch_obj.stroke_position[i][1] + ch_obj.stroke_position[i][3] / 2)
#
#         # only copy the valid pixels
#         for x_ in range(rect_[2]):
#             for y_ in range(rect_[3]):
#                 if img_[rect_[1] + y_][rect_[0] + x_] == 0:
#                     bk[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
#                         img_[rect_[1] + y_][rect_[0] + x_]
#                     s_temp_img[cent_y0 - int(rect_[3] / 2) + 72 + y_][cent_x0 - int(rect_[2] / 2) + 72 + x_] = \
#                         img_[rect_[1] + y_][rect_[0] + x_]
#         strokes_temp_imgs.append(s_temp_img)
#     return bk, strokes_temp_imgs


if __name__ == '__main__':
    dataset = load_stroke_library_dataset()
    print(dataset)