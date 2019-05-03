# coding: utf-8
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font_path = "../data/simkai.ttf"
char_size = 230

def simkai_font_test():

    ch = "爨"

    image_mode = "L"
    font = ImageFont.truetype(font_path, size=char_size)

    image = Image.new(image_mode, (char_size, char_size), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ch, 0, font=font)

    image.save(ch+".png")



if __name__ == '__main__':
    simkai_font_test()