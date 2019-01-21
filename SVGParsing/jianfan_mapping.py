# coding: utf-8
import os
import json


def jianfan_mapping():
    json_path = "../../Data/Characters/JanFan_mapping_dict.json"

    with open(json_path, 'r') as f:
        data = json.load(f)

    if data is None:
        print("json data not found!")
        return

    print("data len:", len(data))
    mapping_data = []
    for i in range(len(data)):
        d = list(data[i].items())
        if d[0][0] != d[0][1]:
            mapping_data.append([d[0][0], d[0][1]])

    print(mapping_data)

    # remove repeat mapping pair
    reaped_id = []
    for i in range(len(mapping_data)):
        is_repeat = False
        pair = mapping_data[i]

        if i in reaped_id:
            continue

        for j in range(len(mapping_data)):
            if i == j:
                continue
            pair_2 = mapping_data[j]

            if j in reaped_id:
                continue

            if pair[0] == pair_2[1] and pair[1] == pair_2[0]:
                reaped_id.append(j)
    print(reaped_id)






if __name__ == '__main__':
    jianfan_mapping()