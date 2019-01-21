from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from xml.dom import minidom


# 1. load svg file


def extract_stroke_path_from_svg(path):

    # 1. load svg file
    doc = minidom.parse(path)

    # 2. get path
    path_elems = [p for p in doc.getElementsByTagName("path")]
    num_paths = int(len(path_elems) / 3)

    path_objs = []
    for i in range(num_paths):
        path_objs.append(path_elems[i])
    print("path len: ", len(path_objs))
    print("path: ", path_objs[0].getAttribute('d'))
    print("path: ", path_objs[1].getAttribute('d'))

    # 3. save path to svg file
    for p_obj in path_objs:
        d = p_obj.getAttribute('d')
        content = '<svg version="1.1" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">\n <g transform="scale(1, -1) translate(0, -900)"><path d="' + d + \
            '" fill="black"></path></g></svg>'
        with open("test_%d.svg" % path_objs.index(p_obj), 'w') as f:
            f.write(content)

        drawing = svg2rlg("test_%d.svg" % path_objs.index(p_obj))
        renderPM.drawToFile(drawing, "test_%d.png" % path_objs.index(p_obj), "png")




if __name__ == '__main__':
    path = "13534.svg"
    extract_stroke_path_from_svg(path)