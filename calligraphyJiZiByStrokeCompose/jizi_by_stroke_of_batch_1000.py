# coding: utf-8
import os
import random
from calligraphyJiZiByStrokeCompose.chinesecharacter import ChineseCharacter
import xml.etree.ElementTree as ET
import ast
import cv2
from time import time
import timeit

from calligraphyJiZiByStrokeCompose.util import query_char_target_strokes, stroke_recompose, \
        query_char_info_from_chars_list, load_stroke_library_dataset, query_char_target_stroke_by_dataset
from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize


def generate_calligraphy_images():

    s_time = timeit.default_timer()

    temp_chars_path = "775basic_characters.txt"
    all_chars_path = "chinese_characters.txt"

    save_path = "../../../Data/1000 generated results"

    stroke_lib_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"
    s_time = timeit.default_timer()
    strokes_dataset = load_stroke_library_dataset(stroke_lib_path)
    print('Load dataset time:', timeit.default_timer() - s_time)

    temp_chars = []
    with open(temp_chars_path, 'r') as f:
        temp_chars = f.readlines()
        temp_chars = [c.strip() for c in temp_chars]

    all_chars = []
    with open(all_chars_path, 'r') as f:
        all_chars = f.readlines()
        all_chars = [c.strip() for c in all_chars]
    print('temp chars num: ', len(temp_chars), ' all chars num: ', len(all_chars))

    # shuffle
    random.shuffle(all_chars)
    random.shuffle(all_chars)

    # select 1200 chars
    # chars = ['梅']
    chars = []
    for i in range(1200):
        chars.append(all_chars[i])
    print("char num: ", len(chars))

    print('Select chars time:', timeit.default_timer() - s_time)

    s_time = timeit.default_timer()
    char_info_list = query_char_info_from_chars_list(chars)
    print("char info list num: ", len(char_info_list))
    print('Select chars info list time:', timeit.default_timer() - s_time)

    s_time = timeit.default_timer()
    char_target_strokes_list = query_char_target_stroke_by_dataset(strokes_dataset, char_info_list)
    # char_target_strokes_list = query_char_target_strokes(char_info_list)
    print('Select chars target stroke time:', timeit.default_timer() - s_time)

    s_time = timeit.default_timer()
    generated_imgs = stroke_recompose(char_info_list, char_target_strokes_list)
    print("generated images num:", len(generated_imgs))
    print('generation image time:', timeit.default_timer() - s_time)

    s_time = timeit.default_timer()
    for i in range(len(generated_imgs)):
        cv2.imwrite(os.path.join(save_path, "%s_%04d.png" % (char_info_list[i].tag, i)), generated_imgs[i])
    print('save images time:', timeit.default_timer() - s_time)


if __name__ == '__main__':

    start_time = timeit.default_timer()
    generate_calligraphy_images()
    end_time = timeit.default_timer()
    print('Time: ', end_time - start_time)