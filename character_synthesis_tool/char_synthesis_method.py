# coding: utf-8
import os
import xml.etree.ElementTree as ET
import copy
import cv2


xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position_add_stroke_order.xml"
stroke_img_path = "../../../Data/Calligraphy_database/Stroke_pngs"
template_folder_path = "../../../Data/Calligraphy_database/Chars_tempalte_library"

from character_synthesis_tool.models import ChineseCharacter, BasicRadical, Stroke

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize

from character_synthesis_tool.template_matching_method import find_similar_basic_radicals_img_names_with_same_position_and_size, \
    find_similar_basic_radicals_img_names_with_same_size, find_similar_strokes_img_names_with_same_position_and_size, \
    find_similar_strokes_img_names_with_same_size

from character_synthesis_tool.generate_template_folders import get_all_basic_radical_type_list, \
get_char_bs_tag_and_stroke_ids_dict_list

# def character_synthesis(chars, root, template_folder_path, stroke_image_path):
#     if root is None or chars == "" or not os.path.exists(template_folder_path):
#         print("char or root or template folder path is none")
#         return
#
#     bs_threshold = 40
#     sk_threshold = 20
#
#     char_obj_list = []
#     for ch in chars:
#         ch_obj = char_from_xml_to_obj(ch, root)
#         char_obj_list.append(copy.deepcopy(ch_obj))
#
#     print("ch obj num: ", len(char_obj_list))
#
#     # all stroke image names
#     all_stroke_image_names = [f for f in os.listdir(stroke_image_path) if ".png" in f]
#
#     # reuslt
#     generated_results = []
#
#     for ch_obj in char_obj_list:
#
#         found_similar_stroke_ids = []
#
#         # find similar basic radical
#         similar_basic_radical_dict = {}     # {'0': {'肫_月_0.png': 31.400000000000002, '肪_月_0.png': 32.8}}
#         for bs_obj in ch_obj.basic_radicals:
#             bs_type = bs_obj.tag
#             print(bs_type)
#             bs_post = bs_obj.position
#             bs_type_path = os.path.join(template_folder_path, "BasicRadicals", bs_type)
#             if not os.path.exists(bs_type_path):
#                 print("bs type: {} not exist".format(bs_type))
#                 continue
#
#             # find bs with same position and size
#             similar_bs_same_post_and_size_list = find_similar_basic_radicals_img_names_with_same_position_and_size(bs_post, bs_type_path)
#             print("same post and size bs num:", len(similar_bs_same_post_and_size_list))
#
#
#             similar_bs_name_dict = {}   # temp_img_name: similar_dist
#
#             temp_img_names = [f for f in os.listdir(bs_type_path) if ".png" in f]
#             for name in temp_img_names:
#                 img_path = os.path.join(bs_type_path, name)
#                 img = cv2.imread(img_path, 0)
#                 rect = getSingleMaxBoundingBoxOfImage(img)
#
#                 # rule 1: same size and position
#                 similar_dist = calculate_ssim(bs_post, rect)
#                 print(similar_dist)
#
#                 if similar_dist < bs_threshold:
#                     similar_bs_name_dict[name] = similar_dist
#
#                     # add found stroke ids
#                     for sk_id in bs_obj.stroke_ids:
#                         if sk_id not in found_similar_stroke_ids:
#                             found_similar_stroke_ids.append(sk_id)
#             if len(similar_bs_name_dict) > 0:
#                 similar_basic_radical_dict[bs_obj.id] = similar_bs_name_dict.copy()
#         print(similar_basic_radical_dict)
#
#         # find the stroke names of these found bs
#         similar_bs_strokes_list_dict_result = {}       # {'0': [肫_storke_0.png, 肫_stroke_1.png ..], [肪_stroke_0.png, 肪_stroke_1.png...]}
#         if len(similar_basic_radical_dict) > 0:
#             for bs_id in similar_basic_radical_dict.keys():
#                 bs_name_ssim_dict = similar_basic_radical_dict[bs_id]
#
#                 bs_stroke_names_list = []
#                 for bs_img_name in bs_name_ssim_dict.keys():
#
#                     bs_sk_names_list = []
#
#                     similar_bs_char_tag = bs_img_name.split("_")[0].strip()
#                     similar_bs_bs_tag = bs_img_name.split("_")[1].strip()
#
#                     similar_bs_bs_sk_ids = get_stroke_ids_in_bs(root, similar_bs_char_tag, similar_bs_bs_tag)
#                     print(similar_bs_bs_sk_ids)
#
#                     # find these stroke images
#                     for sk_id in similar_bs_bs_sk_ids:
#                         for name in all_stroke_image_names:
#                             if "{}_".format(similar_bs_char_tag) in name and "_{}.png".format(sk_id) in name:
#                                 bs_sk_names_list.append(name)
#                                 break
#                     if len(bs_sk_names_list) > 0:
#                         bs_stroke_names_list.append(bs_sk_names_list.copy())
#                 similar_bs_strokes_list_dict_result[bs_id] = bs_stroke_names_list.copy()
#         print(similar_bs_strokes_list_dict_result)
#
#         # find similar strokes
#         unfound_stroke_ids = []
#         for sk_obj in ch_obj.strokes:
#             if int(sk_obj.id) not in found_similar_stroke_ids:
#                 unfound_stroke_ids.append(int(sk_obj.id))
#
#         print(unfound_stroke_ids)
#
#         similar_strokes_dict = {}   # {4: {'丐_4E10_2.png': 13.2, '乍_4E4D_3.png': 17.599999999999998, '上_4E0A_1.png': 15.199999999999996, '乾_4E7E_9.png': 10.799999999999997, '临_4E34_3.png': 19.6}, 5: {
#         for sk_id in unfound_stroke_ids:
#             sk_obj = None
#             for obj in ch_obj.strokes:
#                 if sk_id == int(obj.id):
#                     sk_obj = copy.deepcopy(obj)
#                     break
#             if sk_obj == None:
#                 continue
#             # find similar strokes
#             sk_post = sk_obj.position
#             sk_type = sk_obj.tag
#             sk_type_temp_path = os.path.join(template_folder_path, "Strokes", sk_type)
#             if not os.path.exists(sk_type_temp_path):
#                 print("no this type stroke in templates folder")
#                 continue
#             sk_temp_img_names = [f for f in os.listdir(sk_type_temp_path) if ".png" in f]
#
#             similar_sk_name_dict = {}   # name: similar distance
#             for name in sk_temp_img_names:
#                 sk_img_path = os.path.join(sk_type_temp_path, name)
#                 sk_img = cv2.imread(sk_img_path, 0)
#                 rect = getSingleMaxBoundingBoxOfImage(sk_img)
#
#                 similar_dist = calculate_ssim(sk_post, rect)
#
#                 similar_sk_name_dict[name] = similar_dist
#
#             # sorted this dict
#             similar_sk_name_dict_sorted = {}
#             min_dist = 10000000000000
#             for key in similar_sk_name_dict.keys():
#                 ssim = similar_sk_name_dict[key]
#
#                 if ssim < sk_threshold:
#                     similar_sk_name_dict_sorted[key] = ssim
#                 if ssim < min_dist:
#                     min_dist = ssim
#
#             # if not find stroke ,find the most similar stroke
#             for key in similar_sk_name_dict.keys():
#                 ssim = similar_sk_name_dict[key]
#                 if min_dist == ssim:
#                     similar_sk_name_dict_sorted[key] = ssim
#
#             similar_strokes_dict[sk_id] = similar_sk_name_dict_sorted.copy()
#         print("similar_strokes_dict: ", similar_strokes_dict)
#
#         # sort the similar strokes
#         similar_strokes_dict_result = {}
#         for sk_id in similar_strokes_dict.keys():
#
#             sk_name_list = []
#
#             sk_name_ssim_dict = similar_strokes_dict[sk_id]
#
#             sk_name_ssim_sorted_list = [(k, sk_name_ssim_dict[k]) for k in sorted(sk_name_ssim_dict, key=sk_name_ssim_dict.get)]
#
#             for k, v in sk_name_ssim_sorted_list:
#                 sk_name_list.append(k)
#
#             similar_strokes_dict_result[sk_id] = sk_name_list.copy()
#
#         print(similar_strokes_dict_result)
#
#         # merge image
#
#         ch_stroke_post_dict = {}
#         ch_similar_sk_id_img_name_dict = {}
#         for i in range(len(ch_obj.strokes)):
#             ch_stroke_post_dict[i] = ch_obj.strokes[i].position.copy()
#             ch_similar_sk_id_img_name_dict[i] = ""
#
#         # add found similar strokes
#
#         for sk_id in similar_strokes_dict_result.keys():
#             sk_name_list = similar_strokes_dict_result[sk_id]
#             if sk_id in ch_similar_sk_id_img_name_dict:
#                 ch_similar_sk_id_img_name_dict[sk_id] = sk_name_list[0]
#
#         print(ch_similar_sk_id_img_name_dict)
#
#         # add similar bs strokes to dict
#         for bs_id in similar_bs_strokes_list_dict_result.keys():
#             for bs_obj in ch_obj.basic_radicals:
#                 if bs_obj.id == bs_id:
#                     bs_stroke_ids = bs_obj.stroke_ids
#
#                     for i in range(len(bs_stroke_ids)):
#                         sk_id = bs_stroke_ids[i]
#                         if sk_id in ch_similar_sk_id_img_name_dict:
#                             ch_similar_sk_id_img_name_dict[sk_id] = similar_bs_strokes_list_dict_result[bs_id][0][i]
#         print(ch_similar_sk_id_img_name_dict)
#
#         bk = createBlankGrayscaleImageWithSize((500, 500))
#         offset_base = int(abs(500 - 256) / 2)
#
#         for sk_id in ch_similar_sk_id_img_name_dict:
#             # if sk_id != 6:
#             #     continue
#             img_name = ch_similar_sk_id_img_name_dict[sk_id]
#
#             sk_post = None
#             for sk_obj in ch_obj.strokes:
#                 if sk_obj.id == str(sk_id):
#                     sk_post = sk_obj.position.copy()
#                     break
#             if sk_post is None:
#                 continue
#             x0, y0, w0, h0 = sk_post[0], sk_post[1], sk_post[2], sk_post[3]
#
#             cent_x0 = int(x0 + w0 / 2)
#             cent_y0 = int(y0 + h0 / 2)
#
#             print(cent_x0, cent_y0)
#
#             img = cv2.imread(os.path.join(stroke_image_path, img_name), 0)
#             x, y, w, h = getSingleMaxBoundingBoxOfImage(img)
#
#
#             cent_x = int(x + w / 2)
#             cent_y = int(y + h / 2)
#
#             print(cent_x, cent_y)
#
#             offset_x = cent_x0 - cent_x + offset_base
#             offset_y = cent_y0 - cent_y + offset_base
#
#             # print(cent_x + offset_x, cent_y+offset_y)
#
#             for x in range(256):
#                 for y in range(256):
#                     if img[x][y] == 0:
#                         if x + offset_x < 0 or x + offset_x >= 500 or y + offset_y < 0 and y + offset_y >= 500 or \
#                                 x < 0 or x >= 500 or y < 0 or y >= 500:
#                             continue
#                         bk[x + offset_x][y + offset_y] = img[x][y]
#
#         generated_results.append(bk.copy())
#
#     return generated_results

def character_synthesis_new(chars, root, template_folder_path, stroke_image_path):
    if root is None or chars == "" or not os.path.exists(template_folder_path):
        print("char or root or template folder path is none")
        return

    bs_threshold = 40
    sk_threshold = 20

    char_obj_list = []
    for ch in chars:
        ch_obj = char_from_xml_to_obj(ch, root)
        char_obj_list.append(copy.deepcopy(ch_obj))

    print("ch obj num: ", len(char_obj_list))

    # all stroke image names
    all_stroke_image_names = [f for f in os.listdir(stroke_image_path) if ".png" in f]

    # reuslt
    generated_results = []

    for ch_obj in char_obj_list:

        found_similar_stroke_ids = []

        # find similar basic radical
        similar_basic_radical_dict = {}     # {'0': {'肫_月_0.png': 31.400000000000002, '肪_月_0.png': 32.8}}
        for bs_obj in ch_obj.basic_radicals:
            bs_type = bs_obj.tag
            print(bs_type)
            bs_post = bs_obj.position
            bs_type_path = os.path.join(template_folder_path, "BasicRadicals", bs_type)
            if not os.path.exists(bs_type_path):
                print("bs type: {} not exist".format(bs_type))
                continue

            # find bs with same position and size
            similar_bs_same_post_and_size_list = find_similar_basic_radicals_img_names_with_same_position_and_size(
                    bs_post, bs_type_path, threshold=10)
            print(similar_bs_same_post_and_size_list)
            print("same post and size bs num:", len(similar_bs_same_post_and_size_list))

            exit()

            if len(similar_bs_same_post_and_size_list) > 0:
                print("find same post and size bs")

                for sk_id_ in bs_obj.stroke_ids:
                    if sk_id_ not in found_similar_stroke_ids:
                        found_similar_stroke_ids.append(sk_id_)
                similar_basic_radical_dict[int(bs_obj.id)] = similar_bs_same_post_and_size_list.copy()
                continue

            # not find similar bs with same post and size, need to find bs with same size
            similar_bs_same_size_list = find_similar_basic_radicals_img_names_with_same_size(
                bs_post, bs_type_path, threshold=30)
            if len(similar_bs_same_size_list) > 0:
                print("find same size bs")

                for sk_id_ in bs_obj.stroke_ids:
                    if sk_id_ not in found_similar_stroke_ids:
                        found_similar_stroke_ids.append(sk_id_)

                similar_basic_radical_dict[int(bs_obj.id)] = similar_bs_same_size_list.copy()
                continue
        print(similar_basic_radical_dict)

        print("find stroke ids: ", found_similar_stroke_ids)

        # find the stroke names of these found bs
        similar_bs_strokes_list_dict_result = {}       # {'0': [[肫_storke_0.png, 肫_stroke_1.png ..], [肪_stroke_0.png, 肪_stroke_1.png...]]}
        if len(similar_basic_radical_dict) > 0:
            for bs_id in similar_basic_radical_dict.keys():

                bs_stroke_names_list = []
                bs_similar_bs_name_list = similar_basic_radical_dict[bs_id]
                for bs_img_name in bs_similar_bs_name_list:

                    bs_sk_names_list = []

                    similar_bs_char_tag = bs_img_name.split("_")[0].strip()
                    similar_bs_bs_tag = bs_img_name.split("_")[1].strip()

                    similar_bs_char_all_bs_type = get_all_basic_radical_type_list(root, similar_bs_char_tag)
                    print(similar_bs_char_all_bs_type)

                    similar_bs_sk_ids_list = get_char_bs_tag_and_stroke_ids_dict_list(root, similar_bs_char_tag)
                    print(similar_bs_sk_ids_list)

                    similar_bs_bs_sk_ids = []

                    for d in similar_bs_sk_ids_list:
                        key = list(d.keys())[0]
                        if similar_bs_bs_tag == key:
                            similar_bs_bs_sk_ids = d[key]

                    print("similar_bs_bs_sk_ids: ", similar_bs_bs_sk_ids)

                    # find these stroke images
                    for sk_id in similar_bs_bs_sk_ids:
                        for name in all_stroke_image_names:
                            if "{}_".format(similar_bs_char_tag) in name and "_{}.png".format(sk_id) in name:
                                bs_sk_names_list.append(name)
                                print("name:", name)
                                break
                    if len(bs_sk_names_list) > 0:
                        bs_stroke_names_list.append(bs_sk_names_list.copy())
                similar_bs_strokes_list_dict_result[bs_id] = bs_stroke_names_list.copy()
        print(similar_bs_strokes_list_dict_result)

        # find similar strokes
        unfound_stroke_ids = []
        for sk_obj in ch_obj.strokes:
            if int(sk_obj.id) not in found_similar_stroke_ids:
                unfound_stroke_ids.append(int(sk_obj.id))

        print("not found ids:", unfound_stroke_ids)

        similar_strokes_dict = {}   # {4: {'丐_4E10_2.png': 13.2, '乍_4E4D_3.png': 17.599999999999998, '上_4E0A_1.png': 15.199999999999996, '乾_4E7E_9.png': 10.799999999999997, '临_4E34_3.png': 19.6}, 5: {

        ch_similar_sk_id_img_name_dict = {}
        # init this dict
        for i in range(len(ch_obj.strokes)):
            ch_similar_sk_id_img_name_dict[i] = ""

        if len(similar_bs_strokes_list_dict_result) > 0:
            # this char can be synthezed by similar bs
            for bs_id in similar_bs_strokes_list_dict_result.keys():
                for bs_obj in ch_obj.basic_radicals:
                    if bs_obj.id == str(bs_id):
                        bs_stroke_ids = bs_obj.stroke_ids

                        for i in range(len(bs_stroke_ids)):
                            sk_id = bs_stroke_ids[i]
                            if sk_id in ch_similar_sk_id_img_name_dict:
                                ch_similar_sk_id_img_name_dict[sk_id] = similar_bs_strokes_list_dict_result[bs_id][0][i]
                        break
            print(ch_similar_sk_id_img_name_dict)

        for sk_id in unfound_stroke_ids:
            sk_obj = None
            for obj in ch_obj.strokes:
                if sk_id == int(obj.id):
                    sk_obj = copy.deepcopy(obj)
                    break
            if sk_obj == None:
                continue

            # find similar strokes
            sk_post = sk_obj.position
            sk_type = sk_obj.tag
            sk_type_temp_path = os.path.join(template_folder_path, "Strokes", sk_type)
            if not os.path.exists(sk_type_temp_path):
                print("no this type stroke in templates folder")
                continue

            similar_sk_same_post_and_size_list = find_similar_strokes_img_names_with_same_position_and_size(sk_post,
                                                    sk_type_temp_path, threshold=20)
            if len(similar_sk_same_post_and_size_list) > 0:
                print("find same post and size strokes")
                similar_strokes_dict[sk_id] = similar_sk_same_post_and_size_list.copy()
                ch_similar_sk_id_img_name_dict[sk_id] = similar_sk_same_post_and_size_list[0]
                continue

            # not find same post and size stroke, to find same size
            similar_sk_same_size_list = find_similar_strokes_img_names_with_same_size(sk_post,
                                                    sk_type_temp_path, threshold=30)
            if len(similar_sk_same_size_list) > 0:
                print("find same size strokes")
                similar_strokes_dict[sk_id] = similar_sk_same_size_list.copy()
                ch_similar_sk_id_img_name_dict[sk_id] = similar_sk_same_size_list[0]
                continue


        # merge image
        ch_stroke_post_dict = {}
        for i in range(len(ch_obj.strokes)):
            ch_stroke_post_dict[i] = ch_obj.strokes[i].position.copy()

        # add similar bs strokes to dict
        for bs_id in similar_bs_strokes_list_dict_result.keys():
            for bs_obj in ch_obj.basic_radicals:
                if bs_obj.id == bs_id:
                    bs_stroke_ids = bs_obj.stroke_ids

                    for i in range(len(bs_stroke_ids)):
                        sk_id = bs_stroke_ids[i]
                        if sk_id in ch_similar_sk_id_img_name_dict:
                            ch_similar_sk_id_img_name_dict[sk_id] = similar_bs_strokes_list_dict_result[bs_id][0][i]
        print(ch_similar_sk_id_img_name_dict)

        # merge image
        bk = createBlankGrayscaleImageWithSize((500, 500))
        offset_base = int(abs(500 - 256) / 2)

        for sk_id in ch_similar_sk_id_img_name_dict:
            # if sk_id != 6:
            #     continue
            img_name = ch_similar_sk_id_img_name_dict[sk_id]

            sk_post = None
            for sk_obj in ch_obj.strokes:
                if sk_obj.id == str(sk_id):
                    sk_post = sk_obj.position.copy()
                    break
            if sk_post is None:
                continue
            x0, y0, w0, h0 = sk_post[0], sk_post[1], sk_post[2], sk_post[3]

            cent_x0 = int(x0 + w0 / 2)
            cent_y0 = int(y0 + h0 / 2)

            img = cv2.imread(os.path.join(stroke_image_path, img_name), 0)
            x, y, w, h = getSingleMaxBoundingBoxOfImage(img)

            cent_x = int(x + w / 2)
            cent_y = int(y + h / 2)

            offset_x = cent_x0 - cent_x + offset_base
            offset_y = cent_y0 - cent_y + offset_base

            for x in range(256):
                for y in range(256):
                    if img[x][y] == 0:
                        if x + offset_x < 0 or x + offset_x >= 500 or y + offset_y < 0 and y + offset_y >= 500 or \
                                x < 0 or x >= 500 or y < 0 or y >= 500:
                            continue
                        bk[x + offset_x][y + offset_y] = img[x][y]
            print("show bk")
            cv2.imshow("{}".format(ch_obj.tag), bk)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        generated_results.append(bk.copy())

    return generated_results


def get_stroke_ids_in_bs(root, ch, bs_tag):
    if root is None or ch == "" or bs_tag == "":
        return []

    bs_sk_ids = []
    for child in root:
        tag = child.attrib["TAG"].strip()
        if ch != tag:
            continue

        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    b_tag = bs_item.attrib["TAG"]
                    if bs_tag != b_tag:
                        continue

                    sk_root_elems = bs_item.findall("STROKES")
                    if sk_root_elems:
                        sk_elems = sk_root_elems[0].findall("STROKE")
                        if sk_elems:
                            for sk_item in sk_elems:
                                sk_id = int(sk_item.attrib["ID"].strip())
                                bs_sk_ids.append(sk_id)
                            break

    return bs_sk_ids


def calculate_ssim(bs_post, img_rect, alpha=0.8):
    x0, y0, w0, h0 = bs_post[0], bs_post[1], bs_post[2], bs_post[3]
    x, y, w, h = img_rect[0], img_rect[1], img_rect[2], img_rect[3]

    # calculate the size similar distance
    size_dist = abs(w - w0) + abs(h - h0)

    # location distance
    location_dist = abs(x - x0) + abs(y - y0)

    similar_dist = alpha * size_dist + (1 - alpha) * location_dist

    return similar_dist


def char_from_xml_to_obj(ch, root):
    if ch == "" or root is None:
        print("ch or root is none")
        return

    ch_obj = ChineseCharacter()

    # search for ch in xml
    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue
        # parse xml to get chinese character obj

        # basic radical
        bs_obj_list = []
        sk_post_dict = {}
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                bs_id = bs_item.attrib['ID']
                bs_post = bs_item.attrib['POSITION'].replace("(", "").replace(")", "").split(",")
                bs_post = [int(s.strip()) for s in bs_post]
                bs_tag = bs_item.attrib['TAG']
                bs_sk_ids = []
                sk_root_elems = bs_item.findall("STROKES")
                if sk_root_elems:
                    sk_elems = sk_root_elems[0].findall("STROKE")
                    for sk_item in sk_elems:
                        sk_id = sk_item.attrib['ID'].strip()
                        sk_post = sk_item.attrib['POSITION'].strip().replace("(", "").replace(")", "").split(",")
                        sk_post = [int(s.strip()) for s in sk_post]

                        sk_post_dict[sk_id] = sk_post.copy()
                        bs_sk_ids.append(int(sk_id))

                bs_obj = BasicRadical()
                bs_obj.id = bs_id
                bs_obj.tag = bs_tag
                bs_obj.position = bs_post.copy()
                bs_obj.stroke_ids = bs_sk_ids.copy()

                bs_obj_list.append(bs_obj)

        sk_obj_list = []
        sk_order_str = ""
        sk_order_elems = child.findall("STROKE_ORDER")
        if sk_order_elems:
            sk_order_str = sk_order_elems[0].text.strip()
        sk_order_list = sk_order_str.split("|")
        for sk_id in range(len(sk_order_list)):
            sk_type = sk_order_list[sk_id]
            sk_post = sk_post_dict[str(sk_id)].copy()

            sk_obj = Stroke()
            sk_obj.id = str(sk_id)
            sk_obj.tag = sk_type
            sk_obj.position = sk_post

            sk_obj_list.append(sk_obj)

        # to ch obj
        ch_obj.tag = tag
        ch_obj.basic_radicals = bs_obj_list.copy()
        ch_obj.strokes = sk_obj_list.copy()
        break

    return ch_obj


if __name__ == '__main__':
    # character_synthesis()
    ch = "他"
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # ch_obj = char_from_xml_to_obj(ch, root)
    # print(ch_obj.basic_radicals)

    chars = "他"

    results = character_synthesis_new(chars, root, template_folder_path, stroke_img_path)


