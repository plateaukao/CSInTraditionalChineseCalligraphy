# coding: utf-8


class ChineseCharacter(object):

    tag = ""
    u_code = ""
    stroke_orders = []
    stroke_position = []

    def __init__(self, tag, u_code, stroke_orders, stroke_position):
        self.tag = tag
        self.u_code = u_code
        self.stroke_orders = stroke_orders
        self.stroke_position = stroke_position