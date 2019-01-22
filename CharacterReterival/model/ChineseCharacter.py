# coding: utf-8


class ChineseCharacter:

    id = ''
    tag = ''
    type = ''
    structure = ''
    keyRadical = ''
    strokeCount = ''
    pinyins = None
    subRadicals = None

    def __init__(self, id, tag, type, structure, keyRadical, strokeCount, pinyins, subRadicals):
        self.id = id
        self.tag = tag
        self.type = type
        self.structure = structure
        self.keyRadical = keyRadical
        self.strokeCount = strokeCount
        self.pinyins = pinyins
        self.subRadicals = subRadicals
    