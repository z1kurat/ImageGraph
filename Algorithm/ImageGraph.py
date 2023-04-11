import cv2

import numpy as np


def create_graph(image):
    # Step 1: Load the image into the program and convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply adaptive thresholding to the image
    max_value = 255
    block_size = 11
    binary_image = cv2.adaptiveThreshold(gray, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY, block_size, 1)

    # Step 3: Use a contour detection algorithm to detect the outlines of the graph
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Remove any contours that are not part of the graph
    graph_contours = []
    max_h, max_w = -1, -1
    height, width, _ = image.shape
    max_contur = None
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if width * 0.9 > w > max_w and height * 0.9 > h > max_h:
            max_w = w
            max_h = h
            max_contur = contour

    graph_contours.append(max_contur)

    # Step 5: Crop the original image to extract only the graph
    x, y, w, h = cv2.boundingRect(np.concatenate(graph_contours))
    graph_image = image[y:y + h, x:x + w]

    bit_graph = cv2.cvtColor(graph_image, cv2.COLOR_BGR2GRAY)
    bit_graph = cv2.adaptiveThreshold(bit_graph, max_value, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, block_size, 3)

    # Step 6: Save the resulting image with only the function graph
    return bit_graph
