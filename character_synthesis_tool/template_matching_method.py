# coding: utf-8
import os
import cv2

from utils.Functions import getSingleMaxBoundingBoxOfImage


def find_similar_basic_radicals_img_names_with_same_position_and_size(post, bs_type_path, threshold=5):
    """
    Find the most similar bs with same position and size
    :param post:
    :param bs_type_path:
    :param threshold:
    :return:
    """
    if post is None or bs_type_path == "" or not os.path.exists(bs_type_path):
        return []

    temp_bs_names = [f for f in os.listdir(bs_type_path) if ".png" in f]
    print("temp bs image num: ", len(temp_bs_names))

    similar_bs_names = []

    print("post: ", post)

    min_x = min_y = min_w = min_h = 100000000
    for t_name in temp_bs_names:
        t_img_path = os.path.join(bs_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)
        print(t_name, x, y, w, h)

        # rule1
        if abs(x - post[0]) <= threshold and abs(y - post[1]) <= threshold and abs(w - post[2]) \
                <= threshold and abs(h - post[3]) <= threshold:
            similar_bs_names.append(t_name)

    return similar_bs_names


def find_similar_basic_radicals_img_names_with_same_size(post, bs_type_path, threshold=5):
    """
        Find the most similar bs with same size
        :param post:
        :param bs_type_path:
        :param threshold:
        :return:
        """
    if post is None or bs_type_path == "" or not os.path.exists(bs_type_path):
        return []

    temp_bs_names = [f for f in os.listdir(bs_type_path) if ".png" in f]
    print("temp bs image num: ", len(temp_bs_names))

    similar_bs_names = []

    for t_name in temp_bs_names:
        t_img_path = os.path.join(bs_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        # rule1
        if abs(w - post[2]) <= threshold and abs(h - post[3]) <= threshold:
            similar_bs_names.append(t_name)

    return similar_bs_names


def find_similar_strokes_img_names_with_same_position_and_size(post, stroke_type_path, threshold=5):
    if post is None or stroke_type_path == "" or not os.path.exists(stroke_type_path):
        return []

    temp_sk_names = [f for f in os.listdir(stroke_type_path) if ".png" in f]
    print("temp sk image num:", len(temp_sk_names))

    similar_sk_names = []
    for t_name in temp_sk_names:
        t_img_path = os.path.join(stroke_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        # rule1
        if abs(x - post[0]) <= threshold and abs(y - post[1]) <= threshold and abs(w - post[2]) \
                <= threshold and abs(h - post[3]) <= threshold:
            similar_sk_names.append(t_name)

    return similar_sk_names


def find_similar_strokes_img_names_with_same_size(post, stroke_type_path, threshold=5):
    if post is None or stroke_type_path == "" or not os.path.exists(stroke_type_path):
        return []

    temp_sk_names = [f for f in os.listdir(stroke_type_path) if ".png" in f]
    print("temp sk image num:", len(temp_sk_names))

    similar_sk_names = []
    for t_name in temp_sk_names:
        t_img_path = os.path.join(stroke_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        # rule1
        if abs(w - post[2]) <= threshold and abs(h - post[3]) <= threshold:
            similar_sk_names.append(t_name)

    # if not find same size stroke, return the most similar one stroke
    if len(similar_sk_names) == 0:
        similar_sk_names = find_most_similar_strokes(post, stroke_type_path)

    return similar_sk_names


def find_most_similar_strokes(post, stroke_type_path):
    if post is None or stroke_type_path == "" or not os.path.exists(stroke_type_path):
        return []

    temp_sk_names = [f for f in os.listdir(stroke_type_path) if ".png" in f]
    print("temp sk image num:", len(temp_sk_names))

    similar_sk_names = []
    similar_sk_id = 0
    min_dist = 10000000
    for t_name in temp_sk_names:
        t_img_path = os.path.join(stroke_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        dist = abs(w - post[2]) + abs(h - post[3])
        if dist < min_dist:
            min_dist = dist
            similar_sk_id = temp_sk_names.index(t_name)

    return similar_sk_names.append(temp_sk_names[similar_sk_id])

