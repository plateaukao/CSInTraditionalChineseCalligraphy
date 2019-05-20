# coding:utf-8
class ChineseCharacter(object):
    ucode = ""
    tag = ""
    type = ""
    struct = ""
    key_radical = ""
    stroke_count = ""
    stroke_order = ""

    basic_radicals = []


class BasicRadical(object):
    id = ""
    tag = ""
    strokes = []
    similar_tags = []