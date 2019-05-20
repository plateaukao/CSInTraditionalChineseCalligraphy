#coding: utf-8
import os


chars_9300_path = "9300chars.txt"
chars_600_no_svg_path = "600chars_no_svg.txt"

svg_path = "../../../Data/Calligraphy_database/SVGs_中文"

def chars_600_no_svg():
    svg_imgs = [f.split("_")[0].strip() for f in os.listdir(svg_path) if ".svg" in f]
    print("svg imgs num: ", len(svg_imgs))

    # read 9000 chars
    chars_9000 = []
    with open(chars_9300_path, "r") as f:
        for ch in f.readline():
            chars_9000.append(ch.strip())
    print("chars 9000 num: ", len(chars_9000))

    with open(chars_600_no_svg_path, "w") as f:
        for ch in chars_9000:
            if ch not in svg_imgs:
                f.write(ch + "\n")


if __name__ == '__main__':
    chars_600_no_svg()