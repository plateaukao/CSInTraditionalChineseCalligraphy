# coding: utf-8
import os
import cv2
from utils.Functions import createBlankGrayscaleImageWithSize
from calligraphyJiZiByStrokeCompose.util import create_grid_image_rgb

# path= "./temp"
#
# stroke_imgs = [f for f in os.listdir(path) if "stroke" in f and ".png" in f]
#
# bk_ = createBlankGrayscaleImageWithSize((400, 400))
#
# for fn in stroke_imgs:
#     img_ = cv2.imread(os.path.join(path, fn), 0)
#     for y in range(img_.shape[0]):
#         for x in range(img_.shape[1]):
#             if img_[y][x] == 0:
#                 bk_[y][x] = 0

bk_ = create_grid_image_rgb("田字格", (400, 400))

cv2.imshow("img", bk_)
cv2.waitKey(0)
cv2.destroyAllWindows()



