from Geometry.Point import Point

from Utils.BoundingBoxCreater import BoundingBox

from Utils.ClosedAreaDetector import ClosedAreaDetector

from Utils.Constant import MAX_R
from Utils.Constant import MAX_G
from Utils.Constant import MAX_B

from Utils.Constant import FILE_NAME


def select_contur(image, points):
    binary_image = convert_to_binary(image, points)
    graph_conversion(binary_image)


def graph_conversion(binary_image):
    #!toDO: pass your code here

    # to consider the meaning of the image
    # width, height = binary_image.size
    #     for x in range(width):
    #         for y in range(height):
    #           r, g, b = binary_image.getpixel((x, y))
    #           your code

    pass


def convert_to_binary(image, points):
    width, height = image.size

    white = (255, 255, 255)
    black = (0, 0, 0)

    bounding_box = BoundingBox(points)
    closed_area_detector = ClosedAreaDetector(points)

    for x in range(width):
        for y in range(height):
            if not bounding_box.contains(Point(x, y)):
                image.putpixel((x, y), white)
                continue

            r, g, b = image.getpixel((x, y))
            if not (r < MAX_R and g < MAX_G and b < MAX_B):
                image.putpixel((x, y), white)
                continue

            if not closed_area_detector.contains((x, y)):
                image.putpixel((x, y), white)
                continue

            image.putpixel((x, y), black)

    image.save(FILE_NAME)

    return image
