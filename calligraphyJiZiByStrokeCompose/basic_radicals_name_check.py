# coding:utf-8
import os

char_775_path = '../../../Data/Calligraphy_database/Chars_775'
char_1000_path = '../../../Data/Calligraphy_database/Chars_1000'


def radical_name_check(path):
    if path == '':
        return
    # list all folders
    filenames = [f for f in os.listdir(path) if '.' not in f]
    print('file names len: ', len(filenames))

    for fn in filenames:
        radical_img_names = [f for f in os.listdir(os.path.join(path, fn, 'basic radicals')) if '.png' in f]
        radical_fold_names = [f for f in os.listdir(os.path.join(path, fn, 'basic radicals')) if not '.png' in f]

        error_label = False

        for rin in radical_img_names:
            r_ = rin.replace('.png', '')
            if r_ not in radical_fold_names:
                error_label = True


        if error_label:
            print(fn, ' has error!')
            continue




if __name__ == '__main__':
    radical_name_check(char_775_path)
    radical_name_check(char_1000_path)