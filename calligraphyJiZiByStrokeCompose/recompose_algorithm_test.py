# coding: utf-8
import os
import cv2
import time

from calligraphyJiZiByStrokeCompose.util import query_char_info, query_char_target_strokes, stroke_recompose, \
                    load_stroke_library_dataset, query_char_info_from_chars_list, query_char_target_stroke_by_dataset


def recompose():
    start_time = time.time()
    stroke_lib_path = "../../../Data/Stroke_recomposed_tool/strokes dataset"

    save_path = "../../../Data/1000 generated results"
    dataset = load_stroke_library_dataset(stroke_lib_path)
    print("Load dataset time: ", time.time() - start_time)

    heng_zhe = dataset['横折横折']
    print(len(heng_zhe))

    chars = ['犍']

    char_info_list = query_char_info_from_chars_list(chars)

    char_target_strokes_list = query_char_target_stroke_by_dataset(dataset, char_info_list)

    generated_imgs, _ = stroke_recompose(char_info_list, char_target_strokes_list)

    for i in range(len(generated_imgs)):
        cv2.imshow('img_%d' % i, generated_imgs[i])
        cv2.imwrite(os.path.join(save_path, "%s_%04d.png" % (chars[0], 0)), generated_imgs[i])


    cv2.waitKey(0)
    cv2.destroyAllWindows()






if __name__ == '__main__':
    recompose()