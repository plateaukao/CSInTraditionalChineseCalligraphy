# coding: utf-8
import os
import xml.etree.ElementTree as ET

jianti_xml_path = "../../../Data/Characters/jian_fan_merge_basic_radical_stroke_complement.xml"

chars_2300_path = "../pdf_generation_of_2300_9300_chars/2300chars.txt"
chars_9300_path = "../pdf_generation_of_2300_9300_chars/9300chars.txt"


def bs_265_statistics_in_2300_and_9300():
    bs_set_str = "右侯，里唐，右摇，隹十，右滕，乛点，几币，熏上，釁上，两点，𠃊，帶上，犀上，鹿灬，彐，比左，撇口，豕少横，左叚，酉寸，黎上，㐅，漢右，人彡，三横撇，⺊，右派，覺上，左竹，右谶，左朝，旅右，繫上，關内，右隰，舞上，夕捺，左段，丷一，學上，典上，贵上，十冖，免两点，興上，巤下，右经，左彀，右非，录上，里展，横竖提，左北，臼工，竊下，奏上，羲下，良下，坚上，刍攵，祭上，荛下，舆上，墼上，井横八，匕禾，倉下，夕加点，两夫，珤，右竹，罒，與上，左卯，撇四，左辟，寡中，幺大，庚下，是下，薦下，亠丷冖，⺶捺，横寸，龶，右醯，鬯上，鑿上，升下，横折钩，尸丨，薛下，既左，兜上，右犯，横生，啬上，右汤，日横寸，右隱，撇虫，兰撇捺，小冂，十从冖，鳥少点，横竖，横小，亠凶，勿少撇，右鐵，右练，凿下，竖提横，右姊，里延，里扁，监上，乛耳，丷提，切左，火火冖，粲上，荛中，竖提点，却右，囊上，孔右，右报，蓑下，昔上，⺈田，逐右，龹，段左，定下，横自，折左，录下，百冖，告上，右流，懺右，横肀，鼠下，小点，疆右，坙，右鞴，青上，衣下，壑上，亂左，雐，横丰，丿丨乚，爨上，𡿨，鸟少横，点撇，壞右，左拜，鬱左下，獸左，敖左，撇冂，印左，難左，刃止，右侃，戈少点，辰內，右拜，台上，壺下，龸，兼下，游右，左卬，右叚，互下，鰥右，羊下，左制，嬛右，两竖，華下，金下，曷下，⺮，左那，土丷，歰，岡里，其上，寝下，左卵，曹上，侌，左敝，余下，益上，帀，右婕，曾中，撇竖，鼎下，左非，右德，妻上，繭下，孔左，外臧，第下，具上，彭左，右殇，尞上，叢下，左對，豐上，衡中，郎左，主加横，右临，左殷，𠂤，艷左上，畏下，寒中，者上，竖点夕，十下，黑上，官下，左朗，襄下，小加点，系下，乛捺，骨上，左卸，聚下，右滿，倏右，善上，左艱，右姬，一厶，惠上，⺻，凵丿，走下，裁外，⺍，左即，覀，留上，寇下，盥上，譖右上，共横，歲下，焉下，丅，𠂉"

    bs_set = set()

    for bs in bs_set_str.split("，"):
        bs_set.add(bs.strip())
    print(bs_set)
    print(len(bs_set))

    chars_2300 = []
    with open(chars_2300_path, "r") as f:
        for ch in f.readline():
            chars_2300.append(ch.strip())
    print(chars_2300)

    chars_9300 = []
    with open(chars_9300_path, "r") as f:
        for ch in f.readline():
            chars_9300.append(ch.strip())
    print(chars_9300)

    ch_bs_dict = {}

    tree = ET.parse(jianti_xml_path)
    root = tree.getroot()

    for i in range(len(root)):
        radical_elem = root[i]

        tag = radical_elem.attrib["TAG"].strip()
        bs_list = []

        bs_root_elems = radical_elem.findall("BASIC_RADICALS")
        if bs_root_elems:
            bs_elems = bs_root_elems[0].findall("BASIC_RADICAL")
            if bs_elems:
                for bs_item in bs_elems:
                    bs_list.append(bs_item.attrib["TAG"].strip())

        ch_bs_dict[tag] = bs_list

    print(ch_bs_dict)

    bs_char_dict = {}

    for bs in bs_set:
        ch_list = []
        for ch in ch_bs_dict.keys():
            bs_list = ch_bs_dict[ch]

            if bs in bs_list:
                ch_list.append(ch)

        bs_char_dict[bs] = ch_list

    print(bs_char_dict)
    print('+++++++')

    print(len(bs_char_dict))

    # chars in 2300
    bs_in_2300 = []
    bs_in_2300_chars_dict = {}
    for bs in bs_char_dict.keys():
        ch_list = bs_char_dict[bs]

        ch_in_2300_list = []
        for ch in ch_list:
            if ch in chars_2300:
                ch_in_2300_list.append(ch)

        if len(ch_in_2300_list) > 0:
            bs_in_2300_chars_dict[bs] = ch_in_2300_list
            bs_in_2300.append(bs)
    print(bs_in_2300_chars_dict)
    print(len(bs_in_2300_chars_dict))

    # chars in 9300
    bs_in_9300 = []
    bs_in_9300_chars_dict = {}
    for bs in bs_char_dict.keys():

        if bs in bs_in_2300_chars_dict:
            continue
        ch_list = bs_char_dict[bs]

        ch_in_9300_list = []
        for ch in ch_list:
            if ch not in chars_2300 and ch in chars_9300:
                ch_in_9300_list.append(ch)

        if len(ch_in_9300_list) > 0:
            bs_in_9300_chars_dict[bs] = ch_in_9300_list
            if bs not in bs_in_2300:
                bs_in_9300.append(bs)

    print(bs_in_9300_chars_dict)
    print(len(bs_in_9300_chars_dict))

    print("----")
    print(bs_in_2300)
    print(bs_in_9300)

    bs_2300_set = set()
    for k in bs_in_2300_chars_dict.keys():
        bs_2300_set.add(k)

    bs_9300_set = set()
    for k in bs_in_9300_chars_dict.keys():
        bs_9300_set.add(k)

    print(bs_set - bs_2300_set - bs_9300_set)


if __name__ == '__main__':
    bs_265_statistics_in_2300_and_9300()