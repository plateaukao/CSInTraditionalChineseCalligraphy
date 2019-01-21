import cv2
import numpy as np
import math

from utils.Utils import getSingleMaxBoundingBoxOfImage


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
        word_space_dist = int(new_size * 0.1)
    elif word_space >= 66:
        word_space_mode = "sparse"
        word_space_dist = int(new_size * 0.2)

    column_space_mode = "thick"
    if column_space > 33 and column_space < 66:
        column_space_mode = "normal"
        column_space_dist = int(new_size * 0.4)
    elif column_space > 66:
        column_space_mode = "sparse"
        column_space_dist = int(new_size * 0.6)

    bk_w = int(new_size * column_num + column_space_dist * (column_num - 1) + x_offset)
    bk_h = int(new_size * row_num + word_space_dist * (row_num - 1) + y_offset)

    bk = np.ones((bk_h, bk_w)) * 255
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
