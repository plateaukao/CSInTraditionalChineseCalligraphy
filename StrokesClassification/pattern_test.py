# coding: utf-8

import cv2
import os
import numpy as np
from shutil import copyfile, move
from utils.Functions import getSingleMaxBoundingBoxOfImage, calculateSSIM, calculateCoverageRate

from StrokesClassification.stroke_pattern import check_heng_pattern

template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/classification/pieshang.png'
# template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images/与_4E0E_1.png'
path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images/乇_4E47_0.png'

img = cv2.imread(path, 0)

temp_img = cv2.imread(template_path, 0)


cr = calculateCoverageRate(temp_img, img)
ssim = calculateSSIM(temp_img, img)

print("cr: %0.3f , ssim: %0.3f" % (cr, ssim))