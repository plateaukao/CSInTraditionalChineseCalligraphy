# coding: utf-8
import xml.etree.ElementTree as ET
import ast
from utils.Functions import getSingleMaxBoundingBoxOfImage, createBlankGrayscaleImageWithSize


def query_similar_basic_radicals_and_strokes(basic_radicals_dataset, strokes_dataset, char_info_list):
    """
    Find similar basic radicals and strokes.

    :param basic_radicals_dataset:
    :param strokes_dataset:
    :param char_info_list:
    :return:
    """
    if basic_radicals_dataset is None or strokes_dataset is None:
        print("Basic radical dataset or stroke dataset should not be None!")
        return
    if char_info_list is None or len(char_info_list) == 0:
        print("Char info list should not be None!")
        return

    # iterative search char infor
    similar_chars = []
    for ch_id in range(len(char_info_list)):
        ch_obj = char_info_list[ch_id]

        similar_basic_radicals = {}
        similar_strokes = {}

        found_stroke_id = []    # record the found stroke id in basic radical search action.

        # search similar basic radicals.
        ch_radicals = ch_obj.basic_radicals

        if len(ch_radicals) > 0:
            # this char has basic radical
            for bs_id in range(len(ch_radicals)):
                bs_obj = ch_radicals[bs_id]
                bs_obj_post = bs_obj.position.replace("[", "").replace("]", "").replace(" ", "").split(",")
                bs_obj_post = [int(p) for p in bs_obj_post]
                bs_obj_tag = bs_obj.tag
                bs_obj_id = bs_obj.id

                similar_bss = []

                # find all library basic radical objects
                if not bs_obj_tag in basic_radicals_dataset:
                    print(bs_obj_tag, " not in 775 basic radicals")
                else:
                    basic_radicals_lib = basic_radicals_dataset[bs_obj_tag]
                    print("Basic radicals lib len: ", len(basic_radicals_lib))

                    for bsl in basic_radicals_lib:
                        x, y, w, h = getSingleMaxBoundingBoxOfImage(bsl.image_bytes)

                        sim_bs_dict = {}

                        # rule1
                        if abs(x - bs_obj_post[0]) <= 5 and abs(y - bs_obj_post[1]) <= 5 and abs(w - bs_obj_post[2]) <= 5 and abs(h - bs_obj_post[3]) <= 5:
                            sim_bs_dict["path"] = bsl.image_path
                            sim_bs_dict["strokes_id"] = bs_obj.strokes_id

                            similar_bss.append(sim_bs_dict)

                similar_basic_radicals[bs_obj_id] = similar_bss

        print(similar_basic_radicals)

        # identify the found strokes in found basic radical
        for bs_id in similar_basic_radicals.keys():
            if len(similar_basic_radicals[bs_id]) > 0:
                # this basic radical found similar basic radicals, add stroke ids of this bs to found strokes list

                for bs in ch_obj.basic_radicals:
                    if bs_id == bs.id:
                      found_stroke_id += bs.strokes_id
        found_stroke_id = [int(f) for f in found_stroke_id]
        print(found_stroke_id)

        # find similar strokes for those not found strokes
        for sk in ch_obj.strokes:
            if sk.id in found_stroke_id:
                continue
            # find similar stroke
            post_ = sk.position
            id_ = sk.id
            type_ = sk.tag

            sm_strokes = find_similar_strokes(type_, post_, strokes_dataset)

            similar_strokes[id_] = sm_strokes

        similar_chars.append((similar_basic_radicals, similar_strokes))

    return similar_chars


def recompose_chars(similar_chars):
    if len(similar_chars) == 0:
        print("Not found similar chars")
        return
    # recompose all chars with similar basic radicals and strokes
    for i in range(len(similar_chars)):
        bk = createBlankGrayscaleImageWithSize((256, 256))

        similar_basic_radicals, similar_strokes = similar_chars[i]




def find_similar_strokes(type, position, strokes_dataset):
    """
    Find similar strokes based on the type, position and strokes dataset.
    :param type:
    :param position:
    :param strokes_dataset:
    :return:
    """
    similar_strokes = []

    THRESHOLD_POSITION = 10
    THRESHOLD_SIZE = 15
    THRESHOLD_CONDITION = 1.88

    x = position[0]
    y = position[1]
    w = position[2]
    h = position[3]

    center_x = int(x + w / 2)
    center_y = int(y + h / 2)

    strokes_same_post_and_size = []
    strokes_same_size = []

    sorted_condition = {}
    for i in range(len(strokes_dataset[type])):
        stroke_obj = strokes_dataset[type][i]
        img_ = stroke_obj.image_bytes
        x0, y0, w0, h0 = getSingleMaxBoundingBoxOfImage(img_)

        center_x0 = int(x0 + w0 / 2)
        center_y0 = int(y0 + h0 / 2)

        # calcuate the sorted condition
        val = abs((w - w0) / w0 * 1.) + abs((h - h0) / h0 * 1.) + abs((w * h - w0 * h0) / (w0 * h0) * 1.)
        sorted_condition[i] = val

        # Rule 1: almost same the postion and size
        if abs(center_x - center_x0) <= THRESHOLD_POSITION and abs(center_y - center_y0) <= THRESHOLD_POSITION and \
            abs(w - w0) <= THRESHOLD_SIZE and abs(h - h0) <= THRESHOLD_SIZE:
            strokes_same_post_and_size.append(stroke_obj.image_path)

    if len(strokes_same_post_and_size) > 0:
        # find the strokes with same position and size
        similar_strokes += strokes_same_post_and_size
        return similar_strokes
    else:
        print("Not find strokes with same position and size!")

    # Rule 2: Find strokes with same size
    if len(sorted_condition) == 0:
        print("Sorted condition is null!")

    sorted_condition_sorted = sorted(sorted_condition.items(), key=lambda x: x[1])
    print(sorted_condition_sorted)
    for s in sorted_condition_sorted:
        if s[1] > THRESHOLD_CONDITION:
            break
        strokes_same_size.append(strokes_dataset[type][s[0]].image_path)

    if len(strokes_same_size) > 0:
        similar_strokes += strokes_same_size
    else:
        print("Not find same size strokes")

    return similar_strokes


def query_char_info_from_chars_list(chars, xml_path):
    """
    Query the char info list.
    :param chars:
    :param xml_path:
    :return:
    """
    if chars is None or len(chars) == 0:
        return []

    # load radical data
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return

    root = tree.getroot()
    print("root len:", len(root))

    char_info_list = []

    for ch in chars:
        ch_obj = query_char_info_from_char(ch, root)
        char_info_list.append(ch_obj)

    return char_info_list


def query_char_info_from_char(char, root):
    if char == '':
        return []
    if root is None or len(root) <= 0:
        print('Root is None!')
        return []

    char_info_obj = None

    tag = ""
    u_code = ""
    stroke_orders = []
    stroke_position = []
    basic_radicals = []
    strokes = []

    for child in root:

        ch = child.attrib["TAG"].strip()
        if len(ch) > 1 or ch != char:
            continue

        # tag
        tag = ch

        # unicode
        u_code = child.attrib["ID"]

        # stroke order
        stroke_order_elems = child.findall('STROKE_ORDER')
        if stroke_order_elems:
            s_order = stroke_order_elems[0].text
            stroke_orders = s_order.split("|")
        else:
            print("not find stroke order of ", tag)

        # stroke position
        s_post_elems = child.findall('STROKES_POSITION')
        if s_post_elems:
            ss_post_elems = s_post_elems[0].findall('STROKE_POSITION')
            if ss_post_elems:
                for elem in ss_post_elems:
                    stroke_position.append(ast.literal_eval(elem.text))
        else:
            print("Not find storke position of ", tag)

        if len(stroke_orders) != len(stroke_position):
            print(tag, " storke order and stroke position not same length!")
        else:
            for id_ in range(len(stroke_orders)):
                stk_tag = stroke_orders[id_]
                stk_post = stroke_position[id_]
                stk_id = id_

                stk_obj = Stroke(id=stk_id, tag=stk_tag, path="", position=stk_post)
                strokes.append(stk_obj)

        # basic radicals
        basic_radicals_elems = child.findall("BASIC_RADICALS")
        if basic_radicals_elems:
            bs_elems = basic_radicals_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs in bs_elems:
                    bs_id = bs.attrib["ID"]
                    bs_tag = bs.attrib["TAG"]
                    bs_post = bs.attrib["POSITION"]

                    # basic radical object list
                    bs_strokes = []

                    bs_strokes_id = []

                    bs_strokes_elems = bs.findall("STROKES")
                    if bs_strokes_elems:
                        bs_stk_elems = bs_strokes_elems[0].findall("STROKE")
                        if bs_stk_elems:
                            for bs_stk in bs_stk_elems:
                                bs_stroke_id = bs_stk.attrib["ID"]
                                bs_strokes_id.append(bs_stroke_id)

                    bs_obj = BasicRadcial(id=bs_id, tag=bs_tag, path="", position=bs_post, strokes_id=bs_strokes_id)

                    basic_radicals.append(bs_obj)

        # strokes
        break

    char_info_obj = ChineseCharacter(id=u_code, tag=tag, basic_radicals=basic_radicals, strokes=strokes)
    return char_info_obj


class ChineseCharacter(object):
    id = ""
    tag = ""
    basic_radicals = []
    strokes = []

    def __init__(self, id, tag, basic_radicals, strokes):
        self.id = id
        self.tag = tag
        self.basic_radicals = basic_radicals
        self.strokes = strokes


class BasicRadcial(object):
    id = ""
    tag = ""
    path = ""
    position = []
    strokes_id = []

    def __init__(self, id, tag, path, position, strokes_id):
        self.id = id
        self.tag = tag
        self.path = path
        self.position = position
        self.strokes_id = strokes_id


class Stroke(object):
    id = ""
    tag = ""
    path = ""
    position = []

    def __init__(self, id, tag, path, position):
        self.id = id
        self.tag = tag
        self.path = path
        self.position = position
