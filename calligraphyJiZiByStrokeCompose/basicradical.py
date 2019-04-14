# coding: utf-8


class BasicRadical(object):
    id = ''
    tag = ''
    position = None
    strokes = []

    def __init__(self, id, tag, position, strokes):
        self.id = id
        self.tag = tag
        self.position = position
        self.strokes = strokes


class Stroke(object):
    id = ''
    tag = ''
    position = None

    def __init__(self, id, tag, position):
        self.id = id
        self.tag = tag
        self.position = position
