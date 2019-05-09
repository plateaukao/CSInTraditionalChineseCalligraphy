# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET
import shutil

from utils.Functions import getAllMiniBoundingBoxesOfImage, getConnectedComponentsOfGrayScale, \
    createBlankGrayscaleImageWithSize, getSingleMaxBoundingBoxOfImage


def left_right_split():
    root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp"
    save_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_left_right"
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

        if fn_struct == "Left and Right":
            lr_count += 1

            radical_list = get_radicals_info(root, fn)
            print(radical_list)

            # copy char path to save path
            if not os.path.exists(os.path.join(save_path, fn)):
                # shutil.copytree(os.path.join(root_path, fn), os.path.join(save_path, fn))
                shutil.move(os.path.join(root_path, fn), os.path.join(save_path, fn))

            # open char image
            img_names = [f for f in os.listdir(os.path.join(save_path, fn)) if ".png" in f]
            if len(img_names) == 0:
                print("root path no image ")
                continue
            img_path = os.path.join(save_path, fn, img_names[0])
            img = cv2.imread(img_path, 0)

            bk_left, bk_right = merge_radical_left_right(img)

            left_radical_name = img_names[0].replace(".png", "") + "_0_" + radical_list[0]
            right_radical_name = img_names[0].replace(".png", "") + "_1_" + radical_list[1]

            left_radical_path = os.path.join(save_path, fn, "basic radicals", left_radical_name)
            right_radical_path = os.path.join(save_path, fn, "basic radicals", right_radical_name)

            if not os.path.exists(left_radical_path):
                os.mkdir(left_radical_path)
            if not os.path.exists(right_radical_path):
                os.mkdir(right_radical_path)

            cv2.imwrite(os.path.join(save_path, fn, "basic radicals", "{}.png".format(left_radical_name)), bk_left)
            cv2.imwrite(os.path.join(save_path, fn, "basic radicals", "{}.png".format(right_radical_name)), bk_right)





        elif fn_struct == "Up and Down":
            ud_count += 1

        # if i == 10:
        #     break

    print("lr: {}, ud: {}".format(lr_count, ud_count))



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


def merge_radical_left_right(img):
    if img is None:
        print("img is none!")
        return

    rects = getAllMiniBoundingBoxesOfImage(img)

    rect_imgs = getConnectedComponentsOfGrayScale(img)
    print("rect img num: ", len(rect_imgs))
    print(rects)

    left_side_list = []
    right_side_list = []
    for i in range(len(rects)):
        x, y, w, h = rects[i]

        cent_x = x + int(w / 2)
        cent_y = y + int(h / 2)

        if cent_x > 127:
            right_side_list.append(rects[i])
        else:
            left_side_list.append(rects[i])

        print(cent_x, cent_y)

    print(left_side_list)
    print(right_side_list)

    # check images
    bk_left = createBlankGrayscaleImageWithSize(img.shape)
    bk_right = createBlankGrayscaleImageWithSize(img.shape)

    for rimg in rect_imgs:
        rect = getSingleMaxBoundingBoxOfImage(rimg)
        if rect in left_side_list:
            bk_left = merge_two_images(bk_left, rimg)
        elif rect in right_side_list:
            bk_right = merge_two_images(bk_right, rimg)

    return (bk_left, bk_right)




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
    left_right_split()

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

    # check preccsed left right files
    # root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp"
    # save_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_left_right"
    #
    # clean_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_clean"
    #
    # original_files = [f for f in os.listdir(root_path) if "." not in f]
    # processed_files = [f for f in os.listdir(save_path) if "." not in f]
    #
    # for of in original_files:
    #     if of in processed_files:
    #         shutil.move(os.path.join(root_path, of), os.path.join(clean_path, of))

