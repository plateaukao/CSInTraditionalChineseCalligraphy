# coding: utf-8
import os
import shutil
import random

source_path = "../../../Data/SVGs_中文"
save_path = "../../../Data/Stroke_recomposed_tool/200svg chars dataset"

# remove existed 200 svg files
if os.path.exists(save_path):
    os.remove(save_path)

os.mkdir(save_path)

filenames = [f for f in os.listdir(source_path) if '.svg' in f]
print(filenames)

# shuffle array to random select 200 files

for i in range(10):
    random.shuffle(filenames)

for i in range(200):
    shutil.copy2(os.path.join(source_path, filenames[i]), os.path.join(save_path, filenames[i]))