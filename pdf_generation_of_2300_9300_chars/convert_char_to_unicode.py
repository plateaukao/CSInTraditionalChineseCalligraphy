# coding: utf-8
import os


def char_to_unicode_str(ch):
    if ch == "":
        return ""

    return ch.encode("unicode_escape").decode("utf-8").replace("\\u", "").upper().replace("\\", "").replace("N", "")


def chars_to_unicode_list(chars):
    if chars is None or len(chars) == 0:
        return []

    codes = []
    for ch in chars:
        code = char_to_unicode_str(ch)
        print(code)
        codes.append(code)
    return codes


def convert_char_to_unicode():
    path_2300_chars = "2300chars.txt"
    path_9300_chars = "9300chars.txt"

    with open(path_2300_chars, "r") as f:
        contents = f.readline()
        print(contents)

        codes = chars_to_unicode_list(contents)
        print(codes)

    with open(path_9300_chars, "r") as f:
        contents = f.readline()
        print(contents)
        codes = chars_to_unicode_list(contents)
        print(codes)


if __name__ == '__main__':
    convert_char_to_unicode()

    # char = "嬡"
    # code = char_to_unicode_str(char)
    #
    # print(code)
