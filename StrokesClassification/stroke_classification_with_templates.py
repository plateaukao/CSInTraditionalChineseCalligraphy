# coding: utf-8
import cv2
import os

from utils.Functions import calculateSSIM, calculateCoverageRate


def main():
    images_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/images'
    template_path = '/Users/liupeng/Documents/Data/stroke_classification_dataset/classification/long_heng.png'

    temp_saved_path = template_path.replace('.png', '')
    if not os.path.exists(temp_saved_path):
        os.mkdir(temp_saved_path)

    image_names = [f for f in os.listdir(images_path) if '.png' in f]
    print('images num: ', len(image_names))

    # template image
    temp_img = cv2.imread(template_path, 0)

    for i in range(len(image_names)):
        img_path = os.path.join(images_path, image_names[i])
        img_ = cv2.imread(img_path, 0)

        cr = calculateCoverageRate(temp_img, img_)
        ssim = calculateSSIM(temp_img, img_)

        print("cr: %0.3f , ssim: %0.3f" % (cr, ssim))





if __name__ == '__main__':
    main()