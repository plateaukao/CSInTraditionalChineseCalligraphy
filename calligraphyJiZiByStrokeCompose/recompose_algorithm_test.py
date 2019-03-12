# coding: utf-8
import os
import cv2
import time

from calligraphyJiZiByStrokeCompose.util import query_char_info, query_char_target_strokes, stroke_recompose, \
                    load_stroke_library_dataset, query_char_info_from_chars_list, query_char_target_stroke_by_dataset


def recompose():
    start_time = time.time()
    stroke_lib_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"
    dataset = load_stroke_library_dataset(stroke_lib_path)
    print("Load dataset time: ", time.time() - start_time)

    chars = ['的']

    char_info_list = query_char_info_from_chars_list(chars)

    char_target_strokes_list = query_char_target_stroke_by_dataset(dataset, char_info_list)

    enerated_imgs, _ = stroke_recompose(char_info_list, char_target_strokes_list)





if __name__ == '__main__':
    recompose()