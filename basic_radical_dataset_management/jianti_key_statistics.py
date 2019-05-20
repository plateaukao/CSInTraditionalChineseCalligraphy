# coding: utf-8
import os
import cv2
import xml.etree.ElementTree as ET

jianti_xml_path = "../../../Data/Characters/radical_add_stroke_position_similar_structure_add_stroke_order_add_basic_radicals_add_lp_processed_simpler_jianti.xml"
fanti_xml_path = "../../../Data/Characters/fanti_2.xml"


def jianti_key():
    tree = ET.parse(jianti_xml_path)
    root = tree.getroot()

    key_set = set()
    for i in range(len(root)):
        radical_elem = root[i]

        key_str = ""
        key_elems = radical_elem.findall("KEY_RADICAL")
        if key_elems:
            key_str = key_elems[0].text

        if key_str != "":
            key_set.add(key_str)

    print(key_set)



if __name__ == '__main__':
    # jianti_key()

    xml_data = "页赤身寸耒音黄礻疋疒瓦咅黑卩足冖衤氏矢玄糸甘田门辶艹面香西女月厂示钅廴灬辰齐又至斗四匕石鸟屮乙夕马刂禾丨車皿玉缶色风穴巛文矛艮肉里鬲丷 豆厄忄匚广廾耳弋鬼鼠入小豕山氵大干彡川支宀乛夂高冂辛叉一日骨臣凵飞人户巾长工斤尹言酉比气二手毋殳贝阝瓜韦髟黍牛曰卑子攵彐金尢见爪鬯黽聿毛阜士片弓邑火水纟饣刀冫鼻龙扌走行爿十力止耂心角厶车非亅幺豸谷儿攴羽丶血舟犬韭鼎彑白巳肀讠爫犭王虍食八隹爻旡衣土己父雨立歹皮舌黹采齿而首丿几卝鹿臼彳卜青隶麻兀龠囗鱼乚羊勹欠亻自虫亠生麦母卤麥鼓癶米用革尸竹戈牙目方木口"
    word_data = "丨丿乛一乙乚丶八勹匕冫卜厂刀刂儿二匚阝丷几卩冂力冖凵人亻入十厶亠匸讠廴又艹彳巛川辶寸大飞干工弓廾广己彐巾口马门宀女犭山彡尸饣士扌氵纟巳土囗兀夕夊小忄幺弋尢夂子贝比灬长车歹斗厄方风禸父戈卝户火无旡见斤耂毛木肀牛牜爿片攴攵气欠犬日氏礻手殳水瓦尣王韦文毋心牙爻曰月爫支止爪白癶歺甘瓜禾钅立龙矛皿母目疒鸟皮生石矢示罒田玄穴疋业衤用玉耒艸臣虫而襾臼老虍艮缶耳米齐肉色舌覀羊血行先页网聿至舟衣自竹糹糸舛羽貝采镸車辰赤角見谷豆釆辵克里卤麦身豕走豸酉邑言辛足𧾷青雨齿非靣隶金阜飠鱼隹革骨鬼韭面飛音香韋首食髟高鬲黄鹿麻黑黍黃鼓鼠鼻龠"

    for x in xml_data:
        if x not in word_data:
            print(x)

    print("=======")

    for w in word_data:
        if w not in xml_data:
            print(w)
