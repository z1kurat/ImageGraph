import tkinter
from tkinter import filedialog, NW, messagebox

from PIL import Image, ImageTk, ImageDraw

import Algorithm.SelectContur

from Geometry.Point import Point

from Utils.ClosedAreaFinder import ClosedAreaFinder
from Utils.DrawingUtils import DrawingUtils

from Utils.Constant import FILE_NAME


class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.start_recover = None
        self.end_scale_rectangle = None
        self.start_scale_rectangle = None
        self.scale_box = None
        self.render_button = None
        self.undo_button = None
        self.select_button = None
        self.clear_button = None
        self.binary_image = None
        self.pil_image = None
        self.canvas = None
        self.drawing_utils = None
        self.closed_area_finder = None
        self.image = None
        self.image_path = None
        self.areas = []
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tkinter.Button(self, text="Выбрать фотографию", command=self.select_image)
        self.select_button.grid(row=0, column=0, padx=10, pady=5)

        self.undo_button = tkinter.Button(self, text="Отменить", command=self.clear_line)
        self.undo_button.grid(row=0, column=1, padx=10, pady=5)

        self.clear_button = tkinter.Button(self, text="Очистить все", command=self.clear_all)
        self.clear_button.grid(row=0, column=2, padx=10, pady=5)

        self.render_button = tkinter.Button(self, text="Выделить контуры", command=self.select_contur)
        self.render_button.grid(row=0, column=3, padx=10, pady=5)

        self.scale_box = tkinter.Entry(self, validate="key")
        self.scale_box.grid(row=0, column=4, padx=10, pady=5)

        self.canvas = tkinter.Canvas(master=self.master,
                                     width=self.master.winfo_screenwidth() * 0.8,
                                     height=self.master.winfo_screenheight() * 0.5,
                                     bg="white")

        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.start_scale)
        self.canvas.bind("<B1-Motion>", self.sub_scale_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.end_scale)

        self.drawing_utils = DrawingUtils(canvas=self.canvas)
        self.closed_area_finder = ClosedAreaFinder()

    def start_scale(self, event):
        self.start_scale_rectangle = Point(event.x, event.y)

    def sub_scale_drawing(self, event):
        self.drawing_utils.remove_all_object()
        self.drawing_utils.draw_rectangle(self.start_scale_rectangle, Point(event.x, event.y))

    def end_scale(self, event):
        self.end_scale_rectangle = Point(event.x, event.y)

        self.canvas.bind("<Button-1>", self.start_select_area)
        self.canvas.bind("<B1-Motion>", self.draw_sub_area)
        self.canvas.bind("<ButtonRelease-1>", self.add_line_to_area)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            self.pil_image = Image.open(self.image_path).resize((self.master.winfo_screenwidth(),
                                                                 self.master.winfo_screenheight()))
            self.image = ImageTk.PhotoImage(self.pil_image)
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)
            self.clear_all()

    def start_select_area(self, event):
        if self.closed_area_finder.closed_area:
            return

        start_point = self.closed_area_finder.get_last_point()
        if start_point is not None:
            self.drawing_utils.draw_line(start_point, Point(event.x, event.y))

        if self.closed_area_finder.start_point is None:
            self.closed_area_finder.add_point(Point(event.x, event.y))

    def draw_sub_area(self, event):
        if self.closed_area_finder.closed_area:
            return

        start_point = self.closed_area_finder.get_last_point()
        if start_point is None:
            return

        self.drawing_utils.remove_last_object()
        self.drawing_utils.draw_line(start_point, Point(event.x, event.y))

    def add_line_to_area(self, event):
        if self.closed_area_finder.closed_area:
            return

        self.drawing_utils.remove_last_object()

        start_point = self.closed_area_finder.get_last_point()
        self.closed_area_finder.add_point(Point(event.x, event.y))
        if start_point is not None:
            self.drawing_utils.draw_line(start_point, self.closed_area_finder.get_last_point())

    def clear_line(self):
        self.drawing_utils.remove_last_object()
        self.closed_area_finder.remove_last_point()

    def clear_all(self):
        self.drawing_utils.remove_all_object()
        self.closed_area_finder.remove_all_points()

    def select_contur(self):
        if not self.image_path:
            messagebox.showinfo("Внимание", "Не выбрано изображение")
            return

        if not self.closed_area_finder.closed_area:
            messagebox.showinfo("Внимание", "Не выбран контур")
            return

        self.binary_image = Algorithm.SelectContur.convert_to_binary(self.pil_image.copy(),
                                                                     self.closed_area_finder.points)

        self.binary_image = Image.open(FILE_NAME).resize((self.master.winfo_screenwidth(),
                                                          self.master.winfo_screenheight()))

        self.image = ImageTk.PhotoImage(self.binary_image)

        self.canvas.create_image(0, 0, image=self.image, anchor=NW)
        self.clear_all()

        self.canvas.bind("<Button-1>", self.start_recover_graph)
        self.canvas.bind("<B1-Motion>", self.sub_recover_drawing)
        self.canvas.bind("<ButtonRelease-1>", self.end_recover)

    def start_recover_graph(self, event):
        self.start_recover = Point(event.x, event.y)

    def sub_recover_drawing(self, event):
        self.drawing_utils.remove_all_object()
        self.drawing_utils.draw_line(self.start_recover, Point(event.x, event.y))

    def end_recover(self, event):
        self.drawing_utils.remove_all_object()

        self.binary_image = Image.open(FILE_NAME).resize((self.master.winfo_screenwidth(),
                                                          self.master.winfo_screenheight()))
        draw = ImageDraw.Draw(self.binary_image)

        draw.line([(self.start_recover.x, self.start_recover.y), (event.x, event.y)], fill=(0, 0, 0), width=2)

        self.binary_image.save(FILE_NAME)

        self.binary_image = Image.open(FILE_NAME).resize((self.master.winfo_screenwidth(),
                                                          self.master.winfo_screenheight()))

        self.image = ImageTk.PhotoImage(self.binary_image)

        self.canvas.create_image(0, 0, image=self.image, anchor=NW)
        self.clear_all()

