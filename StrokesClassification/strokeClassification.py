# coding: utf-8
import cv2
import os
import numpy as np
from shutil import copyfile, move

from StrokesClassification.stroke_pattern import check_heng_pattern, check_shu_pattern


def stroke_classification():
    basic_path = '/Users/liupeng/Documents/Data'
    strokes_path = os.path.join(basic_path, 'Strokes_png_test')

    stroke_name = 'heng'
    saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)

    if not os.path.exists(saved_strokes_path):
        os.mkdir(saved_strokes_path)

    stroke_name = 'shu'
    saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)

    if not os.path.exists(saved_strokes_path):
        os.mkdir(saved_strokes_path)

    stroke_name = 'pie'
    saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)

    if not os.path.exists(saved_strokes_path):
        os.mkdir(saved_strokes_path)

    stroke_name = 'na'
    saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)

    if not os.path.exists(saved_strokes_path):
        os.mkdir(saved_strokes_path)

    stroke_name = 'dian'
    saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)

    if not os.path.exists(saved_strokes_path):
        os.mkdir(saved_strokes_path)



    filenames = [f for f in os.listdir(strokes_path) if '.png' in f]
    print('Files len: ', len(filenames))

    for i in range(len(filenames)):
        print("Process id: ", i)
        fl = filenames[i]

        img_path = os.path.join(strokes_path, fl)

        # heng
        # if check_heng_pattern(img_path):
        #     # cp this img to heng directory
        #     stroke_name = 'heng'
        #     saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)
        #     move(img_path, os.path.join(saved_strokes_path, fl))

        if check_shu_pattern(img_path):
            # cp this img to shu directory
            stroke_name = 'shu'
            saved_strokes_path = os.path.join(basic_path, 'strokes_classification', stroke_name)
            move(img_path, os.path.join(saved_strokes_path, fl))



if __name__ == '__main__':
    stroke_classification()