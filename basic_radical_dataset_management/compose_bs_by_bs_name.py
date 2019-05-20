# coding: utf-8
import os
import copy
import cv2
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom

svg_imgs_path = "../../../Data/Calligraphy_database/SVGs_中文"

jianti_str = "追右:追:0 1 2 3 4 5|豐上:豐:0 1 2 3 4 5 6 7 8 9 10|尸丨:声:3 4 5 6|左非:非:0 1 2 3|寒中:寒:3 4 5 6 7 8 9|氺:氺:0 1 2 3 4|龹:龹:0 1 2 3 4 5|一朩:余:2 3 4 5 6|切左:切:0 1|庚下:庚:3 4 5 6 7|龸:党:0 1 2 3 4|中一:贵:0 1 2 3 4|右拜:拜:4 5 6 7 8|夕捺:夜:4 5 6 7|右非:非:4 5 6 7|奏上:奏:0 1 2 3 4|郎左:郎:0 1 2 3 4 5|蓖中:蓖:3 4 5 6 7 8|龶:龶:0 1 2 3|具上:具:0 1 2 3 4 5|勺外:勺:0 1|北左:北:0 1 2|告上:告:0 1 2 3|乂:乂:0 1|寇下:寇:3 4 5 6 7 8 9 10|印左:印:0 1 2|䒑:䒑:0 1 2|敖左:敖:0 1 2 3 4 5|录上:录:0 1 2|卂:卂:0 1 2|龷:昔:0 1 2 3|汤右:汤:3 4 5|啬上:啬:0 1 2 3 4|报右:报:3 4 5 6|左拜:拜:0 1 2 3|彭左:彭:0 1 2 3 4 5 6 7 8|裁外:裁:0 1 2 9 10 11|点撇:辨:7 8|㔾:㔾:0 1|卯左:卯:0 1 2|⺍:⺍:0 1 2|春上:春:0 1 2 3 4|龴:通:0 1|竖点夕:餐:0 1 2 3 4|比左:比:0 1|撇横捺:监:2 3 4|曾中:曾:2 3 4 5 6 7|段左:段:0 1 2 3 4|横寸:得:7 8 9 10|小点:隳:13 14 15 16|凵丿:屰:3 4 5|衡中:衡:3 4 5 6 7 8 9 10 11 12|戊点:蔑:8 9 10 11 12 13|旁上:旁:0 1 2 3 4 5|荛中:荛:3 4 5"
fanti_str = "罒:罒:0 1 2 3 4|右滿:滿:3 4 5 6 7 8 9 10 11 12 13|嬛右:嬛:3 4 5 6 7 8 9 10 11 12 13 14 15|羊八:業:5 6 7 8 9 10 11 12|百冖:憂:0 1 2 3 4 5 6 7|壺下:壺:3 4 5 6 7 8 9 10 11|歲下:歲:4 5 6 7 8 9 10 11 12|叢下:叢:5 6 7 8 9 10 11 12 13 14 15 16 17|繭下:繭:4 5 6 7 8 9 10 11 12 13 14 15 16 17 18|鳥少点:裊:0 1 2 3 4 5 6|彭左:彭:0 1 2 3 4 5 6 7 8|右鐵:鐵:8 9 10 11 12 13 14 15 16 17 18 19 20|倉下:倉:2 3 4 5 6 7 8 9|譖右上:譖:7 8 9 10 11 12 13 14|壞右:壞:3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18|左艱:艱:0 1 2 3 4 5 6 7 8 9 10|雝:癰:5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22|臤:腎:0 1 2 3 4 5 6 7|疆右:疆:6 7 8 9 10 11 12 13 14 15 16 17 18|鬱左下:鬱:14 15 16 17 18 19 20 21 22 23 24 25|帶上:帶:0 1 2 3 4 5|匚夾:愜:3 4 5 6 7 8 9 10 11|亂左:亂:0 1 2 3 4 5 6 7 8 9 10 11|繫上:繫:0 1 2 3 4 5 6 7 8 9 10 11 12|岡里:岡:2 3 4 5 6 7|薦下:薦:4 5 6 7 8 9 10 11 12 13 14 15 16|釁上:釁:0 1 2 3 4 5 6 7 8 9 10 11 12 13|坙:徑:3 4 5 6 7 8 9|竊下:竊:5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21|⺻:盡:0 1 2 3 4|走下:從:7 8 9 10|寉:確:5 6 7 8 9 10 11 12 13 14|昜:傷:4 5 6 7 8 9 10 11 12|睪:澤:3 4 5 6 7 8 9 10 11 12 13 14 15|雔:雙:0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15|犀上:犀:0 1 2 3 4 5 6 7|雐:雐:0 1 2 3 4 5 6 7 8 9 10 11 12 13|帀:帀:0 1 2 3|學上:學:0 1 2 3 4 5 6 7 8 9 10 11 12|火火冖:縈:0 1 2 3 4 5 6 7 8 9|獵右:獵:3 4 5 6 7 8 9 10 11 12 13 14 15 16 17|覺上:覺:0 1 2 3 4 5 6 7 8 9 10 11 12|鑿上:鑿:0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19|歰:歰:0 1 2 3 4 5 6 7 8 9 10 11 12 13|懺右:懺:3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19|乑:乑:0 1 2 3 4 5|關内:關:8 9 10 11 12 13 14 15 16 17 18|丱:丱:0 1 2 3 4|左對:對:0 1 2 3 4 5 6 7 8 9 10|右隱:隱:2 3 4 5 6 7 8 9 10 11 12 13 14 15"

def create_blank_svg(dom):
    # create blank svg file by removing path element
    root = dom.documentElement

    path_elems = root.getElementsByTagName("path")
    if path_elems is None:
        print("not find path elements")
        return
    print("path elements len: ", len(path_elems))

    # path parent element
    path_parent_elem = None

    for e in path_elems:
        # find path parent element
        path_parent_elem = e.parentNode
        break

    for e in path_elems:
        path_parent_elem.removeChild(e)

    return dom, path_parent_elem


def compose_bs_by_bs_name(bs_dict_str, type="jianti"):

    svg_names = [f for f in os.listdir(svg_imgs_path) if ".svg" in f]

    jianti_list = bs_dict_str.split("|")
    print(len(jianti_list))


    for jt_item in jianti_list:

        bs_name = jt_item.split(":")[0]
        svg_char = jt_item.split(":")[1]
        sk_orders = jt_item.split(":")[-1].split(" ")
        sk_orders = [int(s) for s in sk_orders]

        print(bs_name)

        svg_file = ""
        for sn in svg_names:
            if svg_char in sn:
                svg_file = sn
                break
        if svg_file == "":
            continue

        svg_path = os.path.join(svg_imgs_path, svg_file)

        # open svg file
        dom = minidom.parse(svg_path)

        # find path element in original svg file
        root = dom.documentElement
        path_elems = root.getElementsByTagName("path")
        if path_elems is None:
            print("not find path elements")
            return
        print("path elements len: ", len(path_elems))

        dom_, path_parent_elem = create_blank_svg(copy.deepcopy(dom))

        for id in sk_orders:
            path_parent_elem.appendChild(path_elems[id])

        data_xml = dom_.toxml()

        with open("./{}_temp/{}.svg".format(type, bs_name), 'w') as f:
            f.write(data_xml)

        drawing = svg2rlg("./{}_temp/{}.svg".format(type, bs_name))
        if drawing is None:
            print("drawing is None!")
        renderPM.drawToFile(drawing, "./{}_temp/{}.png".format(type, bs_name), "png")

        os.system("rm {}".format("./{}_temp/{}.svg".format(type, bs_name)))


if __name__ == '__main__':
    compose_bs_by_bs_name(jianti_str)
    compose_bs_by_bs_name(fanti_str, type="fanti")