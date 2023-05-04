import cv2

import numpy as np

import matplotlib.path as mpl_path

from Geometry.Point import Point
from Geometry.Rectangle import Rectangle


def get_bounding_box(points):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for point in points:
        if point.x > max_x:
            max_x = point.x
        if point.x < min_x:
            min_x = point.x
        if point.y > max_y:
            max_y = point.y
        if point.y < min_y:
            min_y = point.y

    return Rectangle(min_x, min_y, max_x, max_y)


def convert_to_array(points):
    coords = [(point.x, point.y) for point in points]
    return coords


def convert_to_binary(image, file_name, points, max_r=180, max_g=180, max_b=180):
    width, height = image.size
    bounding_box = get_bounding_box(points)
    closed_area = mpl_path.Path(np.array(convert_to_array(points)))

    for x in range(width):
        for y in range(height):
            if not bounding_box.contains(Point(x, y)):
                image.putpixel((x, y), (255, 255, 255))
                continue

            r, g, b = image.getpixel((x, y))
            if not (r < max_r and g < max_g and b < max_b):
                image.putpixel((x, y), (255, 255, 255))
                continue

            if not closed_area.contains_point((x, y)):
                image.putpixel((x, y), (255, 255, 255))
                continue

            image.putpixel((x, y), (0, 0, 0))

    image.save(file_name)


def create_graph(image):
    bit_graph = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(bit_graph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(bit_graph, contours, -1, (255, 0, 0), 3)
    cv2.imshow("Image", bit_graph)
