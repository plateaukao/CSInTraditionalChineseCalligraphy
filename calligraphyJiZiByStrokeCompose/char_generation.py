# coding: utf-8
import os
import xml.etree.ElementTree as ET
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
from calligraphyJiZiByStrokeCompose.basicradical import BasicRadical, Stroke
from calligraphyJiZiByStrokeCompose.util import load_basic_radicals_library_dataset, load_stroke_library_dataset

from calligraphyJiZiByStrokeCompose.model import query_char_info_from_chars_list, query_similar_basic_radicals_and_strokes, recompose_chars
from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize

import ast
import cv2

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"
char_root_path = "/Users/liupeng/Documents/Data/Calligraphy_database/Chars_775"

def char_generations(chars):

    # query the char info
    chars_info_list = query_char_info_from_chars_list(chars, xml_path)

    # load the basic radicals library
    basic_radicals_dataset = load_basic_radicals_library_dataset()

    # # load the stroke library
    strokes_dataset = load_stroke_library_dataset()

    # # find similar basic radicals and strokes
    similar_chars = query_similar_basic_radicals_and_strokes(basic_radicals_dataset, strokes_dataset, chars_info_list)

    generated_images = recompose_chars(chars_info_list, similar_chars, char_root_path)

    return generated_images, similar_chars


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

    # chars = "吉"
    # chars = "及"
    # results, similar_chars = char_generations(chars)
    #
    # for i in range(len(results)):
    #     cv2.imshow("img_%d" % i, results[i] )
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    path = "../../../Data/Calligraphy_database/Chars_1000"

    save_path = "../../../Data/generated_results/777_chars_add_most_similar_strokes_func"

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    chars = [f for f in os.listdir(path) if "." not in f]
    print(len(chars))
    print(chars)
    #
    for i in range(len(chars)):
        ch = chars[i]
        print(ch)

        generated_images, _ = char_generations(ch)

        img_ = generated_images[0]

        cv2.imwrite(os.path.join(save_path, "%s_%d.png" % (ch, i)), img_)

    targ_bs_obj_list = query_char_info_from_chars_list(["告"])
    print(targ_bs_obj_list[0].basic_radicals[0].strokes_id)


