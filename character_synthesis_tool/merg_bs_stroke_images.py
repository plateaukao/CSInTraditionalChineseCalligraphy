# coding: utf-8
import os
import xml.etree.ElementTree as ET
import copy
import cv2
from utils.Functions import createBlankGrayscaleImageWithSize, getSingleMaxBoundingBoxOfImage

xml_path = "./img_merge_test/add_bs_sk_position_test_result_add_sk_ids_result.xml"



def get_similar_chars_with_same_struct_and_bs_tags(root, ch):
    if root is None or ch == "":
        return

    ch_bs_tags_dict = {}

    ch_struct = ""

    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        struct_elems = child.findall("STRUCTURE")
        if struct_elems:
            ch_struct = struct_elems[0].text.strip()

        # parse the xml to get bs id and position
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                b_id = int(bs_item.attrib['ID'].strip())
                bs_tag = bs_item.attrib['TAG'].strip()

                ch_bs_tags_dict[b_id] = bs_tag

    similar_chars_with_same_bs_tags_dict = {}

    for bs_id in ch_bs_tags_dict.keys():
        bs_tag = ch_bs_tags_dict[bs_id]

        similar_chars = []

        for child in root:
            tag = child.attrib['TAG'].strip()
            if tag == ch:
                continue

            # need to same structure
            struct_str = ""
            struct_elems = child.findall("STRUCTURE")
            if struct_elems and struct_elems[0].text:
                struct_str = struct_elems[0].text.strip()

            if struct_str != ch_struct:
                continue

            # parse the xml to get bs id and position
            bs_root_elems = child.findall("BASIC_RADICALS")
            if bs_root_elems:
                bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
                for bs_item in bs_elems:
                    # b_id = int(bs_item.attrib['ID'].strip())
                    bs_tag_ = bs_item.attrib['TAG'].strip()

                    if bs_tag_ == bs_tag:
                        if tag not in similar_chars:
                            similar_chars.append(tag)
        similar_chars_with_same_bs_tags_dict[bs_id] = similar_chars.copy()

    return ch_bs_tags_dict, similar_chars_with_same_bs_tags_dict



def get_bs_sk_ids_list(root, ch, bs_id=0):
    if root is None or ch == "":
        return

    bs_sk_ids = []

    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue

        # parse the xml to get bs id and position
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                b_id = int(bs_item.attrib['ID'].strip())
                if bs_id == b_id:
                    # find the sk ids in this bs
                    bs_sk_root_elems = bs_item.findall("STROKES")
                    if bs_sk_root_elems:
                        bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                        for bs_sk_item in bs_sk_elems:
                            bs_sk_id = int(bs_sk_item.attrib['ID'].strip())
                            bs_sk_ids.append(bs_sk_id)
                    break

    return bs_sk_ids




def get_basic_radicals_postion_dict(root, ch):
    if root is None or ch == "":
        return {}

    bs_position_dict = {}

    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue
        # parse the xml to get bs id and position
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                bs_id = int(bs_item.attrib['ID'].strip())
                bs_post = bs_item.attrib['POSITION'].strip().replace("(", "").replace(")", "").replace(" ", "").split(",")
                bs_post = [int(p) for p in bs_post]

                bs_position_dict[bs_id] = bs_post.copy()

    return bs_position_dict


def get_strokes_position_dict(root, ch):
    if root is None or ch == "":
        return {}

    strokes_positon_dict = {}
    for child in root:
        tag = child.attrib['TAG'].strip()
        if tag != ch:
            continue
        # parse the xml to get bs id and position
        bs_root_elems = child.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            for bs_item in bs_elems:
                bs_sk_root_elems = bs_item.findall("STROKES")
                if bs_sk_root_elems:
                    bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                    for bs_sk_item in bs_sk_elems:
                        bs_sk_id = int(bs_sk_item.attrib['ID'].strip())
                        bs_sk_post = bs_sk_item.attrib['POSITION'].strip().replace("(", "").replace(")", "").replace(" ", "").split(",")
                        bs_sk_post = [int(p) for p in bs_sk_post]

                        strokes_positon_dict[bs_sk_id] = bs_sk_post.copy()

    return strokes_positon_dict


def merge_stroke_images(bk, post, similar_stroke_path):
    if bk is None or post is None or similar_stroke_path == "":
        return

    img = cv2.imread(similar_stroke_path, 0)
    if img is None:
        print("not open image {}".format(similar_stroke_path))
        return

    stroke_bk = createBlankGrayscaleImageWithSize(bk.shape)

    offset_base = int((bk.shape[0] - img.shape[0]) / 2)

    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    rect = getSingleMaxBoundingBoxOfImage(img)
    if rect is None:
        print("not get rect of stroke image")
        return

    # merge bk and stroke image with center align
    cent_x0 = int(post[0] + post[2] / 2)
    cent_y0 = int(post[1] + post[3] / 2)

    cent_x = int(rect[0] + rect[2] / 2)
    cent_y = int(rect[1] + rect[3] / 2)

    offset_x = cent_x - cent_x0
    offset_y = cent_y - cent_y0

    new_img = createBlankGrayscaleImageWithSize(bk.shape)
    new_img[rect[1]-offset_y+offset_base: rect[1]-offset_y+offset_base+rect[3], rect[0]-offset_x+offset_base: \
                        rect[0]-offset_x+offset_base+rect[2]] = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

    for x in range(new_img.shape[0]):
        for y in range(new_img.shape[1]):
            if new_img[x][y] == 0:
                bk[x][y] = 0
                stroke_bk[x][y] = 0
    return bk, stroke_bk.copy()


def merge_select_stroke_images(bk, ch_sk_postion_dict, ch_stroke_img_name_dict, stroke_png_path):
    if bk is None or ch_sk_postion_dict is None or len(ch_sk_postion_dict) == 0 or \
        ch_stroke_img_name_dict is None or len(ch_stroke_img_name_dict) == 0:
        return
    stroke_bks = []
    for sk_id in ch_sk_postion_dict.keys():
        sk_post = ch_sk_postion_dict[sk_id]

        sk_img_name = ch_stroke_img_name_dict[sk_id]
        img_path = os.path.join(stroke_png_path, sk_img_name)
        bk, sk_bk = merge_stroke_images(bk, sk_post, img_path)
        stroke_bks.append(sk_bk)
    return bk, stroke_bks.copy()



if __name__ == '__main__':
    ch_path = "./img_merge_test/他_4ED6.png"
    root_path = "./img_merge_test"

    tree = ET.parse(xml_path)
    root = tree.getroot()

    ch = "他"

    bs_sk_ids = get_bs_sk_ids_list(root, ch, 0)
    print(bs_sk_ids)

    # ta_img = cv2.imread(ch_path, 0)
    #
    # ch_bs_post_dict = get_basic_radicals_postion_dict(root, ch)
    # print("{} bs post dict: ", ch_bs_post_dict)
    #
    # ch_sk_post_dict = get_strokes_position_dict(root, ch)
    # print("{} sk post dict: ", ch_sk_post_dict)
    #
    # # get the stroke and img dict of this char
    # all_strokes_names = [f for f in os.listdir(root_path) if ".png" in f and len(f.split("_")) == 3]
    # print("all stroke num: {}".format(len(all_strokes_names)))
    # print(all_strokes_names)
    #
    # ch_stroke_img_name_dict = {}
    # ch_stroke_img_name_list = []
    # for name in all_strokes_names:
    #     if ch in name:
    #         ch_stroke_img_name_list.append(name)
    #
    # for i in range(len(ch_stroke_img_name_list)):
    #     for name in ch_stroke_img_name_list:
    #         if "_{}.png".format(i) in name:
    #             ch_stroke_img_name_dict[i] = name
    #             break
    # print("ch stroke img name dict: ", ch_stroke_img_name_dict)

    # bk = createBlankGrayscaleImageWithSize((600, 600))
    # bk_no_align = bk.copy()
    #
    # for sk_id in ch_sk_post_dict.keys():
    #     sk_post = ch_sk_post_dict[sk_id]
    #
    #     sk_img_name = ch_stroke_img_name_dict[sk_id]
    #     img_path = os.path.join(root_path, sk_img_name)
    #     img = cv2.imread(img_path, 0)
    #     _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    #     rect = getSingleMaxBoundingBoxOfImage(img)
    #
    #     cent_x0 = int(sk_post[0] + sk_post[2] / 2)
    #     cent_y0 = int(sk_post[1] + sk_post[3] / 2)
    #
    #     cent_x = int(rect[0] + rect[2] / 2)
    #     cent_y = int(rect[1] + rect[3] / 2)
    #
    #     offset_x = cent_x - cent_x0
    #     offset_y = cent_y - cent_y0
    #
    #     # add rect to ta image to test this post is right
    #     if sk_id == 0:
    #         cv2.rectangle(ta_img, (sk_post[0], sk_post[1]), (sk_post[0]+sk_post[2], sk_post[1]+sk_post[3]), 0, 1)
    #         cv2.rectangle(ta_img, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), 0, 1)
    #         cv2.rectangle(ta_img, (rect[0]-offset_x, rect[1]-offset_y), (rect[0]-offset_x + rect[2], rect[1]-offset_y + rect[3]), 0, 1)
    #
    #
    #     print(rect)
    #
    #     for x in range(img.shape[0]):
    #         for y in range(img.shape[1]):
    #             if img[x][y] == 0:
    #                 bk_no_align[x][y] = 0
    #
    #     bk = merge_stroke_images(bk, sk_post, img_path)


    # cv2.imshow("bk", bk)
    # cv2.imshow("bo no align", bk_no_align)
    # cv2.imshow("img", ta_img)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # calculate the location and size ssim
    # for sk_id in ch_sk_post_dict.keys():
    #     sk_post = ch_sk_post_dict[sk_id]
    #
    #     cent_x0 = int(sk_post[0] + sk_post[2] / 2)
    #     cent_y0 = int(sk_post[1] + sk_post[3] / 2)
    #
    #     for name in all_strokes_names:
    #         img_path = os.path.join(root_path, name)
    #         img = cv2.imread(img_path, 0)
    #         _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    #
    #         rect = getSingleMaxBoundingBoxOfImage(img)
    #         cent_x = int(rect[0] + rect[2] / 2)
    #         cent_y = int(rect[1] + rect[3] / 2)
    #
    #         locat_ssim = abs(cent_x0 - cent_x) + abs(cent_y0 - cent_y)
    #         size_ssim = abs(sk_post[2] - rect[2]) + abs(sk_post[3] - rect[3])
    #
    #         print("sk_id: {}, img: {}  locate ssim: {}, size ssim: {}".format(sk_id, name, locat_ssim, size_ssim))





