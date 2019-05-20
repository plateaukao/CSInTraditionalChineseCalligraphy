# coding: utf-8
import os
import xml.etree.ElementTree as ET
from utils.Functions import prettyXml

xml_path = "../../../Data/Characters/jian_fan_merge_basic_radical_stroke_complement.xml"

save_path = "../../../Data/Characters/not_process_600_chars.xml"

def extract_not_process():
    new_tree = ET.parse(save_path)
    new_root = new_tree.getroot()


    tree = ET.parse(xml_path)
    root = tree.getroot()

    for i in range(len(root)):
        elem = root[i]

        bs_root_elems = elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            continue
        else:
            tag = elem.attrib["TAG"].strip()
            id = elem.attrib["ID"].strip()

            type_str = ""
            type_elems = elem.findall("TYPE")
            if type_elems:
                type_str = type_elems[0].text

            struct_str = ""
            struct_elems = elem.findall("STRUCTURE")
            if struct_elems:
                struct_str = struct_elems[0].text

            key_str = ""
            key_elems = elem.findall("KEY_RADICAL")
            if key_elems:
                key_str = key_elems[0].text

            sk_count_str = ""
            sk_count_elems = elem.findall("STROKE_COUNT")
            if sk_count_elems:
                sk_count_str = sk_count_elems[0].text

            new_radical_elem = ET.SubElement(new_root, "RADICAL")
            new_radical_elem.set("ID", id)
            new_radical_elem.set("TAG", tag)

            new_type_elem = ET.SubElement(new_radical_elem, "TYPE")
            new_type_elem.text = type_str

            new_struct_elem = ET.SubElement(new_radical_elem, "STRUCTURE")
            new_struct_elem.text = struct_str

            new_key_elem = ET.SubElement(new_radical_elem, "KEY_RADICAL")
            new_key_elem.text = key_str

            new_sk_count_elem = ET.SubElement(new_radical_elem, "STROKE_COUNT")
            new_sk_count_elem.text = sk_count_str

    prettyXml(new_root, '\t', '\n')
    new_tree.write(save_path, encoding='utf-8')


if __name__ == '__main__':
    extract_not_process()