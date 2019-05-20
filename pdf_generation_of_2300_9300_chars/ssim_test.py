# coding: utf-8
import os
import cv2
from skimage.measure import compare_ssim

imgs_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/jianti_temp"
temp_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/"

def ssim_test():
    src = os.path.join(temp_path, "temp_80.png")
    tag = os.path.join(imgs_path, "棧_68E7_stroke_10.png")

    src_img = cv2.imread(src, 0)
    tag_img = cv2.imread(tag, 0)


    ssim = compare_ssim(src_img, tag_img, tag_img.max() - tag_img.min())
    print("ssim: ", ssim)

    ssim = compare_ssim(tag_img, src_img, src_img.max() - src_img.min())
    print("ssim: ", ssim)


if __name__ == '__main__':
    ssim_test()