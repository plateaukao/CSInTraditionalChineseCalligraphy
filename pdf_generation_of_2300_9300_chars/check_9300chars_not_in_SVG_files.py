# coding: utf-8
import os
from pdf_generation_of_2300_9300_chars.convert_char_to_unicode import chars_to_unicode_list

def check_9300chars_not_in_svg_files():
    path_9300_chars = "9300chars.txt"

    path_svgs = "../../../Data/SVGs_中文"

    svg_names = [f for f in os.listdir(path_svgs) if ".svg" in f]
    print("svgs num: ", len(svg_names))

    chars = ""
    with open(path_9300_chars, "r") as f:
        chars = f.readline()

    codes = chars_to_unicode_list(chars)
    print("chars len: ", len(chars), " codes num: ", len(codes))

    unfound_chars = []

    for i in range(len(codes)):
        ch = chars[i]
        code = codes[i]

        if not ch + "_" +code + ".svg" in svg_names:
            unfound_chars.append(ch)
            print("Not found: ", ch)
    print(unfound_chars)
    print("Not found chars num: ", len(unfound_chars))


    with open("9300chars_cleaned.txt", "w") as f:
        for i in range(len(chars)):
            if chars[i] not in unfound_chars:
                if i == len(chars) - 1:
                    f.write(chars[i])
                else:
                    f.write(chars[i] + "\n")


if __name__ == '__main__':
    check_9300chars_not_in_svg_files()
