# coding: utf-8
import os
import cv2
import shutil


def copy_strokes_to_basic_radicals(root_path):

    # clean extra image in basic radicals
    chars = [f for f in os.listdir(root_path) if "." not in f]
    print("chars num: ", len(chars))

    for char in chars:
        print(char)
        stroke_path = os.path.join(root_path, char, "strokes")
        radical_path = os.path.join(root_path, char, "basic radicals")

        radical_img_names = [f for f in os.listdir(radical_path) if ".png" in f]
        radical_names = []
        for rin in radical_img_names:
            if len(rin.split("_")) == 3:
                # remove this image
                if os.path.exists(os.path.join(radical_path, rin)):
                    os.remove(os.path.join(radical_path, rin))

            if len(rin.split("_")) == 4:
                radical_names.append(rin)

        # copy stroke images to basic radicals

        stroke_names = [f for f in os.listdir(stroke_path) if ".png" in f]

        used_id = []
        for rn in radical_names:
            bs_img_path = os.path.join(radical_path, rn)
            bs_path = os.path.join(radical_path, rn.replace(".png", ""))
            bs_img = cv2.imread(bs_img_path, 0)

            for i in range(len(stroke_names)):
                if i in used_id:
                    continue
                sk_img_path = os.path.join(stroke_path, stroke_names[i])

                sk_img = cv2.imread(sk_img_path, 0)

                ssim = calculate_ssim(bs_img, sk_img)

                if ssim > 0.94:
                    shutil.copy2(os.path.join(stroke_path, stroke_names[i]), os.path.join(bs_path, stroke_names[i]))
                    used_id.append(i)


def calculate_ssim(bs_img, stroke_img):
    if bs_img is None or stroke_img is None:
        return 0.

    total_count = ssim_count = 0
    for y in range(stroke_img.shape[0]):
        for x in range(stroke_img.shape[1]):
            if stroke_img[y][x] == 0:
                total_count += 1

            if stroke_img[y][x] == 0 and bs_img[y][x] == 0:
                ssim_count += 1

    return ssim_count / total_count * 1.





if __name__ == '__main__':
    # root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp"
    # copy_strokes_to_basic_radicals(root_path)

    # root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_left_right"
    # copy_strokes_to_basic_radicals(root_path)

    root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_processed"
    copy_strokes_to_basic_radicals(root_path)

    # root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_single_char"
    # copy_strokes_to_basic_radicals(root_path)
    #
    # root_path = "../../../Data/Calligraphy_database/not_process_data_split/lp_up_down"
    # copy_strokes_to_basic_radicals(root_path)