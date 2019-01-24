# coding: utf-8

import cv2
import os
import numpy as np
from shutil import copyfile, move
from utils.Functions import getSingleMaxBoundingBoxOfImage, calculateSSIM, calculateCoverageRate

from StrokesClassification.stroke_pattern import check_heng_pattern

# template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/classification/long_heng.png'
template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images/与_4E0E_1.png'
path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images/磲_78F2_4.png'

img = cv2.imread(path, 0)

if img:
    print('not null')
else:
    print('null')

temp_img = cv2.imread(template_path, 0)

cv2.imshow('img', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

# cr = calculateCoverageRate(temp_img, img)
# ssim = calculateSSIM(temp_img, img)

# print("cr: %0.3f , ssim: %0.3f" % (cr, ssim))