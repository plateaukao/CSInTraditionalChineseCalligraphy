# coding: utf-8
import os
import copy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom


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


def extract_path(svg_path):
    if svg_path == "":
        print("svg path should not be none!")
        return

    # get file name
    file_name = svg_path.replace(".svg", "")

    # open svg file
    dom = minidom.parse(svg_path)

    # find path element in original svg file
    root = dom.documentElement
    path_elems = root.getElementsByTagName("path")
    if path_elems is None:
        print("not find path elements")
        return
    print("path elements len: ", len(path_elems))

    for i in range(len(path_elems)):
        dom_, path_parent_elem = create_blank_svg(copy.deepcopy(dom))
        path_parent_elem.appendChild(path_elems[i])

        data_xml = dom_.toxml()

        with open(("%s_stroke_%d.svg" % (file_name, i)), 'w') as f:
            f.write(data_xml)


if __name__ == '__main__':
    path = "月svg01.svg"
    extract_path(path)