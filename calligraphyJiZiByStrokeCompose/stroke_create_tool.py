# coding: utf-8
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def stroke_create():
    """
        根据200个汉字的SVG文件，创建基本笔画库。 格式： 字_unicode_strokenumber.png
    """
    source_path = "../../../Data/Stroke_recomposed_tool/200svg chars dataset"
    save_path = "../../../Data/Stroke_recomposed_tool/200svg strokes dataset"

    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)

    # directory structure:  stroke_type/stroke.png
    stroke_types = ["卧钩", "横", "横折横折", "竖折", "弯钩", "横勾", "横折钩", "竖折折钩", "捺", "横折", "横撇", "竖折撇", "提",
                    "横折弯钩", "横撇弯钩", "竖折竖", "撇", "横折折折钩", "点", "竖提", "撇折", "横折折撇", "竖", "竖钩", "撇点",
                    "横折提", "竖弯", "斜钩", "横折横", "竖弯钩"]

    # for s in stroke_types:
    #     os.mkdir(os.path.join(save_path, s))

    all_char_stroke_dict = {}
    xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order.xml"
    # load radical data
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return

    root = tree.getroot()
    print("root len:", len(root))

    num_stroke_order = 0
    for child in root:
        ch = child.attrib["TAG"]
        if len(ch) > 1:
            continue

        stroke_order = ""
        stroke_order_elems = child.findall('STROKE_ORDER')
        if stroke_order_elems:
            stroke_order = stroke_order_elems[0].text

        if stroke_order != "" and stroke_order:
            stroke_order_split = stroke_order.split("|")
            if len(stroke_order_split) > 0:
                all_char_stroke_dict[ch] = stroke_order_split
    print(all_char_stroke_dict)

    # find all chars in 200 chars
    filenames = [f for f in os.listdir(source_path) if '.svg' in f]
    char_list = []
    for fn in filenames:
        if not '.svg' in fn:
            continue
        ch = fn.split('_')[0]
        char_list.append(ch)

    # find all stroke of all chars
    char_stroke_dict = {}
    for cl in char_list:
        if cl in all_char_stroke_dict:
            strokes = all_char_stroke_dict[cl]
            char_stroke_dict[cl] = strokes
    print(char_stroke_dict)

    # parse the xml and save to png file with stroke type
    for fn in filenames:
        if not '.svg' in fn:
            continue
        ch = fn.split('_')[0]
        ucode = ch.encode("unicode_escape").decode("utf-8").replace("\\u", "").upper()

        if not ch in char_stroke_dict:
            print(ch, 'not in char stroke dict')
            continue
        # parse the xml file to extract single stroke and save to png file
        file_path = os.path.join(source_path, fn)
        doc = minidom.parse(file_path)

        # 2. get path
        path_elems = [p for p in doc.getElementsByTagName("path")]
        print(len(path_elems))

        stroke_order = char_stroke_dict[ch]
        if len(path_elems) == len(stroke_order):
            print(ch, "same size")
            # save to stroke png file
            for i in range(len(path_elems)):
                p_elem = path_elems[i]
                d = p_elem.getAttribute('d')

                content = '<svg version="1.1" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n ' \
                          '<g transform="scale(1, -1) translate(0, -900)"><path d="' + d + \
                          '" fill="black"></path></g></svg>'

                with open(os.path.join(save_path, stroke_order[i], (ch + "_" + ucode + "_" + stroke_order[i] + "_" + str(i) + ".svg")), 'w') as f:
                    f.write(content)

                drawing = svg2rlg(os.path.join(save_path, stroke_order[i], (ch + "_" + ucode + "_" + stroke_order[i] + "_" + str(i) + ".svg")))
                renderPM.drawToFile(drawing, os.path.join(save_path, stroke_order[i], (ch + "_" + ucode + "_" + stroke_order[i] + "_" + str(i) + ".png")), "png")
        else:
            print(ch, ' not same size')







if __name__ == '__main__':
    stroke_create()



