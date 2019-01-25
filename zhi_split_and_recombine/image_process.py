# coding: utf8
import cv2
import os


def image_process():
    path = '/Users/liupeng/Documents/Data/兰亭序-之/original/zhi12/12.tiff'

    img = cv2.imread(path, 0)

    _, img_bit = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)

    cv2.imwrite('1.png', img_bit)


    cv2.imshow('img', img_bit)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_process()