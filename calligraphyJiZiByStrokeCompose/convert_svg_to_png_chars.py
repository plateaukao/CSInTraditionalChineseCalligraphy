# coding: utf-8
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import cv2


svg_path = "../../../Data/SVGs_中文"
save_path = "../../../Data/SVG_2_PNG_chars"


def convert_svg_to_png_chars():

    svg_names = [f for f in os.listdir(svg_path) if ".svg" in f]

    count = 0
    for sn in svg_names:
        drawing = svg2rlg(os.path.join(svg_path, sn))

        if drawing is None:
            print("drawing is None!")
        renderPM.drawToFile(drawing, os.path.join(save_path, sn.replace('svg', 'png')), "png")

        count +=1
        print(count)

    count = 0
    for sn in svg_names:
        print(os.path.join(save_path, sn.replace('svg', 'png')))

        img_ = cv2.imread(os.path.join(save_path, sn.replace('svg', 'png')), 0)
        print(img_.shape)

        img_ = cv2.resize(img_, (256, 256))

        # cv2.resize(img_, (256, 256))
        cv2.imwrite(os.path.join(save_path, sn.replace('svg', 'png')), img_)

        count += 1
        print(count)


if __name__ == '__main__':
    convert_svg_to_png_chars()
