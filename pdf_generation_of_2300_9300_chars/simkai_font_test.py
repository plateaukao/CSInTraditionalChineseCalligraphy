# coding: utf-8
import os
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font_path = "../data/simkai.ttf"
char_size = 230

save_path = "../../../Data/generated_results/2300fonts/"

path_2300 = "2300chars.txt"

def simkai_font_test():

    ch = "爨"

    image_mode = "L"
    font = ImageFont.truetype(font_path, size=char_size)

    image = Image.new(image_mode, (char_size, char_size), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ch, 0, font=font)

    image.save(ch+".png")


def generate_char_font_image(ch, font):
    image_mode = "L"
    image = Image.new(image_mode, (char_size, char_size), 255)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), ch, 0, font=font)

    return image


def chars_simkai_font_test():
    chars = []
    with open(path_2300, "r") as f:
        chars = f.readline()

    font = ImageFont.truetype(font_path, size=char_size)

    for ch in chars:
        img = generate_char_font_image(ch, font)
        img.save(os.path.join(save_path, "{}.png".format(ch)))




if __name__ == '__main__':
    # simkai_font_test()
    chars_simkai_font_test()