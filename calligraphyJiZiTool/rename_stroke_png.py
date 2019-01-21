# coding: utf-8
import os
import cv2


def rename_stroke_png():
    path = '../../Data/Strokes_png'

    save_path = '../../Data/Strokes_png_renamed'

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    names = [x for x in os.listdir(path) if '.png' in x]

    for i in range(len(names)):
        img_ = cv2.imread(os.path.join(path, names[i]))

        nm = names[i]
        new_nm = ''
        # remove the chinese character
        nms = nm.split('_')
        for j in range(1, len(nms)):
            if j == len(nms)-1:
                new_nm += nms[j]
            else:
                new_nm += nms[j] + '_'

        cv2.imwrite(os.path.join(save_path, new_nm), img_)

        # if i == 10:
        #     break


if __name__ == '__main__':
    rename_stroke_png()