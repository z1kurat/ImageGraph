import cv2

from PIL import Image


def convert_to_binary(image_path, file_name, max_r, max_g, max_b):
    image = Image.open(image_path)
    width, height = image.size

    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if r < max_r and g < max_g and b < max_b:
                image.putpixel((x, y), (0, 0, 0))
            else:
                image.putpixel((x, y), (255, 255, 255))

    image.save(file_name)


def create_graph(image):
    bit_graph = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(bit_graph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(bit_graph, contours, -1, (255, 0, 0), 3)
    cv2.imshow("Image", bit_graph)
