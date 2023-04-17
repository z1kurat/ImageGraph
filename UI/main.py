import tkinter as tk
from tkinter import filedialog

from Algorithm import ImageGraph

import cv2


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        ImageGraph.convert_to_binary(file_path, "binary.jpg", 180, 180, 180)

        image = cv2.imread("binary.jpg")
        ImageGraph.create_graph(image)


root = tk.Tk()
root.title("Выберите фотографию")

button = tk.Button(root, text="Выбрать файл", command=open_file)
button.pack()

label = tk.Label(root)
label.pack()

root.mainloop()
