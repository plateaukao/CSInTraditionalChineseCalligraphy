# coding: utf-8
import os
import cv2


def char_select():
    chars_775_path = "775basic_characters.txt"
    chars_all_path = "chinese_characters.txt"

    chars_775 = []
    chars_all = []

    chars_3000_commons = []
    chars_other_1000 = []

    with open(chars_all_path, 'r') as f:
        for s in f.readlines():
            chars_all.append(s.strip())
    print(chars_all[-1])

    with open(chars_775_path, 'r') as f:
        for s in f.readlines():
            chars_775.append(s.strip())
    print(chars_775[-1])

    # select 3000 common chars
    chars_3000_commons = chars_all[: 3000]

    chars_3000_commons = sorted(chars_3000_commons)
    chars_3000_commons = sorted(chars_3000_commons)

    # select 1000 chars from common chars
    count = 0
    for s in chars_3000_commons:
        if s not in chars_775:
            chars_other_1000.append(s)
            count += 1
        if count >= 1000:
            break

    print(len(chars_other_1000))

    with open("1000_characters.txt", 'w') as f:
        for s in chars_other_1000:
            if chars_other_1000.index(s) == len(chars_other_1000) -1:
                f.write(s)
            else:
                f.write(s + "\n")








if __name__ == '__main__':
    char_select()