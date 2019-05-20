# coding: utf-8
import os
import xml.etree.ElementTree as ET
from pdf_generation_of_2300_9300_chars.convert_char_to_unicode import char_to_unicode_str
from utils.Functions import prettyXml
from xml.dom import minidom
import copy
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import cv2


svg_path = "../../../Data/Calligraphy_database/SVGs_中文"
fanti_xml_path = "fanti_1830.xml"

xml_save_path = "fanti_1830_add_fantis.xml"

fanti_1830_path = "1672chars_fanti.txt"
xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals.xml"

def generate_fanti_1830_chars():
    svg_files = [f for f in os.listdir(svg_path) if ".svg" in f]

    fanti_chars = []
    with open(fanti_1830_path, "r") as f:
        for ch in f.readlines():
            fanti_chars.append(ch.strip())

    # get structure chars dict
    struct_dict = get_structure_char_map()

    # create xml data
    tree = ET.parse(fanti_xml_path)
    root = tree.getroot()

    for ch in fanti_chars:
        radical_elem = ET.Element("RADICAL")

        ucode = char_to_unicode_str(ch)

        radical_elem.set("ID", ucode)
        radical_elem.set("TAG", ch)

        type_elem = ET.SubElement(radical_elem, "TYPE")
        type_elem.text = "character"

        struct_info = get_struct_info(struct_dict, ch)
        struct_elem = ET.SubElement(radical_elem, "STRUCTURE")
        struct_elem.text = struct_info

        # stroke count
        sk_count = get_stroke_count_from_svg_file(ch)
        sk_count_elem = ET.SubElement(radical_elem, "STROKE_COUNT")
        sk_count_elem.text = str(sk_count)

        # stroke orders
        sk_orders = get_stroke_order_of_char_from_stroke_type_folder(ch)
        sk_orders_str = ""
        for s in sk_orders:
            if sk_orders.index(s) == len(sk_orders)-1:
                sk_orders_str += s
            else:
                sk_orders_str += s + "|"

        if sk_count == len(sk_orders):
            sk_orders_elem = ET.SubElement(radical_elem, "STROKE_ORDER")
            sk_orders_elem.text = sk_orders_str



        root.append(radical_elem)


    # perty xml
    prettyXml(root, '\t', '\n')
    tree.write(xml_save_path, encoding='utf-8')


def statistics_structure():
    structure_set = set()

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for child in root:
        struc_elems = child.findall("STRUCTURE")
        if struc_elems:
            structure_set.add(struc_elems[0].text.strip())

    print("struc num: ", len(structure_set))
    print(structure_set)

    struc_path = "../../../Data/Calligraphy_database/char structures"

    for ss in structure_set:
        os.mkdir(os.path.join(struc_path, ss))


def get_struct_info(struct_dict, ch):
    struct_info = ""

    for key in struct_dict.keys():
        chars = struct_dict[key]

        if ch in chars:
            struct_info = key
            break

    return struct_info


def get_structure_char_map():
    path = "../../../Data/Calligraphy_database/char structures"
    struct_files = [f for f in os.listdir(path) if "." not in f]
    print("struct num: ", len(struct_files))

    struct_dict = {}

    for sf in struct_files:
        p_ = os.path.join(path, sf)
        img_files = [f.replace(".png", "") for f in os.listdir(p_) if ".png" in f]

        struct_dict[sf] = img_files

    return struct_dict


def get_stroke_count_from_svg_file(ch):

    svg_files = [f for f in os.listdir(svg_path) if ".svg" in f]
    print("svg num: ", len(svg_files))

    svg_file = ""
    for sf in svg_files:
        if ch in sf:
            svg_file = sf
            break
    print("name: ", svg_file)

    if not os.path.exists(os.path.join(svg_path, svg_file)):
        print("svg file not exist!")
        return 0

    # open svg file
    dom = minidom.parse(os.path.join(svg_path, svg_file))

    # find path element in original svg file
    root = dom.documentElement
    path_elems = root.getElementsByTagName("path")

    return len(path_elems)


def extract_stroke_png_from_svg_files():
    svg_files = [f for f in os.listdir(svg_path) if ".svg" in f]

    fanti_chars = []
    with open(fanti_1830_path, "r") as f:
        for ch in f.readlines():
            fanti_chars.append(ch.strip())

    for fc in fanti_chars:
        for sf in svg_files:
            if fc in sf:
                svg_name = sf
                path = os.path.join(svg_path, svg_name)

                extract_png_path(path)




def extract_png_path(svg_path):
    if svg_path == "":
        print("svg path should not be none!")
        return

    # get file name
    file_name = svg_path.replace(".svg", "").split("/")[-1]

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

        with open(os.path.join("jianti_temp", "%s_stroke_%d.svg" % (file_name, i)), 'w') as f:
            f.write(data_xml)

        drawing = svg2rlg(os.path.join("jianti_temp", "%s_stroke_%d.svg" % (file_name, i)))
        renderPM.drawToFile(drawing, os.path.join("jianti_temp", "%s_stroke_%d.png" % (file_name, i)), "png")

        # del svg file
        os.system("rm {}".format(os.path.join("jianti_temp", "%s_stroke_%d.svg" % (file_name, i))))

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


def resize_image():
    path = "./jianti_temp"

    img_files = [f for f in os.listdir(path) if ".png" in f]
    print("img num: ", len(img_files))

    for f in img_files:
        print(f)
        img = cv2.imread(os.path.join(path, f), 0)
        img = cv2.resize(img, (256, 256), cv2.INTER_CUBIC)

        cv2.imwrite(os.path.join(path, f), img)

        # if img_files.index(f) == 10:
        #     break


def get_stroke_order_of_char_from_stroke_type_folder(ch=""):
    type_path = "../../../Data/Calligraphy_database/Stroke_types"

    type_folders = [f for f in os.listdir(type_path) if "." not in f]
    print(type_folders)

    # stroke type dict: type: images
    stroke_type_dict = {}

    for i in range(len(type_folders)):
        type = type_folders[i]

        img_names = [f for f in os.listdir(os.path.join(type_path, type)) if ".png" in f]
        stroke_type_dict[type] = img_names

    # search strokes for char
    stroke_imgs = []
    stroke_orders = []

    for key in stroke_type_dict.keys():
        names = stroke_type_dict[key]

        for name in names:
            if "{}_".format(ch) in name:
                stroke_imgs.append(name)
                stroke_orders.append(key)
                continue

    print(stroke_imgs)
    print(stroke_orders)

    # sort strokes
    stroke_orders_sorted = []
    for i in range(len(stroke_imgs)):
        for j in range(len(stroke_imgs)):
            name = stroke_imgs[j]

            if "stroke_{}.png".format(i) in name:
                stroke_orders_sorted.append(stroke_orders[j])
                break

    return stroke_orders_sorted






if __name__ == '__main__':
    generate_fanti_1830_chars()

    # statistics structure
    # statistics_structure()

    # get_structure_char_map()

    # count = get_stroke_count_from_svg_file("賤")
    # print("count: ", count)

    # extract_stroke_png_from_svg_files()

    # resize_image()
    # ch = "嫗"
    # stroke_orders = get_stroke_order_of_char_from_stroke_type_folder(ch)
    # print(stroke_orders)
