# coding: utf-8
import os
import xml.etree.ElementTree as ET
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
from calligraphyJiZiByStrokeCompose.basicradical import BasicRadical, Stroke
from calligraphyJiZiByStrokeCompose.util import load_basic_radicals_library_dataset, load_stroke_library_dataset

from calligraphyJiZiByStrokeCompose.model import query_char_info_from_chars_list, query_similar_basic_radicals_and_strokes
from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize

import ast
import cv2

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"
char_root_path = "/Users/liupeng/Documents/Data/Calligraphy_database/Chars_775"

def char_generations(chars):
    generated_images = []
    selected_basic_radicals = []
    selected_strokes = []

    # query the char info
    chars_info_list = query_char_info_from_chars_list(chars, xml_path)

    # load the basic radicals library
    basic_radicals_dataset = load_basic_radicals_library_dataset()

    # # load the stroke library
    strokes_dataset = load_stroke_library_dataset()

    # # find similar basic radicals and strokes
    similar_chars = query_similar_basic_radicals_and_strokes(basic_radicals_dataset, strokes_dataset, chars_info_list)

    for sc in similar_chars:
        similar_basic_radicals, similar_strokes = sc

        # get basic radicals info and his strokes images
        similar_bs_dict = {}
        for bs_id in similar_basic_radicals.keys():

            bs_obj = []

            for bs_ in similar_basic_radicals[bs_id]:

                bs_obj_dict = {}

                path_ = bs_["path"]
                strokes_id_ = bs_["strokes_id"]

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
                bs_obj.append(bs_obj_dict)

            if bs_obj != []:
                similar_bs_dict[bs_id] = bs_obj

        print(similar_bs_dict)

        # recompose basic radicals and strokes

        bk = createBlankGrayscaleImageWithSize((256, 256))
        # load basic radicals stroke images
        for bs_id in similar_bs_dict.keys():
            for bs_obj in similar_bs_dict[bs_id]:
                print(bs_obj)
                stroke_objs = bs_obj["strokes"]
                for s_id in stroke_objs.keys():
                    path_ = stroke_objs[s_id]

                    img_ = cv2.imread(path_, 0)

                    for x in range(img_.shape[0]):
                        for y in range(img_.shape[1]):
                            if img_[x][y] == 0:
                                bk[x][y] = 0

        # load stroke images
        for s_id in similar_strokes.keys():
            path_ = similar_strokes[s_id][0]

            img_ = cv2.imread(path_, 0)

            for x in range(img_.shape[0]):
                for y in range(img_.shape[1]):
                    if img_[x][y] == 0:
                        bk[x][y] = 0


        generated_images.append(bk)

    return generated_images, selected_basic_radicals, selected_strokes


if __name__ == '__main__':
    # run()

    # chars = "仟"
    # char_info_list = query_char_info_from_chars_list(chars, xml_path)
    # print(len(char_info_list))
    # print(char_info_list[0].basic_radicals[0].tag)
    #
    # for bs in char_info_list[0].basic_radicals:
    #     print(bs.tag, bs.id, bs.strokes_id, bs.position)
    # for sk in char_info_list[0].strokes:
    #     print(sk.id, sk.tag, sk.position)

    chars = "仟"
    results, basic_radicals, strokes = char_generations(chars)

    for i in range(len(results)):
        cv2.imshow("img_%d" % i, results[i] )

    cv2.waitKey(0)
    cv2.destroyAllWindows()