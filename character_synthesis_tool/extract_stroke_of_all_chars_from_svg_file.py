# coding: utf-8
import json
import os
import cv2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from utils.Functions import prettyXml
from xml.dom import minidom
import copy


def create_blank_svg(dom):
    # create blank svg file by removing path element
    root = dom.documentElement

    path_elems = root.getElementsByTagName("path")
    if path_elems is None:
        print("not find path elements")
        return
    print("path elements len: ", len(path_elems))

    # path parent element
    path_parent_elem = None

    for e in path_elems:
        # find path parent element
        path_parent_elem = e.parentNode
        break

    for e in path_elems:
        path_parent_elem.removeChild(e)

    return dom, path_parent_elem


def extract_stroke_from_graphics_file(char_path, svg_path, save_path):
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # load json data from graphics.txt
    chars = []
    with open(char_path, "r") as f:
        for ch in f.readlines():
            chars.append(ch.strip())

    svg_names = [f for f in os.listdir(svg_path) if ".svg" in f]
    if len(svg_names) == 0:
        print("svg is none")
        return

    for i in range(len(chars)):
        ch = chars[i]
        code = ch.encode("unicode_escape").decode("utf-8").replace("\\u", "").upper()
        svg_name = ""
        for sn in svg_names:
            if ch in sn:
                svg_name = sn
                break
        if svg_name == "":
            print("{} not find svg file".format(ch))
            continue

        dom = minidom.parse(os.path.join(svg_path, svg_name))
        root = dom.documentElement
        path_elems = root.getElementsByTagName("path")
        if path_elems is None or len(path_elems) == 0:
            print("{} svg not find path".format(ch))
            continue

        for p_id in range(len(path_elems)):
            new_dom, path_parent_elem = create_blank_svg(copy.deepcopy(dom))
            path_parent_elem.appendChild(path_elems[p_id])
            data_xml = new_dom.toxml()

            svg_p = os.path.join(save_path, "{}_{}_{}.svg".format(ch, code, p_id))
            with open(svg_p, "w") as f:
                f.write(data_xml)

            # save to png
            drawing = svg2rlg(svg_p)
            if drawing is None:
                print("drawing is None!")
            png_p = os.path.join(save_path, "{}_{}_{}.png".format(ch, code, p_id))
            renderPM.drawToFile(drawing, png_p, "png")
            img = cv2.imread(png_p, 0)
            img = cv2.resize(img, (256, 256))
            cv2.imwrite(png_p, img)

            os.remove(svg_p)


if __name__ == '__main__':
    char_path = "chars.txt"
    svg_path = "../../../Data/Calligraphy_database/Chars_svg_files"
    save_path = "../../../Data/Calligraphy_database/Stroke_pngs"
    extract_stroke_from_graphics_file(char_path, svg_path, save_path)
