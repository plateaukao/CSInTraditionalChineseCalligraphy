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

    cent_x0 = int(post[0] + post[2] / 2)
    cent_y0 = int(post[1] + post[3] / 2)

    similar_image_ssim_dict = {}
    for t_name in temp_bs_names:
        t_img_path = os.path.join(bs_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        _, t_img = cv2.threshold(t_img, 127, 255, cv2.THRESH_BINARY)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        cent_x = int(x + w / 2)
        cent_y = int(y + h / 2)

        loc_ssim = abs(cent_x0 - cent_x) + abs(cent_y0 - cent_y)
        size_ssim = abs(w - post[2]) + abs(h - post[3])

        total_ssim = 0.5 * loc_ssim + 0.5 * size_ssim

        if total_ssim <= threshold:
            similar_image_ssim_dict[t_name] = total_ssim


    # sorted find images based on the total ssim
    if len(similar_image_ssim_dict) > 0:
        dict_sorted_list = [(k, similar_image_ssim_dict[k]) for k in sorted(similar_image_ssim_dict,\
                            key=similar_image_ssim_dict.get)]

        for k, _ in dict_sorted_list:
            similar_bs_names.append(k)

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

    similar_image_ssim_dict = {}
    for t_name in temp_bs_names:
        t_img_path = os.path.join(bs_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        _, t_img = cv2.threshold(t_img, 127, 255, cv2.THRESH_BINARY)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        size_ssim = abs(w - post[2]) + abs(h - post[3])
        if size_ssim <= threshold:
            similar_image_ssim_dict[t_name] = size_ssim

    # sorted
    if len(similar_image_ssim_dict) > 0:
        dict_sorted_list = [(k, similar_image_ssim_dict[k]) for k in sorted(similar_image_ssim_dict, \
                                                                            key=similar_image_ssim_dict.get)]
        for k, _ in dict_sorted_list:
            similar_bs_names.append(k)

    return similar_bs_names


def find_similar_strokes_img_names_with_same_position_and_size(post, stroke_type_path, threshold=5):
    if post is None or stroke_type_path == "" or not os.path.exists(stroke_type_path):
        return []

    temp_sk_names = [f for f in os.listdir(stroke_type_path) if ".png" in f]
    print("temp sk image num:", len(temp_sk_names))

    similar_sk_names = []

    cent_x0 = int(post[0] + post[2] / 2)
    cent_y0 = int(post[1] + post[3] / 2)

    similar_image_ssim_dict = {}
    for t_name in temp_sk_names:
        t_img_path = os.path.join(stroke_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        _, t_img = cv2.threshold(t_img, 127, 255, cv2.THRESH_BINARY)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        cent_x = int(x + w / 2)
        cent_y = int(y + h / 2)

        loc_ssim = abs(cent_x0 - cent_x) + abs(cent_y0 - cent_y)
        size_ssim = abs(w - post[2]) + abs(h - post[3])

        total_ssim = 0.5 * loc_ssim + 0.5 * size_ssim

        if total_ssim <= threshold:
            similar_image_ssim_dict[t_name] = total_ssim

    # sorted find images based on the total ssim
    if len(similar_image_ssim_dict) > 0:
        dict_sorted_list = [(k, similar_image_ssim_dict[k]) for k in sorted(similar_image_ssim_dict, \
                                                                                    key=similar_image_ssim_dict.get)]

        for k, _ in dict_sorted_list:
            similar_sk_names.append(k)

    return similar_sk_names


def find_similar_strokes_img_names_with_same_size(post, stroke_type_path, threshold=5):
    if post is None or stroke_type_path == "" or not os.path.exists(stroke_type_path):
        return []

    temp_sk_names = [f for f in os.listdir(stroke_type_path) if ".png" in f]
    print("temp sk image num:", len(temp_sk_names))

    similar_sk_names = []

    similar_image_ssim_dict = {}
    for t_name in temp_sk_names:
        t_img_path = os.path.join(stroke_type_path, t_name)
        t_img = cv2.imread(t_img_path, 0)
        _, t_img = cv2.threshold(t_img, 127, 255, cv2.THRESH_BINARY)
        x, y, w, h = getSingleMaxBoundingBoxOfImage(t_img)

        size_ssim = abs(w - post[2]) + abs(h - post[3])
        if size_ssim <= threshold:
            similar_image_ssim_dict[t_name] = size_ssim

    # sorted
    if len(similar_image_ssim_dict) > 0:
        dict_sorted_list = [(k, similar_image_ssim_dict[k]) for k in sorted(similar_image_ssim_dict, \
                                                                key=similar_image_ssim_dict.get)]

        for k, _ in dict_sorted_list:
            similar_sk_names.append(k)

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

