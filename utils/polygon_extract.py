# coding: utf-8
def extractStorkeByPolygon(image, polygon):

    image_ = image.copy()

    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if not ray_tracing_method(x, y, polygon):
                image_[y][x] = 255

    return image_


# Ray tracing check point in polygon
def ray_tracing_method(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside