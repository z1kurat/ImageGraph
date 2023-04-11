import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk

from Algorithm import ImageGraph

import cv2


def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open image
        image = cv2.imread(file_path)

        # Create graph
        image = ImageGraph.create_graph(image)

        # Prepare the format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)

        # Update view
        label.config(image=photo)
        label.image = photo


# Start window
root = tk.Tk()
root.title("Выберите фотографию")

# Prepare button
button = tk.Button(root, text="Выбрать файл", command=open_file)
button.pack()

# Set init image
label = tk.Label(root)
label.pack()

# Open window
root.mainloop()
