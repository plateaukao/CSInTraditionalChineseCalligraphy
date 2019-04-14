# coding: utf-8


class StrokeImage(object):
    image_path = ""
    image_bytes = None

    def __init__(self, path, image_bytes):
        self.image_path = path
        self.image_bytes = image_bytes


class BasicRadicalImage(object):
    image_path = ""
    image_bytes = None

    def __init__(self, image_path, image_bytes):
        self.image_path = image_path
        self.image_bytes = image_bytes