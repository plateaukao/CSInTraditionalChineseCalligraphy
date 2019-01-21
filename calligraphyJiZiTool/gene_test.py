# coding: utf-8
import cv2

from utils.Templates import create_doufang_template


images_path = ['/Users/liupeng/Documents/Data/Calligraphy_database_test/song/白_767D_白_1.png',
               '/Users/liupeng/Documents/Data/Calligraphy_database_test/song/日_65E5_日_1.png',
               '/Users/liupeng/Documents/Data/Calligraphy_database_test/kai/畩_7569_依_1.png',
               '/Users/liupeng/Documents/Data/Calligraphy_database_test/song/山_5C71_山_1.png',
               '/Users/liupeng/Documents/Data/Calligraphy_database_test/song/尽_5C3D_盡_1.png']

images = []

for path in images_path:
    img_ = cv2.imread(path, 0)
    images.append(img_)

bk = create_doufang_template(images, 20, 60, num_per_column=3)

print(bk.shape)

cv2.imshow("bk", bk)

cv2.waitKey(0)
cv2.destroyAllWindows()
