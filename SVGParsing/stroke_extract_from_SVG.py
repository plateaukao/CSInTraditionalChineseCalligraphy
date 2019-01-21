import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom


def extract_stroke_path_from_svg(svg_name, svg_path, stroke_path):

    # 1. load svg file
    doc = minidom.parse(svg_path)

    # 2. get path
    path_elems = [p for p in doc.getElementsByTagName("path")]
    num_paths = int(len(path_elems) / 3)

    path_objs = []
    for i in range(num_paths):
        path_objs.append(path_elems[i])
    print("path len: ", len(path_objs))

    # 3. save path to svg file
    for i in range(len(path_objs)):
        p_obj = path_objs[i]
        d = p_obj.getAttribute('d')
        content = '<svg version="1.1" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n <g transform="scale(1, -1) translate(0, -900)"><path d="' + d + \
            '" fill="black"></path></g></svg>'
        with open(os.path.join(stroke_path, (svg_name + "_" + str(i) + ".svg")), 'w') as f:
            f.write(content)

        drawing = svg2rlg(os.path.join(stroke_path, (svg_name + "_" + str(i) + ".svg")))
        renderPM.drawToFile(drawing, os.path.join(stroke_path, (svg_name + "_" + str(i) + ".png")), "png")

def stroke_extract_from_SVG():
    base_path = "../../Data/svgs"
    stroke_path = "../../Data/svgs_stroke"
    if not os.path.exists(stroke_path):
        os.mkdir(stroke_path)

    file_list = os.listdir(base_path)

    svg_file_names = []
    for fl in file_list:
        if ".svg" in fl:
            svg_file_names.append(fl)
    print(svg_file_names)

    for i in range(len(svg_file_names)):
        print("process: ", i)
        svg_file = svg_file_names[i]
        svg_path = os.path.join(base_path, svg_file)
        svg_name = svg_file.replace(".svg", "")
        extract_stroke_path_from_svg(svg_name, svg_path, stroke_path)

        # if i == 3:
        #     break






if __name__ == '__main__':
    stroke_extract_from_SVG()