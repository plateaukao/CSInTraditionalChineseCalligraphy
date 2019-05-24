class ChineseCharacter(object):
    ucode = ""
    tag = ""
    basic_radicals = []
    strokes = []


class BasicRadical(object):
    id = ""
    tag = ""
    position = []
    stroke_ids = []

class Stroke(object):
    id = ""
    tag = ""
    position = []


class CharMatchResult(object):
    tag = ""
    similar_basic_radicals = {}
    similar_strokes = {}