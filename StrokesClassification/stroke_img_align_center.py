# coding: utf-8
import cv2
import os

from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImage


def stroke_img_align_center():
    img_path = '/Users/liupeng/Documents/Data/Strokes_png'
    save_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images'

    filenames = [f for f in os.listdir(img_path) if '.png' in f]
    print('Files count: ', len(filenames))

    for i in range(len(filenames)):
        print("procsss: ", i)
        path_ = os.path.join(img_path, filenames[i])
        img_ = cv2.imread(path_, 0)
        if img_ is None:
            continue
        x, y, w, h = getSingleMaxBoundingBoxOfImage(img_)
        blank_ = createBlankGrayscaleImage(img_)

        # blank_[]

        blank_[128 - int(h / 2): 128 - int(h / 2) + h, 128 - int(w / 2): 128 - int(w / 2) + w] = img_[y:y + h, x:x + w]

        cv2.imwrite(os.path.join(save_path,filenames[i]), blank_)




if __name__ == '__main__':
    stroke_img_align_center()

