# coding: utf-8
import json
import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


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

        content = '<svg version="1.1" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n <g transform="scale(1, -1) translate(0, -900)"> \n'

        for j in range(num_strokes):
            sk_path = strokes[j]

            content += '<path d="' + sk_path + '" fill="black"></path> \n'

        content += '</g></svg>'
        with open(os.path.join(save_path, (tag + "_" + code + ".svg")), 'w') as f:
            f.write(content)

        drawing = svg2rlg(os.path.join(save_path, (tag + "_" + code + ".svg")))
        if drawing is None:
            print("drawing is None!")
        renderPM.drawToFile(drawing, os.path.join(save_path, (tag + "_" + code + ".png")), "png")

        print(tag, ": ", len(strokes))


if __name__ == '__main__':
    path = "../../../Data/graphics.txt"
    save_path = "../../../Data/SVGs_中文"
    extract_stroke_from_graphics_file(path, save_path)
