# coding: utf-8
import os
import xml.etree.ElementTree as ET
from time import time


def prettyXml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作


def add_structure_similar_tags():
    radical_path = "../../Data/Characters/radical_add_stroke_position.xml"
    save_path = "../../Data/Characters/radical_add_stroke_position_similar_structure.xml"

    # load radical data
    tree = ET.parse(radical_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    struct_dict = {}

    for i in range(len(root)):
        radical = root[i]
        # if no sub_radicals, no processing
        if radical.find('SUB_RADICALS') is None:
            print(radical.attrib['TAG'])
            continue

        ch = radical.attrib['TAG']
        if len(ch) > 1:
            continue
        sub_radicals = []
        sub_radicals_elem = radical.find('SUB_RADICALS')
        sub_radical_elems = sub_radicals_elem.findall('SUB_RADICAL')
        print('sub radical len: ', len(sub_radical_elems))
        for sub in sub_radical_elems:
            sub_radicals.append(sub.attrib['ID'])
        print(sub_radicals)

        struct_dict[ch] = sub_radicals

    print(struct_dict)

    print('begin to process relation:')
    begin_time = time()
    struct_sub_dict = {}
    for key1 in struct_dict.keys():

        if len(key1) > 1:
            continue

        sub_rds1 = struct_dict[key1]

        sub_dicts = []
        for sub_ in sub_rds1:
            s_dict_ = {}
            s_list_ = []

            for key2 in struct_dict.keys():
                if key1 == key2 or len(key2) > 1:
                    continue

                sub_rds2 = struct_dict[key2]
                if sub_ in sub_rds2:
                    s_list_.append(key2)
            if len(s_list_) > 0:
                s_dict_[sub_] = s_list_
                sub_dicts.append(s_dict_)
        struct_sub_dict[key1] = sub_dicts
    print(struct_sub_dict)

    end_time = time()

    print('spend time: ', (end_time - begin_time))


    # add SIMILAR_TAGS in SUB_RADICAL element
    for k in struct_sub_dict.keys():
        sub_relation_list = struct_sub_dict[k]
        if struct_sub_dict is None or len(sub_relation_list) < 1:
            continue

        for i in range(len(root)):
            radical = root[i]

            if k != radical.attrib['TAG']:
                continue

            sub_radicals_elem = radical.find('SUB_RADICALS')
            sub_radical_elems = sub_radicals_elem.findall('SUB_RADICAL')
            print((len(sub_radical_elems)))

            for j in range(len(sub_radical_elems)):
                for sub_rel_ in sub_relation_list:
                    if sub_radical_elems[j].find('SIMILAR_TAG') is not None:
                        print("find similar tag")
                        break
                    sub_key = list(sub_rel_.keys())[0]
                    if sub_radical_elems[j].attrib['ID'] == sub_key:

                        sub_rel_elem = ET.Element("SIMILAR_TAG")
                        sub_rel_elem.text = str(sub_rel_[sub_key])

                        sub_radical_elems[j].append(sub_rel_elem)

    prettyXml(root, '\t', '\n')
    tree.write(save_path, encoding='utf-8')











if __name__ == '__main__':
    add_structure_similar_tags()