# coding: utf-8
import os
import cv2
from skimage.measure import compare_ssim

from utils.Functions import calculateSSIM, getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize
import shutil


temp_name = "temp_1"

imgs_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/jianti_temp"
temp_path = "../../../Data/stroke_classification_dataset/fanti_stroke_classification/"

# def ssim_test():
#     src = os.path.join(imgs_path, "諭_8AED_stroke_3.png")
#     tag = os.path.join(imgs_path, "諫_8AEB_stroke_3.png")
#
#     src_img = cv2.imread(src, 0)
#     tag_img = cv2.imread(tag, 0)
#
#     ssim = get_ssim(src_img, tag_img)
#     print("ssim: ", ssim)
#
#
# def get_ssim(src_img, tag_img):
#
#     total_count = 0
#     valid_count = 0
#
#     for y in range(src_img.shape[0]):
#         for x in range(src_img.shape[1]):
#             if src_img[y][x] == 255:
#                 continue
#
#             if src_img[y][x] == 0:
#                 total_count += 1
#                 if src_img[y][x] == tag_img[y][x]:
#                     valid_count += 1
#
#     return valid_count / total_count * 1.


def move_align_center():
    img_files = [f for f in os.listdir(imgs_path) if ".png" in f]

    for f in img_files:
        print("process: ", img_files.index(f))
        p = os.path.join(imgs_path, f)

        img = cv2.imread(p, 0)

        img = img_align_center(img)

        cv2.imwrite(p, img)


def img_align_center(img):
    if img is None:
        print("img is none!")
        return

    x, y, w, h = getSingleMaxBoundingBoxOfImage(img)
    cent_x = x + int(w / 2)
    cent_y = y + int(h / 2)

    bk = createBlankGrayscaleImageWithSize(img.shape)

    offset_x = 128 - cent_x
    offset_y = 128 - cent_y

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x] == 0:
                bk[y+offset_y][x+offset_x] = img[y][x]

    return bk



def ssim_test():
    src = os.path.join(temp_path, "temp_2.png")
    tag = os.path.join(imgs_path, "齷_9F77_stroke_14.png")

    src_img = cv2.imread(src, 0)
    tag_img = cv2.imread(tag, 0)

    # ssim = get_ssim(src_img, tag_img)
    # print("ssim: ", ssim)

    ssim = compare_ssim(src_img, tag_img, tag_img.max() - tag_img.min())
    print("ssim: ", ssim)



if __name__ == '__main__':
    move_align_center()
    # fanti_strokes_class()
    # ssim_test()

    # src = os.path.join(imgs_path, "駿_99FF_stroke_5.png")
    #
    # img = cv2.imread(src, 0)
    #
    # bk = img_align_center(img)
    #
    # cv2.imshow("bk", bk)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


