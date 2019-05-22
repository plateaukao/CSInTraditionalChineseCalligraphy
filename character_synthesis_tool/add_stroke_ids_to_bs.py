# coding: utf-8
import os
import xml.etree.ElementTree as ET
from utils.Functions import prettyXml


xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_no_position.xml"
save_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_position.xml"

def add_stroke_ids_to_bs():
    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return

    root = tree.getroot()

    for i in range(len(root)):
        radical_elem = root[i]
        tag = radical_elem.attrib["TAG"].strip()

        bs_sk_count_dict = {}   # [3,4,5]  3 + 4 +5 == sk_count

        sk_count = 0
        sk_count_elems = radical_elem.findall("STROKE_COUNT")
        if sk_count_elems and sk_count_elems[0].text is not None:
            sk_count = int(sk_count_elems[0].text)
        else:
            print("{} has no stroke count!".format(tag))
            continue

        if sk_count == 0:
            continue

        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_tag = bs_item.attrib["TAG"].strip()
                    bs_id = bs_item.attrib["ID"].strip()
                    if bs_tag == "":
                        continue
                    bs_sk_count = get_stroke_count(root, bs_tag)
                    bs_sk_count_dict[bs_id] = bs_sk_count

        # check bs sk count == sk_count

        bs_sk_count_total = 0
        for key in bs_sk_count_dict.keys():
            bs_sk_count_total += bs_sk_count_dict[key]

        if bs_sk_count_total == sk_count:
            pass
        else:
            if bs_sk_count_total < sk_count:
                d_value = sk_count - bs_sk_count_total
                for key in bs_sk_count_dict.keys():
                    if bs_sk_count_dict[key] == 0:
                        bs_sk_count_dict[key] = d_value

        # add sk ids to basic radicals
        used_ids = 0
        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_id = bs_item.attrib["ID"].strip()

                    if bs_id not in bs_sk_count_dict:
                        continue

                    bs_sk_count = bs_sk_count_dict[bs_id]

                    bs_sk_root_elem = ET.SubElement(bs_item, "STROKES")

                    for bs_sk_id in range(bs_sk_count):
                        sk_id_ = used_ids + bs_sk_id
                        bs_sk_elem = ET.SubElement(bs_sk_root_elem, "STROKE")
                        bs_sk_elem.set("ID", str(sk_id_))

                    used_ids += bs_sk_count

    # pretty xml
    prettyXml(root, '\t', '\n')
    tree.write(save_path, encoding='utf-8')








def get_stroke_count(root, ch):
    if root is None or ch == "":
        print("root or ch is none!")
        return 0

    sk_count = 0
    for i in range(len(root)):
        elem = root[i]

        tag = elem.attrib["TAG"].strip()

        if ch == tag:
            sk_count_elems = elem.findall("STROKE_COUNT")
            if sk_count_elems and sk_count_elems[0].text is not None:
                sk_count = int(sk_count_elems[0].text)
                break

    return sk_count


if __name__ == '__main__':
    add_stroke_ids_to_bs()


    # test get stroke count

    # tree = ET.parse(xml_path)
    # root = tree.getroot()
    #
    # ch = "斤"
    # sk_count = get_stroke_count(root, ch)