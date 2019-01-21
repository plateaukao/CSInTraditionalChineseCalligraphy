# coding: utf-8
import os
import cv2


def get_file_names(text, dataset_path, font):
    """
    Get all image file image_names of one font in dataset.
    :param text:
    :param dataset_path:
    :param font:
    :return:
    """

    if text == "" or dataset_path == "" or font == "":
        return []

    # text len
    text_count = len(text)
    image_names = ["" for _  in range(text_count)]
    print("name len: ", len(image_names))

    # all font images name
    all_font_names = []
    files = os.listdir(os.path.join(dataset_path, font))
    for fl in files:
        if ".png" in fl:
            all_font_names.append(fl)
    print("all %s images name len: %d" % (font, len(all_font_names)))

    not_find_flag = False

    for i in range(text_count):
        ch = text[i]
        for name_ in all_font_names:
            if ch in name_:
                image_names[i] = os.path.join(dataset_path, font, name_)
                break

        if image_names[i] == "":
            # not find image name of this char
            not_find_flag = True

    if not_find_flag:

        all_kai_names = []
        files = os.listdir(os.path.join(dataset_path, "kai"))
        for fl in files:
            if ".png" in fl:
                all_kai_names.append(fl)
        print("all kai iamges name len: ", len(all_kai_names))

        for i in range(len(image_names)):
            if image_names[i] == "":
                ch = text[i]

                for name_ in all_kai_names:
                    if ch in name_:
                        image_names[i] = os.path.join(dataset_path, "kai", name_)

    print("image names:", image_names)

    return image_names


def getSingleMaxBoundingBoxOfImage(image):
    """
    Calculate the coordinates(x, y, w, h) of single maximizing bounding rectangle boxing of grayscale image
    of character, in order to using this bounding box to select the region of character.
    :param image: grayscale image of character.
    :return: coordinates(x, y, w, h) of single maximizing bounding boxing.
    """
    if image is None:
        return None

    HEIGHT = image.shape[0]
    WIDTH = image.shape[1]

    # moments
    im2, contours, hierarchy = cv2.findContours(image, 1, 2)

    minx = WIDTH
    miny = HEIGHT
    maxx = 0
    maxy = 0
    # Bounding box
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        print(x, y, w, h)

        if w > 0.99 * WIDTH and h > 0.99 * HEIGHT:
            continue
        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x + w, maxx)
        maxy = max(y + h, maxy)

    return minx, miny, maxx - minx, maxy - miny


def getCenterOfGravity(image):
    """
    Get the center of gravity of image.
    :param image: grayscale image of character.
    :return: (x, y), the coordinate of center of gravity of image.
    """
    src_cog_x = 0;
    src_cog_y = 0
    total_pixels = 0
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if image[y][x] == 0.0:
                src_cog_x += x
                src_cog_y += y
                total_pixels += 1

    src_cog_x = int(src_cog_x / total_pixels)
    src_cog_y = int(src_cog_y / total_pixels)
    return src_cog_x, src_cog_y