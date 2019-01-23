# coding: utf-8
import cv2
import os
from utils.Functions import getAllMiniBoundingBoxesOfImage, getCenterOfRectangles, combineRectangles, rgb2qimage


def layout_analysis():
    path = 'test.jpg'

    img_ = cv2.imread(path, 0)

    _, img_bit = cv2.threshold(img_, 127, 255, cv2.THRESH_BINARY)

    boxes = getAllMiniBoundingBoxesOfImage(img_bit)
    print('all boxes len: ', len(boxes))

    cv2.imshow("original", img_bit)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    layout_analysis()