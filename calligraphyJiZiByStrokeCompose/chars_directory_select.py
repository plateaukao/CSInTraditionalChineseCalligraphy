# coding: utf-8
import os
import shutil

char_775_path = "../../../Data/Calligraphy_database/Chars_775"
char_1000_path = "../../../Data/Calligraphy_database/Chars_1000"
char_path = "../../../Data/Calligraphy_database/Chars"

def chars_select():
    char_775_path = "../../../Data/Calligraphy_database/Chars_775"
    char_1000_path = "../../../Data/Calligraphy_database/Chars_1000"
    char_path = "../../../Data/Calligraphy_database/Chars"

    file_names = [f for f in os.listdir(char_path) if '.' not in f]
    print(file_names)

    chars_775 = []
    with open("775basic_characters.txt", 'r') as f:
        for s in f.readlines():
            chars_775.append(s.strip())

    chars_1000 = []
    with open("1000_characters.txt", 'r') as f:
        for s in f.readlines():
            chars_1000.append(s.strip())

    # move 775 chars
    for s in chars_775:
        if not os.path.exists(os.path.join(char_path, s)):
            print("{} not found".format(s))
            continue
        else:
            if not os.path.exists(os.path.join(char_775_path, s)):
                shutil.copytree(os.path.join(char_path, s), os.path.join(char_775_path, s))

    print("==========")
    # move 1000 chars
    for s in chars_1000:
        if not os.path.exists(os.path.join(char_path, s)):
            print("{} not found".format(s))
            continue
        else:
            if not os.path.exists(os.path.join(char_1000_path, s)):
                shutil.copytree(os.path.join(char_path, s), os.path.join(char_1000_path, s))


def clean_data():

    filenames = [f for f in os.listdir(char_775_path) if '.' not in f]

    for fn in filenames:
        radical_path = os.path.join(char_775_path, fn, "basic radicals")
        stroke_path = os.path.join(char_775_path, fn, "strokes")

        # radical path remove png file
        png_names = [f for f in os.listdir(radical_path) if ".png" in f]
        for pn in png_names:
            os.remove(os.path.join(radical_path, pn))

        # stroke path rename png file
        png_names = [f for f in os.listdir(stroke_path) if ".png" in f]
        for pn in png_names:
            pns = pn.split('_')
            new_pn = pns[0] + '_' + pns[1] + '_' + 'stroke' + '_' + pns[2]

            shutil.move(os.path.join(stroke_path, pn), os.path.join(stroke_path, new_pn))

    filenames = [f for f in os.listdir(char_1000_path) if '.' not in f]

    for fn in filenames:
        radical_path = os.path.join(char_1000_path, fn, "basic radicals")
        stroke_path = os.path.join(char_1000_path, fn, "strokes")

        # radical path remove png file
        png_names = [f for f in os.listdir(radical_path) if ".png" in f]
        for pn in png_names:
            os.remove(os.path.join(radical_path, pn))

        # stroke path rename png file
        png_names = [f for f in os.listdir(stroke_path) if ".png" in f]
        for pn in png_names:
            pns = pn.split('_')
            new_pn = pns[0] + '_' + pns[1] + '_' + 'stroke' + '_' + pns[2]

            shutil.move(os.path.join(stroke_path, pn), os.path.join(stroke_path, new_pn))




if __name__ == '__main__':
    # chars_select()
    clean_data()
