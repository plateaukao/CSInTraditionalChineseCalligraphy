# coding: utf-8
import cv2
import os


def storke_png_resize():
    path = "../../Data/svgs_stroke"

    saved_path = "../../Data/Strokes_png"

    list_files = os.listdir(path)
    png_files = []
    for fl in list_files:
        print("process: ", list_files.index(fl))
        if ".png" in fl:
            img = cv2.imread(os.path.join(path, fl), 0)
            if img is None:
                print("img is none!")
                continue

            img_resized = cv2.resize(img, (256, 256), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(saved_path, fl), img_resized)


if __name__ == '__main__':
    storke_png_resize()