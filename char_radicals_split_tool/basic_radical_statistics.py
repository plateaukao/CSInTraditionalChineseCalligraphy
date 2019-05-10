# coding: utf-8
import os


def basic_radical_statistics():
    path = "../../../Data/Calligraphy_database/not_process_data_split/lp_processed"
    bushou_txt_path = "../../../Data/Characters/基本偏旁部首和部件.txt"

    save_path = "../../../Data/Characters/部件统计.txt"

    chars = [f for f in os.listdir(path) if "." not in f]
    print("chars num: ", len(chars))

    bs_names = set()
    for char_id in range(len(chars)):
        ch = chars[char_id]

        bs_path = os.path.join(path, ch, "basic radicals")

        bs_folders = [f for f in os.listdir(bs_path) if "." not in f]

        for bf in bs_folders:
            bs_names.add(bf.split("_")[-1])

    print("bs name num: ", len(bs_names))
    print(bs_names)

    bushou_set = set()
    with open(bushou_txt_path, "r") as f:
        for r in f.readlines():
            bushou_set.add(r.strip())

    print("bushou num: ", len(bushou_set))
    print(bushou_set)

    pianpang_set = bs_names - bushou_set
    print("pianpang num: ", len(pianpang_set))
    print(pianpang_set)

    with open(save_path, "w") as f:
        for ps in pianpang_set:
            if ps == "":
                continue
            f.write(ps + "\n")


def split_pianpang_bushou():
    bushou_txt_path = "../../../Data/Characters/基本偏旁部首和部件.txt"

    bushou_set = set()
    with open(bushou_txt_path, "r") as f:
        for r in f.readlines():
            bushou_set.add(f)


if __name__ == '__main__':
    basic_radical_statistics()