# coding: utf-8
import cv2
import numpy as np
from utils.Functions import getSingleMaxBoundingBoxOfImage


def check_heng_pattern(img_path):
    img_ = cv2.imread(img_path, 0)
    if img_ is not None:
        x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)

        black_area = np.sum((255 - np.array(img_, dtype=np.uint8)) / 255)
        total_area = w * h

        # long heng
        if w / h >= 6:
            return True
        if w / h >= 4.5 and black_area / total_area > 0.4:
            return True

        if w / h >= 3.2 and black_area / total_area > 0.4:
            return True

        if w / h >= 3.8 and black_area / total_area > 0.37:
            return True

        if w / h >= 4.9 and black_area / total_area > 0.31:
            return True
        if w / h >= 4.8 and black_area / total_area > 0.34:
            return True

    return False


def check_shu_pattern(img_path):
    img_ = cv2.imread(img_path, 0)
    if img_ is not None:
        x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)

        black_area = np.sum((255 - np.array(img_, dtype=np.uint8)) / 255)
        total_area = w * h

        if h / w > 7.1:
            return True
        if h / w > 6.6 and black_area / total_area > 0.4:
            return True

        if h / w > 5.45 and black_area / total_area > 0.45:
            return True
        if h / w > 4.9 and black_area / total_area > 0.51:
            return True



    return False
