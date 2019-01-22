# coding: utf-8
import os
import xml.etree.ElementTree as ET
from time import time

from CharacterReterival.model import ChineseCharacter


def queryChineseCharacter(condition):
    """
    Query the chinese character with input search condition from the xml datafile.
    :param condition:
    :return:
    """
    if condition is None or condition == '':
        return None

    radical_path = "../../../Data/Characters/radical_add_stroke_position.xml"

    # load radical data
    tree = ET.parse(radical_path)
    if tree is None:
        print("tree is none!")
        return
    root = tree.getroot()
    print("root len:", len(root))

    char_obj = None
    for i in range(len(root)):
        radical = root[i]

        ch = radical.attrib['TAG']

        if ch == condition:
            # parse the target radical
            id = radical.attrib['ID']


            break


    return char_obj


if __name__ == '__main__':
    char_obj = queryChineseCharacter("我")

