# coding: utf-8
import json
import os
import cv2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from utils.Functions import prettyXml


def extract_stroke_from_graphics_file(path, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # load json data from graphics.txt
    json_data = None
    with open(path, 'r') as f:
        json_data = json.load(f)
    print(len(json_data))

    # parse json data: character and strokes path
    for i in range(len(json_data)):
        print("process: ", i)
        data = json_data[i]

        tag = data["character"]
        strokes = data["strokes"]
        code = tag.encode("unicode_escape").decode("utf-8").replace("\\u", "").upper()
        print(code)

        num_strokes = len(strokes)

        for j in range(num_strokes):
            sk_path = strokes[j]

            content = '<svg version="1.1" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n <g transform="scale(1, -1) translate(0, -900)"><path d="' + sk_path + \
                      '" fill="black"></path></g></svg>'
            with open(os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".svg")), 'w') as f:
                f.write(content)

            drawing = svg2rlg(os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".svg")))
            if drawing is None:
                print("drawing is None!")
            renderPM.drawToFile(drawing, os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".png")), "png")
            img = cv2.imread(os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".png")), 0)
            img = cv2.resize(img, (256, 256))
            cv2.imwrite(os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".png")))

            os.remove(os.path.join(save_path, (tag + "_" + code + "_" + str(j) + ".svg")))

        print(tag, ": ", len(strokes))


if __name__ == '__main__':
    path = "../../Data/graphics.txt"
    save_path = "../../../Data/Calligraphy_database/Stroke_pngs"
    extract_stroke_from_graphics_file(path, save_path)
