# coding: utf-8
import cv2
import os
import numpy as np


def calculateCoverageRate(source, target):
    """
    Corverage rate calculation.
    :param source: grayscale image of source.
    :param target: grayscale image of target.
    :return: Coverage rate of source and target images.
    """
    p_valid = np.sum(255.0 - source) / 255.0

    if p_valid == 0.0:
        return 0.0

    diff = target - source

    p_less = np.sum(diff == 255.0)
    p_over = np.sum(diff == -255.0)

    cr = (p_valid - p_less - p_over) / p_valid * 100.0
    return cr



def stroke_cluster():
    stroke_path = '../../Data/Strokes_png'
    cluster_path = '../../Data/Strokes_png_cluster'

    if not os.path.exists(cluster_path):
        os.mkdir(cluster_path)

    names = [x for x in os.listdir(stroke_path) if '.png' in x]

    print(len(names))

    used_files = []

    stroke_clus = []

    for i in range(len(names)):
        print("process: ", i)
        x_name = names[i]
        if x_name in used_files:
            continue
        used_files.append(x_name)

        cluster = []

        x_img = cv2.imread(os.path.join(stroke_path, x_name), 0)

        for j in range(i+1, len(names)):
            y_name = names[j]
            if y_name in used_files:
                continue
            y_img = cv2.imread(os.path.join(stroke_path, y_name), 0)

            cr = calculateCoverageRate(x_img, y_img)

            if cr > 80:
                cluster.append(y_name)
        stroke_clus.append(cluster)

    print(len(stroke_clus))

    for i in range(len(stroke_clus)):
        cluster = stroke_clus[i]
        if len(cluster) == 1 or len(cluster) == 0:
            continue

        index_path = os.path.join(cluster_path, str(i))
        if not os.path.exists(index_path):
            os.mkdir(index_path)

        for item in cluster:
            img_ = cv2.imread(os.path.join(stroke_path, item), 0)
            cv2.imwrite(os.path.join(index_path, item), img_)



if __name__ == '__main__':
    stroke_cluster()