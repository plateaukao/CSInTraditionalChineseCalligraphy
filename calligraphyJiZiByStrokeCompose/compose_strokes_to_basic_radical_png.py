# coding: utf-8
import os
import cv2

from utils.Functions import createBlankGrayscaleImageWithSize

char_1000_path = "../../../Data/Calligraphy_database/Chars_1000"


def recompose_strokes_to_basic_radical_png():
    char_names = [f for f in os.listdir(char_1000_path) if '.' not in f]
    print(len(char_names))

    for cn in char_names:
        print(cn)
        radical_names = [f for f in os.listdir(os.path.join(char_1000_path, cn, 'basic radicals')) if '.' not in f]
        print(radical_names)

        for rn in radical_names:

            bk_ = createBlankGrayscaleImageWithSize((256, 256))

            stroke_names = [f for f in os.listdir(os.path.join(char_1000_path, cn, 'basic radicals', rn)) if '.png' in f]
            if len(stroke_names) == 0:
                print(cn, ' ', rn, ' not found!')
                continue

            for sn in stroke_names:
                img_ = cv2.imread(os.path.join(char_1000_path, cn, 'basic radicals', rn, sn), 0)
                for x in range(img_.shape[0]):
                    for y in range(img_.shape[1]):
                        if img_[x][y] == 0:
                            bk_[x][y] = 0

            cv2.imwrite(os.path.join(os.path.join(char_1000_path, cn, 'basic radicals', rn + '.png')), bk_)


        # break


if __name__ == '__main__':
    recompose_strokes_to_basic_radical_png()