# coding: utf-8
import os
import cv2

from utils.Functions import calculateSSIM
import shutil
from skimage.measure import compare_ssim


temp_name = "temp_80"

threshold = 0.65

imgs_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/jianti_temp"
temp_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/"

def fanti_strokes_class():
    temp_p = os.path.join(temp_path, "{}.png".format(temp_name))

    temp_img = cv2.imread(temp_p, 0)

    temp_folder = temp_p.replace(".png", "")
    print(temp_folder)
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)

    # ssim for each image
    img_files = [f for f in os.listdir(imgs_path) if ".png" in f]

    for i in range(len(img_files)):
        print("process: ", i)
        p = os.path.join(imgs_path, img_files[i])
        img = cv2.imread(p, 0)

        ssim = compare_ssim(img, temp_img, temp_img.max() - temp_img.min())

        if ssim > threshold:
            shutil.move(p, temp_folder)

        # if i == 100:
        #     break





if __name__ == '__main__':

    fanti_strokes_class()
