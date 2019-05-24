# coding: utf-8

import os
import shutil
import xml.etree.ElementTree as ET
from utils.Functions import prettyXml


def add_stroke_order_to_XML():
    type_path = '/Users/liupeng/Documents/Data/Calligraphy_database/Stroke_types'
    stroke_name = [f.replace('.png', '') for f in os.listdir(type_path) if '.png' in f]
    print(stroke_name)
    print("stroke num:", len(stroke_name))

    stroke_map = {}

    type_img_names = []

    for s in stroke_name:
        path = os.path.join(type_path, s)
        stroke_imgs = [f for f in os.listdir(path) if '.png' in f]
        for img in stroke_imgs:
            stroke_map[img] = s
            type_img_names.append(img)

    print(len(stroke_map))
    print(len(type_img_names))

    all_imgs_path = '/Users/liupeng/Documents/Data/Calligraphy_database/Stroke_pngs'
    all_names = [f for f in os.listdir(all_imgs_path) if '.png' in f]
    print(len(all_names))

    img_names_diff = []
    for s in all_names:
        if s not in type_img_names:
            print(s)
            img_names_diff.append(s)
    print(len(img_names_diff))

    img_diff_path = '/Users/liupeng/Documents/Data/Calligraphy_database/Stroke_type_img_diff'
    if not os.path.exists(img_diff_path):
        os.mkdir(img_diff_path)

    for s in img_names_diff:
        shutil.copy2(os.path.join(all_imgs_path, s), img_diff_path)

    xml_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position.xml"
    save_path = "../../../Data/Calligraphy_database/XML_dataset/dataset_add_ids_add_position_add_stroke_order.xml"

    tree = ET.parse(xml_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    for i in range(len(root)):
        print(i)
        radical = root[i]

        if len(radical.attrib['TAG']) <= 0 or len(radical.attrib['TAG']) > 1:
            continue
        tag = radical.attrib['TAG']
        # find all images
        imgs = []
        for s in type_img_names:
            if tag + '_' in s:
                imgs.append(s)
        # sort images
        max_num = 0
        for s in imgs:
            s = s.replace('.png', '')
            ss = s.split('_')
            if len(ss) == 3:
                num = int(ss[2].replace(' ', '').replace("\n", "").replace("stroke", ""))
            elif len(ss) == 4:
                num = int(ss[3].replace(' ', '').replace("\n", "").replace("stroke", ""))
            # if i > 7379:
            #     print(ss[2].replace(' ', ''))
            # num = int(ss[2].replace(' ', '').replace("\n", "").replace("stroke", ""))
            max_num = max(num, max_num)

        imgs_sorted = []
        for k in range(max_num+1):
            for s in imgs:
                if '_' + str(k) + '.png' in s:
                    imgs_sorted.append(s)
        stroke_order = []
        for s in imgs_sorted:
            stroke_order.append(stroke_map[s])
        stroke_order_str = ''
        for j in range(len(stroke_order)):
            if j == len(stroke_order) - 1:
                stroke_order_str += stroke_order[j]
            else:
                stroke_order_str += stroke_order[j] + '|'

        stroke_order_elem = ET.Element("STROKE_ORDER")
        stroke_order_elem.text = stroke_order_str

        root[i].append(stroke_order_elem)

    prettyXml(root, '\t', '\n')
    tree.write(save_path, encoding='utf-8')




if __name__ == '__main__':
    add_stroke_order_to_XML()