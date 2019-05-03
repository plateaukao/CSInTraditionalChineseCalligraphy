# coding: utf-8
import os
import cv2
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np


from utils.Functions import createBlankGrayscaleImageWithSize, creatBlankRGBImageWithSize
from pdf_generation_of_2300_9300_chars.convert_char_to_unicode_test import chars_to_unicode_list


# chars_path = "9300chars_cleaned.txt"
chars_path = "2300chars.txt"
font_path = "../data/simkai.ttf"
char_size = 500
# save_path = "../../../Data/generated_results/9300 pdf files"
save_path = "../../../Data/generated_results/2300 pdf files"

pdf_file_name = "2300chars.pdf"



def drawline(img,pt1,pt2,color,thickness=1,style='dotted',gap=5):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in  np.arange(0,dist,gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)

    if style=='dotted':
        for p in pts:
            cv2.circle(img,p,thickness,color,-1)
    else:
        s=pts[0]
        e=pts[0]
        i=0
        for p in pts:
            s=e
            e=p
            if i%2==1:
                cv2.line(img,s,e,color,thickness)
            i+=1


def create_pdf_files():
    chars = []
    with open(chars_path, "r") as f:
        chars = f.readline()
    print("chars num: ", len(chars))

    codes = chars_to_unicode_list(chars)

    font = ImageFont.truetype(font_path, size=char_size)
    label_font = ImageFont.truetype(font_path, size=100)

    bk = creatBlankRGBImageWithSize((4200, 3000))
    for char_id in range(len(chars)):

        if char_id == len(chars) - 1:
            cv2.imwrite(os.path.join(save_path, "page_%d.png" % (math.floor(char_id / 35) - 1)), bk)

        if char_id % 35 == 0 and char_id != 0:
            cv2.imwrite(os.path.join(save_path, "page_%d.png" % (math.floor(char_id / 35)-1)), bk)
            # create new page of PDF
            bk = creatBlankRGBImageWithSize((4200, 3000))

        page_id = math.floor((char_id / 35))
        print("page id: ", page_id)

        # # merge 35 chars to one page.
        col_id = math.floor((char_id - page_id * 35) / 5)
        row_id = (char_id - page_id * 35) % 5

        # create char image
        image = Image.new("L", (char_size, char_size), 255)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), chars[char_id], 0, font=font)

        # draw label
        label_img = Image.new("L", (500, 100), 255)
        label_draw = ImageDraw.Draw(label_img)
        label_draw.text((0, 0), (chars[char_id].replace("\n", "") + " " + str(codes[char_id])), 0, font=label_font)

        # print(codes[char_id], type(codes[char_id]), chars[char_id].replace("\n", "") + str(codes[char_id]))

        ch_bk = createBlankGrayscaleImageWithSize((600, 600))
        ch_bk[:char_size, :char_size] = image
        ch_bk[char_size: 600, : char_size] = label_img

        ch_bk_3 = cv2.cvtColor(ch_bk, cv2.COLOR_GRAY2RGB)

        # write char and unicode to image
        # cv2.putText(ch_bk, chars[char_id] + " " + codes[char_id], (10,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0, 2)

        ch_bk_rgb = creatBlankRGBImageWithSize(ch_bk.shape)

        # add boundary
        cv2.line(ch_bk_rgb, (1, 1), (1, char_size-1), (0, 0, 255), 4)
        cv2.line(ch_bk_rgb, (1, 1), (char_size - 1, 1), (0, 0, 255), 4)
        cv2.line(ch_bk_rgb, (char_size-1, 1), (char_size-1, char_size - 1), (0, 0, 255), 4)
        cv2.line(ch_bk_rgb, (1, char_size-1), (char_size-1, char_size - 1), (0, 0, 255), 4)

        # dash line
        drawline(ch_bk_rgb, (int(char_size/2), 1), (int(char_size/2), char_size-1), (0, 0, 255), 2)
        drawline(ch_bk_rgb, (1, int(char_size / 2)), (char_size - 1, int(char_size / 2)), (0,0,  255), 2)

        for y in range(ch_bk.shape[0]):
            for x in range(ch_bk.shape[1]):
                if ch_bk[y][x] != 255 :
                    ch_bk_rgb[y][x] = (0, 0, 0)



        print("col id: ", col_id, " row id:", row_id)
        print(bk[col_id*char_size: (col_id+1)*char_size, row_id*char_size: (row_id+1)*char_size].shape)
        bk[col_id*600: (col_id+1)*600, row_id*600: (row_id+1)*600] = ch_bk_rgb

        # if char_id == 36:
        #     break


def merge_pngs_to_pdf_file():

    file_names = [f for f in os.listdir(save_path) if ".png" in f]
    file_names = sorted(file_names)
    print(file_names)

    img_list = []
    img1 = Image.open(os.path.join(save_path, file_names[0]))
    for i in range(1, len(file_names)):
        img_ = Image.open(os.path.join(save_path, file_names[i]))
        img_list.append(img_)

    pdf_path = os.path.join(save_path, pdf_file_name)

    img1.save(pdf_path, "PDF", resolution=100., save_all=True, append_images=img_list)


def merge_pngs_to_pdf_file_by_range(page_num=20):
    file_names = [f for f in os.listdir(save_path) if ".png" in f]
    file_names = sorted(file_names)
    print(file_names)

    img_list = []
    img1 = Image.open(os.path.join(save_path, file_names[0]))

    for i in range(1, len(file_names)):
        if i % page_num == 0 or i == len(file_names) - 1:
            pdf_path = os.path.join(save_path, ("2300chars_{}.pdf".format(math.floor(i / page_num))))
            img1.save(pdf_path, "PDF", resolution=100., save_all=True, append_images=img_list)

            if i < len(file_names) - 1:
                img_list = []
                img1 = Image.open(os.path.join(save_path, file_names[i]))
            continue

        img_ = Image.open(os.path.join(save_path, file_names[i]))
        img_list.append(img_)





if __name__ == '__main__':
    # create_pdf_files()
    # merge_pngs_to_pdf_file()
    merge_pngs_to_pdf_file_by_range()