# coding: utf-8
import os
import shutil

stroke_path = "../../../Data/Calligraphy_database/Stroke_pngs"
type_path = "../../../Data/Calligraphy_database/Stroke_types"
save_path = "../../../Data/Calligraphy_database/Stroke_type_checks"

def stroke_type_check():
    stroke_png_names = [f for f in os.listdir(stroke_path) if ".png" in f]

    stroke_type_names = []
    type_names = [f for f in os.listdir(type_path) if "." not in f]
    for type in type_names:
        type_stroke_names = [f for f in os.listdir(os.path.join(type_path, type)) if ".png" in f]
        stroke_type_names += type_stroke_names

    for spn in stroke_png_names:
        if spn not in stroke_type_names:
            shutil.copy2(os.path.join(stroke_path, spn), os.path.join(save_path, spn))


if __name__ == '__main__':
    stroke_type_check()