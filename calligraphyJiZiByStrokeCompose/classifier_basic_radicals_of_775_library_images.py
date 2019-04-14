# coding: utf-8
import os
import shutil


save_path = "../../../Data/Calligraphy_database/char_generate_lib/basic radicals dataset"
char_775_path = "../../../Data/Calligraphy_database/Chars_775"


def classifier_basic_radicals_of_775_library_images():
    chars = [f for f in os.listdir(char_775_path) if "." not in f]
    print("Chars len: ", len(chars))

    type_set = set()

    for ch in chars:
        radical_path = os.path.join(char_775_path, ch, "basic radicals")
        radical_names = [f for f in os.listdir(radical_path) if ".png" in f]
        for rn in radical_names:
            r_name = rn.replace(".png", "").split("_")[-1]
            type_set.add(r_name)
    print("Type num: ", len(type_set))

    # create type folder in save path
    for ts in type_set:
        if os.path.exists(os.path.join(save_path, ts)):
            continue

        os.mkdir(os.path.join(save_path, ts))

    # move basic radical images to type folder of basic radical
    for ch in chars:
        radical_path = os.path.join(char_775_path, ch, "basic radicals")
        radical_names = [f for f in os.listdir(radical_path) if ".png" in f]
        for rn in radical_names:
            r_name = rn.replace(".png", "").split("_")[-1]
            shutil.copy2(os.path.join(radical_path, rn), os.path.join(save_path, r_name))





if __name__ == '__main__':
    classifier_basic_radicals_of_775_library_images()