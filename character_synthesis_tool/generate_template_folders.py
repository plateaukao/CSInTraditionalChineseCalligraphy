# coding: utf-8
import os
import xml.etree.ElementTree as ET
from utils.Functions import createBlankGrayscaleImageWithSize
import cv2
import shutil


xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position_add_stroke_order.xml"
stroke_img_path = "../../../Data/Calligraphy_database/Stroke_pngs"
template_folder_path = "../../../Data/Calligraphy_database/Chars_tempalte_library"


def generate_template_folders(chars, xml_path, stroke_image_path, template_folder_path):
    if chars == "":
        return

    if not os.path.exists(template_folder_path):
        os.mkdir(template_folder_path)
        os.mkdir(os.path.join(template_folder_path, "Strokes"))
        os.mkdir(os.path.join(template_folder_path, "BasicRadicals"))

    stroke_lib_root_path = os.path.join(template_folder_path, "Strokes")
    bs_lib_root_path = os.path.join(template_folder_path, "BasicRadicals")

    # all stroke images in template_folder_path
    all_stroke_img_names = [f for f in os.listdir(stroke_image_path) if ".png" in f]

    tree = ET.parse(xml_path)
    root = tree.getroot()

    # get all stroke types in these chars
    all_stroke_type_list = get_all_stroke_type_list(root, chars)
    print(all_stroke_type_list)
    print(len(all_stroke_type_list))

    # create folder to strokes
    for sk_type in all_stroke_type_list:
        if not os.path.exists(os.path.join(stroke_lib_root_path, sk_type)):
            os.mkdir(os.path.join(stroke_lib_root_path, sk_type))

    # get all bs types in these chars
    all_bs_type_list = get_all_basic_radical_type_list(root, chars)
    print(all_bs_type_list)

    # create folder to bs
    for bs_type in all_bs_type_list:
        if not os.path.exists(os.path.join(bs_lib_root_path, bs_type)):
            os.mkdir(os.path.join(bs_lib_root_path, bs_type))

    # process each char and generate stroke library
    for ch in chars:
        # search all stroke images of this char
        ch_sk_img_names = []
        for name in all_stroke_img_names:
            if ch in name:
                ch_sk_img_names.append(name)
        print(ch_sk_img_names)

        if len(ch_sk_img_names) > 0:
            ch_sk_order_list = get_stroke_order_list(root, ch)
            for sk_id in range(len(ch_sk_order_list)):
                sk_type = ch_sk_order_list[sk_id].strip()
                sk_img_name = ""
                for name in ch_sk_img_names:
                    if "_{}.png".format(sk_id) in name:
                        sk_img_name = name
                        break
                if sk_img_name != "":
                    print(sk_img_name)
                    shutil.copy2(os.path.join(stroke_image_path, sk_img_name), os.path.join(stroke_lib_root_path, sk_type, sk_img_name))

    print("Strokes processed!")
    # process each char and generate basic radical library
    for ch in chars:
        char_bs_tag_stroke_ids_dict_list = get_char_bs_tag_and_stroke_ids_dict_list(root, ch)
        print(char_bs_tag_stroke_ids_dict_list)

        char_bs_images = merge_strokes_to_basic_radical_img(ch, char_bs_tag_stroke_ids_dict_list, stroke_image_path)

        for img_id in range(len(char_bs_images)):
            bs_img = char_bs_images[img_id]

            bs_sk_ids_dict = char_bs_tag_stroke_ids_dict_list[img_id]
            bs_tag = list(bs_sk_ids_dict.keys())[0]

            cv2.imwrite(os.path.join(bs_lib_root_path, bs_tag, "{}_{}_{}.png".format(ch, bs_tag, img_id)), bs_img)









    # for ch in chars:
    #     ch_sk_order_list = get_stroke_order_list(root, ch)
    #     print(ch_sk_order_list)
    #
    #     if len(ch_sk_order_list) == 0:
    #         print("{} not find stroke order".format(ch))
    #         continue



def get_all_stroke_type_list(root, chars):
    if root is None or chars is None or len(chars) == 0:
        return []

    all_stroke_type_list = []
    for ch in chars:
        ch_sk_order_list = get_stroke_order_list(root, ch)

        for ch_sk_item in ch_sk_order_list:
            if ch_sk_item not in all_stroke_type_list:
                all_stroke_type_list.append(ch_sk_item)

    return all_stroke_type_list


def get_all_basic_radical_type_list(root, chars):
    if root is None or chars is None or len(chars) == 0:
        return []

    all_bs_type_list = []

    for ch in chars:
        bs_type_list = get_basic_radical_tag_list(root, ch)
        if bs_type_list is None:
            continue
        for type in bs_type_list:
            if type not in all_bs_type_list:
                all_bs_type_list.append(type)

    # check second time to find sub-basic radicals
    sub_bs_tag_list = []
    for type in all_bs_type_list:
        bs_type_list = get_basic_radical_tag_list(root, type)
        if bs_type_list is None:
            continue
        for type in bs_type_list:
            if type not in all_bs_type_list:
                sub_bs_tag_list.append(type)

    if len(sub_bs_tag_list) > 0:
        for sub_bs in sub_bs_tag_list:
            all_bs_type_list.append(sub_bs)
    return all_bs_type_list


def get_stroke_count(root, ch):
    if root is None or ch == "":
        return "0"

    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        sk_count_elems = child.findall("STROKE_COUNT")
        if sk_count_elems:
            return str(sk_count_elems[0].text)

    return "0"

def get_bs_count_of_char(root, ch):
    if root is None or ch == "":
        return 0

    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                return len(bs_elems)

        return 0




def get_basic_radical_tag_list(root, ch):
    if root is None or ch == "":
        return []

    bs_tags_list = []
    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_tag = bs_item.attrib['TAG'].strip()
                    bs_tags_list.append(bs_tag)
        break

    return bs_tags_list


def get_char_bs_tag_and_stroke_ids_dict_list(root, ch):
    """
    Get bs and stroke ids in these bs of this char
    :param root:
    :param ch:
    :return: [{相: [0-8]}, {心:[9-12]}, {木:[0-3]}, {目:[4-8]}]
    """
    if root is None or ch == "":
        return []

    char_bs_tag_stroke_ids_dict_list = []

    # find bs and his stroke ids
    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        # frist level : 相 和 心
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:

                for bs_item in bs_elems:
                    bs_tag_sk_ids_dict = {}
                    bs_tag = bs_item.attrib['TAG'].strip()
                    bs_sk_ids = []
                    bs_sk_root_elems = bs_item.findall("STROKES")
                    if bs_sk_root_elems:
                        bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                        for bs_sk_item in bs_sk_elems:
                            bs_sk_id = bs_sk_item.attrib['ID'].strip()
                            bs_sk_ids.append(bs_sk_id)
                    if len(bs_sk_ids) > 0:
                        bs_tag_sk_ids_dict[bs_tag] = bs_sk_ids.copy()

                    if bs_tag_sk_ids_dict != {}:
                        char_bs_tag_stroke_ids_dict_list.append(bs_tag_sk_ids_dict)

        # second level : 木 和 目
        if char_bs_tag_stroke_ids_dict_list is None or len(char_bs_tag_stroke_ids_dict_list) == 0:
            continue

        for bs_sk_ids_item_dict in char_bs_tag_stroke_ids_dict_list:
            print(bs_sk_ids_item_dict.keys())
            if list(bs_sk_ids_item_dict.keys()) is None or len(list(bs_sk_ids_item_dict.keys())) == 0:
                continue
            bs_tag = list(bs_sk_ids_item_dict.keys())[0]
            bs_count = get_bs_count_of_char(root, bs_tag)
            if bs_count == 1:
                continue

            # this radical can be split into sub-radicals
            bs_sk_ids_dict_list = get_char_bs_tag_and_stroke_ids_dict_list(root, bs_tag)
            if len(bs_sk_ids_dict_list) > 0:
                for item in bs_sk_ids_dict_list:
                    char_bs_tag_stroke_ids_dict_list.append(item)

    return char_bs_tag_stroke_ids_dict_list


def merge_strokes_to_basic_radical_img(ch, char_bs_tag_stroke_ids_dict_list, stroke_img_path=""):
    if char_bs_tag_stroke_ids_dict_list is None or ch == "":
        print("char_bs_tag_stroke_ids_dict_list is none")
        return

    ch_bs_images = []

    # get all stroke images of this char
    all_stroke_img_names = [f for f in os.listdir(stroke_img_path) if ".png" in f]
    ch_stroke_img_names = []
    for name in all_stroke_img_names:
        if ch in name:
            ch_stroke_img_names.append(name)

    # merge stroke images based on the dict list : [{'心': ['9', '10', '11', '12']}, {'相': ['0', '1', '2', '3', '4', '5', '6', '7', '8']}, {'目': ['4', '5', '6', '7', '8']}, {'木': ['0', '1', '2', '3']}]
    for bs_sk_ids_dict in char_bs_tag_stroke_ids_dict_list:
        if list(bs_sk_ids_dict.keys()) is None or len(list(bs_sk_ids_dict.keys())) == 0:
            continue
        bs_tag = list(bs_sk_ids_dict.keys())[0]
        bs_sk_ids = bs_sk_ids_dict[bs_tag]
        bs_sk_ids = [int(ids) for ids in bs_sk_ids]

        bs_sk_img_names = []
        for sk_id in bs_sk_ids:
            for name in ch_stroke_img_names:
                if "_{}.png".format(sk_id) in name:
                    bs_sk_img_names.append(name)

        # merge stroke image togeter
        new_bs = createBlankGrayscaleImageWithSize((256, 256))
        for name in bs_sk_img_names:
            img_path = os.path.join(stroke_img_path, name)
            img = cv2.imread(img_path, 0)

            new_bs = merge_two_images(new_bs, img)

            del img
        ch_bs_images.append(new_bs.copy())

    return ch_bs_images




def merge_two_images(bk, img):
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y] == 0:
                bk[x][y] = 0

    return bk









def get_stroke_order_list(root, ch):
    if root is None or ch == "":
        return []

    stroke_orders = []
    for child in root:
        tag = child.attrib['TAG'].strip()

        if tag != ch:
            continue

        # find stroke order elems
        sk_order_elems = child.findall("STROKE_ORDER")
        if sk_order_elems:
            sk_order_str = sk_order_elems[0].text
            stroke_orders = sk_order_str.split("|")
            break

    return stroke_orders


if __name__ == '__main__':
    chars = "肪肫想"
    print(chars)
    # generate_template_folders(chars, xml_path, stroke_img_path, template_folder_path)

    chars = []
    with open("2300chars.txt", "r") as f:
        for s in f.readlines():
            chars.append(s.strip())
    generate_template_folders(chars, xml_path, stroke_img_path, template_folder_path)


    # ch = "殇"
    # tree = ET.parse(xml_path)
    # root = tree.getroot()

    # ch_bs_list = get_basic_radical_tag_list(root, ch)
    # print(ch_bs_list)

    # chars = "肪肫想"
    # all_bs_tags_list = get_all_basic_radical_type_list(root, chars)
    # print(all_bs_tags_list)
    # char_bs_tag_stroke_ids_dict_list = get_char_bs_tag_and_stroke_ids_dict_list(root, ch)
    # # print(char_bs_tag_stroke_ids_dict_list)
    #
    # bs_imgs = merge_strokes_to_basic_radical_img(ch, char_bs_tag_stroke_ids_dict_list, stroke_img_path=stroke_img_path)
    #
    # for i in range(len(bs_imgs)):
    #     cv2.imshow("{}".format(i), bs_imgs[i])
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

