# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET
import shutil

from utils.Functions import getAllMiniBoundingBoxesOfImage, getConnectedComponentsOfGrayScale, \
    createBlankGrayscaleImageWithSize, getSingleMaxBoundingBoxOfImage


def up_down_split():
    root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp"
    save_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_up_down"
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

    tree = ET.parse(xml_path)

    if tree is None:
        print("Tree is none!")
        return

    root = tree.getroot()

    # file path
    file_names = [f for f in os.listdir(root_path) if "." not in f]
    print("files num: ", len(file_names))

    lr_count = 0
    ud_count = 0
    for i in range(len(file_names)):
        fn = file_names[i]

        fn_struct = get_structure_info(root, fn)
        print(fn_struct)

        if fn_struct == "Up and Down":
            ud_count += 1

            radical_list = get_radicals_info(root, fn)
            print(radical_list)

            if len(radical_list) != 2:
                print("fn: ", fn, " not 2 radicals")
                continue

            # copy char path to save path
            if not os.path.exists(os.path.join(save_path, fn)):
                # shutil.copytree(os.path.join(root_path, fn), os.path.join(save_path, fn))
                shutil.move(os.path.join(root_path, fn), os.path.join(save_path, fn))

            # open char image
            img_names = [f for f in os.listdir(os.path.join(save_path, fn)) if ".png" in f]
            if len(img_names) == 0:
                print("root path no image ")
                continue
            # img_path = os.path.join(save_path, fn, img_names[0])
            # img = cv2.imread(img_path, 0)

            bk_up, bk_down = merge_radical_up_down(os.path.join(save_path, fn, "strokes"))

            up_radical_name = img_names[0].replace(".png", "") + "_0_" + radical_list[0]
            down_radical_name = img_names[0].replace(".png", "") + "_1_" + radical_list[1]

            up_radical_path = os.path.join(save_path, fn, "basic radicals", up_radical_name)
            down_radical_path = os.path.join(save_path, fn, "basic radicals", down_radical_name)

            if not os.path.exists(up_radical_path):
                os.mkdir(up_radical_path)
            if not os.path.exists(down_radical_path):
                os.mkdir(down_radical_path)

            cv2.imwrite(os.path.join(save_path, fn, "basic radicals", "{}.png".format(up_radical_name)), bk_up)
            cv2.imwrite(os.path.join(save_path, fn, "basic radicals", "{}.png".format(down_radical_name)), bk_down)

        # if i == 100:
        #     break

    print("ud: {}".format(ud_count))



def get_structure_info(root, char):
    if root is None or char == "":
        print("root or char is none!")
        return ""

    for i in range(len(root)):
        elem = root[i]
        tag = elem.attrib["TAG"].strip()
        if tag != char:
            continue

        struct_info = ""
        struct_elems = elem.findall("STRUCTURE")
        if struct_elems:
            struct_info = struct_elems[0].text
        return struct_info


def get_radicals_info(root, char):
    if root is None or char == "":
        print("root or char is none!")
        return []

    for i in range(len(root)):
        elem = root[i]

        tag = elem.attrib["TAG"].strip()

        if tag != char:
            continue

        radicals_list = []
        sub_radical_root_elems = elem.findall("SUB_RADICALS")
        if sub_radical_root_elems:

            sub_radical_elems = sub_radical_root_elems[0].findall("SUB_RADICAL")

            print("sub num: ", len(sub_radical_elems))
            for item in sub_radical_elems:
                radicals_list.append(item.attrib["TAG"].strip())

        return radicals_list


def merge_radical_up_down(strokes_path):
    if not os.path.exists(strokes_path):
        print("stroke path not exist")
        return

    # get all stroke images
    stroke_names_ = [f for f in os.listdir(strokes_path) if ".png" in f]
    print("stroke : ", stroke_names_)

    # sorted image names
    stroke_names = []
    for i in range(len(stroke_names_)):
        for sn in stroke_names_:
            if "_{}.png".format(i) in sn:
                stroke_names.append(sn)
                break
    print(stroke_names)

    # up and down list
    up_strokes_list = []
    down_strokes_list = []

    for sn in stroke_names:
        sk_img_path = os.path.join(strokes_path, sn)
        sk_img = cv2.imread(sk_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(sk_img)
        cent_x = x + int(w / 2)
        cent_y = y + int(h / 2)

        if cent_y > 120:
            down_strokes_list.append(sk_img_path)
        else:
            up_strokes_list.append(sk_img_path)

    # check images
    bk_up = createBlankGrayscaleImageWithSize((256, 256))
    bk_down = createBlankGrayscaleImageWithSize((256, 256))

    for img_path in up_strokes_list:
        img = cv2.imread(img_path, 0)
        bk_up = merge_two_images(bk_up, img)

    for img_path in down_strokes_list:
        img = cv2.imread(img_path, 0)
        bk_down = merge_two_images(bk_down, img)

    return (bk_up, bk_down)



# def merge_radical_up_down(img):
#     if img is None:
#         print("img is none!")
#         return
#
#     rects = getAllMiniBoundingBoxesOfImage(img)
#
#     rect_imgs = getConnectedComponentsOfGrayScale(img)
#     print("rect img num: ", len(rect_imgs))
#     print(rects)
#
#     up_side_list = []
#     down_side_list = []
#     for i in range(len(rects)):
#         x, y, w, h = rects[i]
#
#         cent_x = x + int(w / 2)
#         cent_y = y + int(h / 2)
#
#         if cent_y > 127:
#             down_side_list.append(rects[i])
#         else:
#             up_side_list.append(rects[i])
#
#         print(cent_x, cent_y)
#
#     print(up_side_list)
#     print(down_side_list)
#
#     # check images
#     bk_up = createBlankGrayscaleImageWithSize(img.shape)
#     bk_down = createBlankGrayscaleImageWithSize(img.shape)
#
#     for rimg in rect_imgs:
#         rect = getSingleMaxBoundingBoxOfImage(rimg)
#         if rect in up_side_list:
#             bk_up = merge_two_images(bk_up, rimg)
#         elif rect in down_side_list:
#             bk_down = merge_two_images(bk_down, rimg)
#
#     return (bk_up, bk_down)




def merge_two_images(bk, img):
    if bk is None or img is None:
        print("bk or img is none!")
        return
    if bk.shape != img.shape:
        print("two images are not same shape")
        return
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] == 0:
                bk[y][x] = 0

    return bk


if __name__ == '__main__':
    up_down_split()

    # img_path = "../../../Data/Calligraphy_database/not_process_data_split/lp/蛑/蛑_86D1.png"
    # img = cv2.imread(img_path, 0)
    #
    #
    # bk_left, bk_right = merge_radical_left_right(img)
    #
    # cv2.imshow("left", bk_left)
    # cv2.imshow("right", bk_right)
    #
    #
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

