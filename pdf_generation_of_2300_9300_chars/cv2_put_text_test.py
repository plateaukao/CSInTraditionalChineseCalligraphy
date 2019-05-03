# coding: utf-8
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

font_path = "../data/simkai.ttf"
char_size = 20




font = ImageFont.truetype(font_path, size=char_size)

label_img = Image.new("L", (250, 20), 255)
label_draw = ImageDraw.Draw(label_img)
label_draw.text((0, 0), "测试" + "8DB5\N", 0, font=font)





img = np.ones((20, 250), np.uint8) * 255

img[:20, : 250] = label_img
#
# font                   = cv2.FONT_HERSHEY_SIMPLEX
# bottomLeftCornerOfText = (10,230)
# fontScale              = 0.5
# fontColor              = 0
# lineType               = 2
#
# cv2.putText(img,'Hello World!',
#     bottomLeftCornerOfText,
#     font,
#     fontScale,
#     fontColor,
#     lineType)
#
#


cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()