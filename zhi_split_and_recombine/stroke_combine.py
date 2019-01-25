# coding: utf-8
import cv2
import os
import random

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize


def merge_image(source, target):
    if source.shape != target.shape:
        print("source shape is not same as the target!")
        return

    for i in range(target.shape[0]):
        for j in range(target.shape[1]):
            if source[i][j] == 0:
                target[i][j] = 0
    return target


def combine():
    path1 = '/Users/liupeng/Documents/Data/兰亭序-之/original/zhi1'
    path2 = '/Users/liupeng/Documents/Data/兰亭序-之/original/zhi4'
    path3 = '/Users/liupeng/Documents/Data/兰亭序-之/original/zhi13'
    path4 = '/Users/liupeng/Documents/Data/兰亭序-之/original/zhi12'

    save_img_path = '/Users/liupeng/Documents/Data/兰亭序-之/save_resluts'

    img1 = cv2.imread(os.path.join(path1, 'original.png'), 0)
    print(img1.shape)
    img2 = cv2.imread(os.path.join(path2, 'original.png'), 0)
    print(img2.shape)
    img3 = cv2.imread(os.path.join(path3, 'original.png'), 0)
    print(img3.shape)

    img4 = cv2.imread(os.path.join(path4, 'original.png'), 0)
    print(img4.shape)

    x1, y1, w1, h1 = getSingleMaxBoundingBoxOfImage(img1)
    print(x1, y1, w1, h1)
    x2, y2, w2, h2 = getSingleMaxBoundingBoxOfImage(img2)
    print(x2, y2, w2, h2)
    x3, y3, w3, h3 = getSingleMaxBoundingBoxOfImage(img3)
    print(x3, y3, w3, h3)

    x4, y4, w4, h4 = getSingleMaxBoundingBoxOfImage(img4)

    new_h = max(img1.shape[0], img2.shape[0], img3.shape[0], img4.shape[0])
    new_w = max(img1.shape[1], img2.shape[1], img3.shape[1], img4.shape[1])

    print(new_w, ' ', new_h)

    img1_strokes = []
    for i in range(1, 5):
        img_ = cv2.imread(os.path.join(path1, '%d.png' % i), 0)

        blank_ = createBlankGrayscaleImageWithSize((new_h, new_w))

        blank_[int(new_h/2)-int(h1/2): int(new_h/2)-int(h1/2)+h1, int(new_w/2)-int(w1/2): int(new_w/2)-int(w1/2)+w1] = \
            img_[y1: y1+h1, x1: x1+w1]

        img1_strokes.append(blank_)
    print('img1 stroke num: ', len(img1_strokes))

    img2_strokes = []
    for i in range(1, 5):
        img_ = cv2.imread(os.path.join(path2, '%d.png' % i), 0)

        blank_ = createBlankGrayscaleImageWithSize((new_h, new_w))

        blank_[int(new_h / 2) - int(h2 / 2): int(new_h / 2) - int(h2 / 2) + h2,
        int(new_w / 2) - int(w2 / 2): int(new_w / 2) - int(w2 / 2) + w2] = \
            img_[y2: y2 + h2, x2: x2 + w2]

        img2_strokes.append(blank_)
    print('img2 stroke num: ', len(img2_strokes))

    img3_strokes = []
    for i in range(1, 5):
        img_ = cv2.imread(os.path.join(path3, '%d.png' % i), 0)

        blank_ = createBlankGrayscaleImageWithSize((new_h, new_w))

        blank_[int(new_h / 2) - int(h3 / 2): int(new_h / 2) - int(h3 / 2) + h3,
        int(new_w / 2) - int(w3 / 2): int(new_w / 2) - int(w3 / 2) + w3] = \
            img_[y3: y3 + h3, x3: x3 + w3]

        img3_strokes.append(blank_)
    print('img3 stroke num: ', len(img3_strokes))

    img4_strokes = []
    for i in range(1, 5):
        img_ = cv2.imread(os.path.join(path4, '%d.png' % i), 0)

        blank_ = createBlankGrayscaleImageWithSize((new_h, new_w))

        blank_[int(new_h / 2) - int(h4 / 2): int(new_h / 2) - int(h4 / 2) + h4,
        int(new_w / 2) - int(w4 / 2): int(new_w / 2) - int(w4 / 2) + w4] = \
            img_[y4: y4 + h4, x4: x4 + w4]

        img4_strokes.append(blank_)
    print('img4 stroke num: ', len(img4_strokes))

    # combine images
    index_combine_set = set()

    # all combine result of index of image
    while True:
        if len(index_combine_set) >= 256:
            break
        index_list = []
        for i in range(4):
            index_list.append(random.randint(1, 4))
        index_combine_set.add(tuple(index_list))

    # index_combine_list = list
    combine_results = []
    index = 0
    for item in index_combine_set:
        blank_ = createBlankGrayscaleImageWithSize((new_h, new_w))

        # add 1st stroke
        id = item[0]
        stroke_img = None
        if id == 1:
            stroke_img = img1_strokes[0]
        elif id == 2:
            stroke_img = img2_strokes[0]
        elif id == 3:
            stroke_img = img3_strokes[0]
        elif id == 4:
            stroke_img = img4_strokes[0]

        blank_ = merge_image(stroke_img, blank_)


        # add 2ed stroke
        id = item[1]
        stroke_img = None
        if id == 1:
            stroke_img = img1_strokes[1]
        elif id == 2:
            stroke_img = img2_strokes[1]
        elif id == 3:
            stroke_img = img3_strokes[1]
        elif id == 4:
            stroke_img = img4_strokes[1]
        blank_ = merge_image(stroke_img, blank_)

        # add 3rd stroke
        id = item[2]
        stroke_img = None
        if id == 1:
            stroke_img = img1_strokes[2]
        elif id == 2:
            stroke_img = img2_strokes[2]
        elif id == 3:
            stroke_img = img3_strokes[2]
        elif id == 4:
            stroke_img = img4_strokes[2]
        blank_ = merge_image(stroke_img, blank_)

        # add 4th stroke
        id = item[3]
        stroke_img = None
        if id == 1:
            stroke_img = img1_strokes[3]
        elif id == 2:
            stroke_img = img2_strokes[3]
        elif id == 3:
            stroke_img = img3_strokes[3]
        elif id == 4:
            stroke_img = img4_strokes[3]
        blank_ = merge_image(stroke_img, blank_)

        cv2.imwrite(os.path.join(save_img_path, 'result_4chars_%d.png' % index), blank_)
        index += 1








    # for i in range(len(img1_strokes)):
    #     cv2.imshow('%d img' % i, img1_strokes[i])
    #
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()








if __name__ == '__main__':
    combine()