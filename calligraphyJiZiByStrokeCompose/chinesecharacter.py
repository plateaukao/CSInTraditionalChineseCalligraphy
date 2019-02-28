# coding: utf-8


class ChineseCharacter(object):

    tag = ""
    u_code = ""
    stroke_orders = []
    stroke_position = []
    stroke_orders_to_string = ""

    def __init__(self, tag, u_code, stroke_orders, stroke_position):
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