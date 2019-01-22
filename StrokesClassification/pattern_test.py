# coding: utf-8

import cv2
import os
import numpy as np
from shutil import copyfile, move
from utils.Functions import getSingleMaxBoundingBoxOfImage

from StrokesClassification.stroke_pattern import check_heng_pattern

path = '/Users/liupeng/Documents/Data/Strokes_png_test/丄_4E04_0.png'

img = cv2.imread(path, 0)

if img is None:
    print("img is None")

x, y, w, h = getSingleMaxBoundingBoxOfImage(img)
print(w, h, (h / w))

# area ratio
black_area = np.sum((255 - np.array(img, dtype=np.uint8)) / 255)
total_area = w * h

print(black_area / total_area)