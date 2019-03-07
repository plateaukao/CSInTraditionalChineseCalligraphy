# coding: utf-8
import os
import cv2
import math

from utils.Functions import createBlankGrayscaleImageWithSize


def merge_all_generation_images():
    img_path = "../../../Data/1000 generated results"

    filenames = [f for f in os.listdir(img_path) if ".png" in f]
    print("image num: ", len(filenames))

    bk = createBlankGrayscaleImageWithSize((4000, 4000))

    for i in range(len(filenames[:1000])):
        page_id = math.floor(i / 100)
        print(page_id)

        id = i - page_id * 100
        img_ = cv2.imread(os.path.join(img_path, filenames[i]), 0)

        row = math.floor(id / 10)
        col = id % 10
        bk[row * 400: (row + 1) * 400, col * 400: (col + 1) * 400] = img_

        if (i+1) % 100 == 0:
            cv2.imwrite("../../../Data/1000 merged result/all_merged_%d.png" % page_id, bk)

            bk = createBlankGrayscaleImageWithSize((4000, 4000))

        else:

            continue


def merge_diff_generation_real_images():
    img_path = "../../../Data/1000 generated results"

    kai_path = "../../../Data/Calligraphy_database/kai"

    filenames = [f for f in os.listdir(img_path) if ".png" in f]
    print("filenames len: ", len(filenames))

    kainames = [f for f in os.listdir(kai_path) if ".png" in f]

    bk = createBlankGrayscaleImageWithSize((2400, 1600))

    for i in range(len(filenames[: 1000])):
        page_id = math.floor(i / 12)
        print(page_id)

        fname = filenames[i]
        tag = fname.split("_")[0]
        print(tag)

        kai_img_path = ""
        # find real kai image
        for kn in kainames:
            kai_tag = kn.split("_")[0]
            if tag == kai_tag:
                kai_img_path = os.path.join(kai_path, kn)
                break
        if kai_img_path == "":
            print(tag, "not find real kai image")
            continue

        # open kai img
        kai_img = cv2.imread(kai_img_path, 0)

        new_kai_img = createBlankGrayscaleImageWithSize((400, 400))
        new_kai_img[72: 328, 72: 328] = kai_img

        # kai_img = cv2.resize(kai_img, (400, 400))

        img = cv2.imread(os.path.join(img_path, filenames[i]), 0)

        id = i - page_id * 12

        row = math.floor(id / 2)
        col = id % 2

        print(row, col)

        if col == 0:
            bk[row * 400: (row + 1) * 400, col * 400: (col + 1) * 400] = img
            bk[row * 400: (row + 1) * 400, (col+1) * 400: (col + 2) * 400] = new_kai_img
        else:
            bk[row * 400: (row + 1) * 400, (col+1) * 400: (col + 2) * 400] = img
            bk[row * 400: (row + 1) * 400, (col + 2) * 400: (col + 3) * 400] = new_kai_img

        if (i+1) % 12 == 0:
            cv2.imwrite("../../../Data/1000 merged result/all_merged_diff_%d.png" % page_id, bk)

            bk = createBlankGrayscaleImageWithSize((2400, 1600))

        else:

            continue



    #

    #
    #     row = math.floor(i / 2)
    #     col = i % 2
    #
    #     print(row, col)
    #
    #     bk[row * 400: (row + 1) * 400, col * 400: (col + 1) * 400] = img
    #     bk[row * 400: (row + 1) * 400, (col+1) * 400: (col + 2) * 400] = kai_img
    #
    # cv2.imwrite("../../../Data/1000 merged result/all_merged_diff_.png", bk)


if __name__ == '__main__':
    # merge_all_generation_images()
    merge_diff_generation_real_images()