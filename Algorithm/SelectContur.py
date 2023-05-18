from Geometry.Point import Point

from Utils.BoundingBoxCreater import BoundingBox

from Utils.ClosedAreaDetector import ClosedAreaDetector

from Parameters.Constant import MAX_R
from Parameters.Constant import MAX_G
from Parameters.Constant import MAX_B

from Parameters.Constant import FILE_NAME


def render_graph(binary_image, rectangle, speed):
    #!toDO: pass your code here

    # to consider the meaning of the image
    # width, height = new_pill_image.size
    #     for x in range(width):
    #         for y in range(height):
    #           r, g, b = new_pill_image.getpixel((x, y))
    #           your code

    pass


def convert_to_binary(image, points):
    white = (255, 255, 255)
    black = (0, 0, 0)

    bounding_box = BoundingBox(points)
    closed_area_detector = ClosedAreaDetector(points)

    width, height = image.size

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

    image = image.crop((bounding_box.rectangle.x1, bounding_box.rectangle.y1,
                       bounding_box.rectangle.x2, bounding_box.rectangle.y2))

    image.save(FILE_NAME)

    return image
