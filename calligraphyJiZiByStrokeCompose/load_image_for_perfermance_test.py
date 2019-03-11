# coding: utf-8
import cv2
import os
import time


def load_image_test():
    path="../../../Data/Stroke_recomposed_tool/strokes dataset"
    type_names = [f for f in os.listdir(path) if '.DS_Store' not in f]
    print('type name num: ', len(type_names))

    dataset = {}
    count = 0
    for tn in type_names:
        path_ = os.path.join(path, tn)

        img_obj_list = []
        img_names = [os.path.join(path_, f) for f in os.listdir(path_) if '.png' in f]

        for p in img_names:
            img_ = cv2.imread(p, 0)
            img_ = cv2.resize(img_, (256, 256))
            cv2.imwrite(p, img_)



if __name__ == '__main__':
    load_image_test()