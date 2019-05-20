# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET


from utils.Functions import getSingleMaxBoundingBoxOfImage, prettyXml

xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals_add_lp_processed.xml"
xml_template_path = "../../../Data/Characters/xml_template.xml"
save_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals_add_lp_processed_simpler_jianti.xml"


def simpler_jianti_xml():
    tree = ET.parse(xml_path)
    if tree is None:
        print("Tree is none")
        return
    root = tree.getroot()
    # print(len(root))
    # return

    # write to new xml
    new_tree = ET.parse(xml_template_path)
    if new_tree is None:
        print("template xml tree is none!")
        return
    new_root = new_tree.getroot()

    for i in range(len(root)):
        print("Process: ", i)
        radical_elem = root[i]

        tag = radical_elem.attrib["TAG"].strip()
        ucode = radical_elem.attrib["ID"].strip()

        type_str = ""

        type_elems = radical_elem.findall("TYPE")
        if type_elems:
            type_str = type_elems[0].text

        key_str = ""
        key_elems = radical_elem.findall("KEY_RADICAL")
        if key_elems:
            key_str = key_elems[0].text

        struct_str = ""
        struct_elems = radical_elem.findall("STRUCTURE")
        if struct_elems:
            struct_str = struct_elems[0].text

        sk_count_str = ""
        sk_count_elems = radical_elem.findall("STROKE_COUNT")
        if sk_count_elems:
            sk_count_str = sk_count_elems[0].text

        bs_stroke_dict = {}
        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_id = bs_item.attrib["ID"].strip()
                    bs_tag = bs_item.attrib["TAG"].strip()

                    bs_sk_key = "{}_{}".format(bs_id, bs_tag)   # id_tag
                    bs_sk_ids = []   # stroke id of this bs item
                    # find all strokes in this bs elem
                    bs_sk_root_elems = bs_item.findall("STROKES")
                    if bs_sk_root_elems:
                        bs_sk_elems = bs_sk_root_elems[0].findall("STROKE")
                        if bs_sk_elems:
                            for bs_sk_item in bs_sk_elems:
                                bs_sk_ids.append(bs_sk_item.attrib["TAG"].strip())

                    if len(bs_sk_ids) > 0:
                        bs_stroke_dict[bs_sk_key] = bs_sk_ids


        # new radical element
        new_radical_elem = ET.Element("RADICAL")
        new_radical_elem.set("ID", ucode)
        new_radical_elem.set("TAG", tag)

        new_type_elem = ET.SubElement(new_radical_elem, "TYPE")
        new_type_elem.text = type_str

        new_struct_elem = ET.SubElement(new_radical_elem, "STRUCTURE")
        new_struct_elem.text = struct_str

        new_key_elem = ET.SubElement(new_radical_elem, "KEY_RADICAL")
        new_key_elem.text = key_str

        new_sk_count_elem = ET.SubElement(new_radical_elem, "STROKE_COUNT")
        new_sk_count_elem.text = sk_count_str

        if len(bs_stroke_dict) > 0:
            new_bs_root_elem = ET.SubElement(new_radical_elem, "BASIC_RADICALS")
            for key in bs_stroke_dict.keys():
                new_bs_id = key.split("_")[0]
                new_bs_tag = key.split("_")[-1]

                new_bs_elem = ET.SubElement(new_bs_root_elem, "BASIC_RADICAL")
                new_bs_elem.set("ID", new_bs_id)
                new_bs_elem.set("TAG", new_bs_tag)

                # new_bs_sk_ids = bs_stroke_dict[key]
                # if len(new_bs_sk_ids) > 0:
                #     for id in new_bs_sk_ids:
                #         new_bs_sk_elem = ET.SubElement(new_bs_elem, "STROKE")
                #         new_bs_sk_elem.set("ID", id)

        new_root.append(new_radical_elem)

    # write to new xml file
    prettyXml(new_root, '\t', '\n')
    new_tree.write(save_path, encoding='utf-8')







if __name__ == '__main__':
    simpler_jianti_xml()