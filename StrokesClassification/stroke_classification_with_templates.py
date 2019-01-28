# coding: utf-8
import cv2
import os
import time
import shutil

from utils.Functions import calculateSSIM, calculateCoverageRate


def main():
    images_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images'
    template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/classification/hengzheshu2.png'

    temp_saved_path = template_path.replace('.png', '')
    if not os.path.exists(temp_saved_path):
        print("not exist")
        os.mkdir(temp_saved_path)

    image_names = [f for f in os.listdir(images_path) if '.png' in f]
    print('images num: ', len(image_names))

    # template image
    temp_img = cv2.imread(template_path, 0)

    start = time.time()

    for i in range(len(image_names)):
        print('process: ', i, '-', image_names[i])
        img_path = os.path.join(images_path, image_names[i])
        img_ = cv2.imread(img_path, 0)

        if img_ is None:
            continue

        cr = calculateCoverageRate(temp_img, img_)
        ssim = calculateSSIM(temp_img, img_)

        # wangou2
        if ssim > 97 and cr > 48.5:
            shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzheshu4
        # if ssim > 90.5 and cr > 40.2:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie9
        # if ssim > 95.4 and cr > 50.6:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzhe
        # if ssim > 95 and cr > 71.4:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # zhongheng
        # if ssim > 94.8 and cr > 61.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie8
        # if ssim > 97 and cr > 86:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # henzheshu8
        # if ssim > 97 and cr > 83:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # wangou
        # if ssim > 90 and cr > 31:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzheshu6
        # if ssim > 94 and cr > 27.8:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shu heng
        # if ssim > 82.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzhehengzhepie
        # if ssim > 94.3 and cr > 80:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))


        # heng5
        # if ssim > 98 and cr > 87:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzheshu2
        # if ssim > 96 and cr > 63.2:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shu 2
        # if ssim > 98.4 and cr > 65.7:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # yan
        # if ssim > 92 and cr > 67.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # # ti2
        # if ssim > 97 and cr > 83.7:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shuwan
        # if ssim > 96 and cr > 70:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie5
        # if ssim >= 98 and cr > 78:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # yan
        # if ssim > 95 and cr > 85:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengpie1
        # if ssim > 96.4 and cr > 89.1:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie4
        # if ssim > 97.4 and cr > 61.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzheshu3
        # if ssim > 96.4 and cr > 83:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # na 5
        # if ssim > 92.4 and cr > 16.9:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shuti2
        # if ssim > 95 and cr > 64:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # heng 4
        # if ssim > 98.4 and cr > 89.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # yan
        # if ssim > 95 and cr > 85:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # er2
        # if ssim > 93 and cr > 73.8:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # er
        # if ssim > 96.8 and cr > 83.7:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzheshu2

        # if ssim > 97.6 and cr > 89:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # duanshu3
        # if ssim > 98.7 and cr > 80.9:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # duanheng2
        # if ssim > 98.6 and cr > 85.9:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # duanshu2
        # if ssim > 97.9 and cr > 65.6:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzhe
        # if ssim > 97 and cr > 88:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # na4
        # if ssim > 94.8 and cr > 77:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shuti
        # if ssim > 95.1 and cr > 74.1:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # ti
        # if ssim > 99 and cr > 98.7:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # piena
        # if ssim > 94.6 and cr > 83.8:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengzhegou3
        # if ssim > 92.6 and cr > 78.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # duanshu
        # if ssim > 99 and cr > 94.4:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # yi1
        # if ssim > 84.6 and cr > 39.1:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # henshugou2
        # if ssim > 89.3 and cr > 44:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie3
        # if ssim > 97 and cr > 85:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # heng zhe shu
        # if ssim > 95.8 and cr > 84.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # di san dian
        # if ssim > 97.4 and cr > 77.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # hengshu gou
        # if ssim > 89 and cr > 45:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # na2
        # if ssim > 94.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))


        # shu wan gou 戈
        # if ssim > 87 and cr > 46:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shu gou 2
        # if ssim > 96 and cr > 94:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # da shu wan gou
        # if ssim > 87 and cr > 48.6:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # xiao pie ti
        # if ssim > 95.5 and cr > 67.7:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie shang
        # if ssim > 96.2:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # na
        # if ssim > 92.8 and cr > 58.4:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie 2
        # if ssim > 93.8 and cr > 26.9:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # # pie
        # if ssim > 92.5 and cr > 32:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))


        # chang heng
        # if ssim > 97.2:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # # pie dian
        # if ssim > 97.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # zhong heng
        # if ssim > 96.5 and cr > 74.3:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # duan heng
        # if ssim > 97.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))


        # chang dian
        # if ssim > 96 and cr > 58:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shugou
        # if ssim > 93 and cr > 90:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shuhengzhegou
        # if ssim > 89.5:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # heng
        # if ssim > 93.4:
        #     # shutil.copy2(img_path, os.path.join(temp_saved_path, image_names[i]))
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # shu
        # if ssim > 94.5:
        #     # shutil.copy2(img_path, os.path.join(temp_saved_path, image_names[i]))
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pie
        # if ssim > 94:
        #     # shutil.copy2(img_path, os.path.join(temp_saved_path, image_names[i]))
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # na
        # if ssim > 94:
        #     shutil.copy2(img_path, os.path.join(temp_saved_path, image_names[i]))

        # dian
        # if ssim > 98.5:
        #     # shutil.copy2(img_path, os.path.join(temp_saved_path, image_names[i]))
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # chagn pie
        # if ssim > 92 and cr > 52:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        # pieti
        # if ssim > 90 and cr > 30:
        #     shutil.move(img_path, os.path.join(temp_saved_path, image_names[i]))

        if i % 1000 == 0:
            print("cr: %0.3f , ssim: %0.3f" % (cr, ssim))

        # if i == 10000:
        #     break

    end = time.time()
    print('Process time: ', (end - start))





if __name__ == '__main__':
    main()