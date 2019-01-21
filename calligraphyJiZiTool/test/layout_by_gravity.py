# coding: utf-8
import cv2
import os
import numpy as np
import math

from utils.Utils import getSingleMaxBoundingBoxOfImage, getCenterOfGravity


def create_doufang_template(images, word_space, column_space, num_per_column, x_offset=100, y_offset=100):
    """
    Create tempalte for doufang .
    :param images:
    :param word_space:
    :param column_space:
    :param num_per_column:
    :return:
    """
    if images is None:
        return

    count = len(images)

    column_num = np.ceil(count / num_per_column)

    # change rectangle image to square
    images_squares = []
    for i in range(len(images)):
        img = images[i]

        x0, y0, w, h = getSingleMaxBoundingBoxOfImage(img)

        rect = img[y0: y0+h, x0: x0+w]
        new_w = max(w, h)

        new_rect = np.ones((new_w, new_w)) * 255
        print('rect shape:', rect.shape, 'new_rect:', new_rect.shape)
        if w > h:
            new_rect[int((w-h)/2): int((w-h)/2) + h, 0: w] = rect
        else:
            new_rect[0: h, int((h-w)/2): int((h-w)/2) + w] = rect

        images_squares.append(new_rect)

    # resize all images squares with same size
    images_squares_resized = []
    new_size = 0
    for i in range(len(images_squares)):
        new_size += images_squares[i].shape[0]

    # new size of square is the mean value of all squares
    new_size = int(new_size / len(images_squares) * 0.5)
    print(new_size)

    for i in range(len(images_squares)):
        img = images_squares[i]
        img = cv2.resize(img, (new_size, new_size))
        images_squares_resized.append(img)

    del images_squares

    row_num = num_per_column

    word_space_dist = 0
    column_space_dist = 0

    word_space_mode = "thick"
    if word_space > 33 and word_space < 66:
        word_space_mode = "normal"
        word_space_dist = int(new_size * 0.3)
    elif word_space >= 66:
        word_space_mode = "sparse"
        word_space_dist = int(new_size * 0.6)

    column_space_mode = "thick"
    if column_space > 33 and column_space < 66:
        column_space_mode = "normal"
        column_space_dist = int(new_size * 0.6)
    elif column_space > 66:
        column_space_mode = "sparse"
        column_space_dist = int(new_size * 0.8)

    # create bk image with new_size, column_num, and row_num
    bk_w = int(new_size * (2 * column_num + 1))
    bk_h = int(new_size * (2 * row_num + 1))

    bk = np.array(np.ones((bk_h, bk_w)) * 255, dtype=np.uint8)
    bk_rgb = cv2.cvtColor(bk, cv2.COLOR_GRAY2RGB)
    print('bk shape:', bk.shape)

    # layout of all characters
    for i in range(1, len(images_squares_resized) + 1):
        print('process', i)
        column_id = math.ceil(i / num_per_column)
        row_id = i % num_per_column
        if row_id == 0:
            row_id = num_per_column
        print('colu %d row %d' % (column_id, row_id))

        insert_pos_y = int(y_offset / 2) + (row_id - 1) * new_size + (row_id - 1) * word_space_dist
        insert_pos_x = bk.shape[1] - int(x_offset / 2) - column_id * new_size - (column_id - 1) * column_space_dist

        print('insert pos:', (insert_pos_y, insert_pos_x))
        print('bk rect:', bk[insert_pos_y: insert_pos_y + new_size, insert_pos_x: insert_pos_x + new_size].shape)
        bk[insert_pos_y: insert_pos_y + new_size, insert_pos_x: insert_pos_x + new_size] = images_squares_resized[i - 1]

    return bk


def create_doufang_template_by_gravity_alignment(images, word_space, column_space, num_per_column, x_offset=100, y_offset=100):
    """
        Create tempalte for doufang .
        :param images:
        :param word_space:
        :param column_space:
        :param num_per_column:
        :return:
        """
    if images is None:
        return

    count = len(images)
    column_num = int(np.ceil(count / num_per_column))
    row_num = num_per_column

    # change rectangle image to square
    images_squares = []
    for i in range(len(images)):
        img = images[i]

        x0, y0, w, h = getSingleMaxBoundingBoxOfImage(img)

        rect = img[y0: y0 + h, x0: x0 + w]
        new_w = max(w, h)

        new_rect = np.ones((new_w, new_w)) * 255
        print('rect shape:', rect.shape, 'new_rect:', new_rect.shape)
        if w > h:
            new_rect[int((w - h) / 2): int((w - h) / 2) + h, 0: w] = rect
        else:
            new_rect[0: h, int((h - w) / 2): int((h - w) / 2) + w] = rect

        images_squares.append(new_rect)

    # resize all images squares with same size
    images_squares_resized = []
    new_size = 0
    for i in range(len(images_squares)):
        new_size += images_squares[i].shape[0]

    # new size of square is the mean value of all squares
    new_size = int(new_size / len(images_squares) * 0.5)

    for i in range(len(images_squares)):
        img = images_squares[i]
        img = cv2.resize(img, (new_size, new_size))
        images_squares_resized.append(img)

    del images_squares

    word_space_dist = 0
    column_space_dist = 0

    word_space_mode = "thick"
    if word_space > 33 and word_space < 66:
        word_space_mode = "normal"
        word_space_dist = int(new_size * 0.3)
    elif word_space >= 66:
        word_space_mode = "sparse"
        word_space_dist = int(new_size * 0.6)

    column_space_mode = "thick"
    if column_space > 33 and column_space < 66:
        column_space_mode = "normal"
        column_space_dist = int(new_size * 0.6)
    elif column_space > 66:
        column_space_mode = "sparse"
        column_space_dist = int(new_size * 0.8)

    # create bk image with new_size, column_num, and row_num
    bk_w = int(new_size * (2 * column_num + 1))
    bk_h = int(new_size * (2 * row_num + 1))

    bk = np.array(np.ones((bk_h, bk_w)) * 255, dtype=np.uint8)
    bk_rgb = cv2.cvtColor(bk, cv2.COLOR_GRAY2RGB)
    print('bk shape:', bk.shape)

    # set up the first row characters
    first_row_gravity = []
    first_row_insert_x = []
    for i in range(column_num):
        img_ = images_squares_resized[i * num_per_column]
        # get gravity of img
        goc_x, goc_y = getCenterOfGravity(img_)

        insert_pos_x = bk.shape[1] - int(x_offset / 2) - (i + 1) * new_size - i * column_space_dist
        insert_pos_y = int(y_offset / 2)

        # set goc x and y
        goc_x += insert_pos_x
        goc_y += insert_pos_y
        first_row_gravity.append([goc_x, goc_y])

        bk[insert_pos_y: insert_pos_y + new_size, insert_pos_x: insert_pos_x + new_size] = img_

        cv2.circle(bk, (goc_x, goc_y), 3, 0, 2)
    print(first_row_gravity)

    # set up last other characters
    for i in range(len(images_squares_resized)):
        if i % num_per_column == 0:
            # first image of each column not process
            continue

        column_id = math.ceil(i / num_per_column)
        row_id = i % num_per_column
        print("rod_id:", row_id)

        img_ = images_squares_resized[i]

        goc_x, goc_y = getCenterOfGravity(img_)

        goc_x_offset = new_size - goc_x
        goc_y_offset = new_size - goc_y

        print("column id:", column_id, " ", first_row_gravity[column_id-1][0])
        insert_pos_x = first_row_gravity[column_id-1][0] - goc_x

        insert_pos_y = row_id * new_size + int(y_offset/2) + row_id * word_space_dist
        print("word space dist: ", word_space_dist)

        bk[insert_pos_y: insert_pos_y + new_size, insert_pos_x: insert_pos_x + new_size] = img_

        cv2.circle(bk, (insert_pos_x + goc_x, insert_pos_y + goc_y), 3, 0, 2)

    return bk


if __name__ == '__main__':

    images = []

    path = "../../../Data/Calligraphy_database_test/layout_test"

    file_list = os.listdir(path)
    if file_list is None:
        print("can not find image files")

    img_names = []
    for fl in file_list:
        if ".png" in fl:
            img_names.append(fl)
    print(img_names)

    content = "白日依山尽黄河入海流欲"
    img_names_sorted = []
    for i in range(len(content)):
        ct = content[i]
        for nm in img_names:
            if ct in nm:
                img_names_sorted.append(nm)
    print(img_names_sorted)

    for nm in img_names_sorted:
        url = os.path.join(path, nm)
        img_ = cv2.imread(url, 0)
        images.append(img_)
    print("image len:", len(images))

    word_space = 80
    column_space = 70
    num_per_column = 5
    alignment_mode = "gravity"

    bk = create_doufang_template_by_gravity_alignment(images, word_space, column_space, num_per_column)
    # bk = create_doufang_template(images, word_space, column_space, num_per_column)

    # bk = images[3]
    #
    # gocx, gocy = getCenterOfGravity(bk)
    #
    # cv2.circle(bk, (gocx, gocy), 3, 255, 2)

    cv2.imshow("bk", bk)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
