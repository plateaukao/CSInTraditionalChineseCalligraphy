# coding: utf-8
import cv2
import os

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImage

img_path = '住_4F4F_1.png'

img_ = cv2.imread(img_path, 0)

x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)
blank_ = createBlankGrayscaleImage(img_)

blank_[128-int(h/2): 128-int(h/2)+h, 128-int(w/2): 128-int(w/2)+w] = img_[y:y+h, x:x+w]

cv2.imshow("crop", blank_)

cv2.waitKey(0)
cv2.destroyAllWindows()
