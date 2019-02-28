# coding: utf-8
import os
import shutil
import random

source_path = "../../../Data/SVGs_中文"
save_path = "../../../Data/Stroke_recomposed_tool/chars dataset"

characters_path = "775characters.txt"

characters = ""
with open(characters_path, 'r') as f:
    characters = f.readlines()[0]
    print(characters)

print(len(characters))

if not os.path.exists(save_path):
    os.mkdir(save_path)
    
filenames = [f for f in os.listdir(source_path) if '.svg' in f]

count = 0
for ch in characters:
    for fn in filenames:
        if ch in fn:
            shutil.copy2(os.path.join(source_path, fn), os.path.join(save_path, fn))
            count += 1
print('count: ', count)

# remove existed  svg files
# if os.path.exists(save_path):
#     os.remove(save_path)
#
# os.mkdir(save_path)
#
# filenames = [f for f in os.listdir(source_path) if '.svg' in f]
# print(filenames)
#
# # shuffle array to random select 200 files
#
# for i in range(10):
#     random.shuffle(filenames)
#
# for i in range(200):
#     shutil.copy2(os.path.join(source_path, filenames[i]), os.path.join(save_path, filenames[i]))