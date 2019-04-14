# coding: utf-8


class ChineseCharacter(object):

    tag = ""
    u_code = ""
    stroke_orders = []
    stroke_position = []
    stroke_orders_to_string = ""
    strokes = []
    basic_radicals = []

    def __init__(self, tag, u_code, stroke_orders, stroke_position, basic_radicals=[], strokes=[]):
        self.tag = tag
        self.u_code = u_code
        self.stroke_orders = stroke_orders
        self.stroke_position = stroke_position

        if len(stroke_orders) > 0:
            for i in range(len(stroke_orders)):
                if i == len(stroke_orders) - 1:
                    self.stroke_orders_to_string += stroke_orders[i]
                else:
                    self.stroke_orders_to_string += stroke_orders[i] + ", "
        else:
            self.stroke_orders_to_string = ""

        self.strokes = strokes
        self.basic_radicals = basic_radicals


class SimilarChineseCharacter(object):

    # {bs_id:  [radical list]}
    similar_basic_radicals = None

    # {stroke_id: [stroke list]}
    similar_strokes = None

    def __init__(self, similar_basic_radicals, similar_strokes):
        self.similar_basic_radicals = similar_basic_radicals
        self.similar_strokes = similar_strokes