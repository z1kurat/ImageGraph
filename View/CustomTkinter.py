import threading

import tkinter
from tkinter import filedialog, NW, messagebox

from PIL import Image, ImageTk

from Algorithm import SelectContur

from Geometry.Point import Point

from Utils.ClosedAreaFinder import ClosedAreaFinder
from Utils.DrawingUtils import DrawingUtils

from ThreadingTask.Task import Task


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.task_select_contur = None
        self.thread = None
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
        select_button = tkinter.Button(self, text="Выбрать фотографию", command=self.select_image)
        select_button.grid(row=0, column=0)

        clear_button = tkinter.Button(self, text="Отменить", command=self.clear_line)
        clear_button.grid(row=0, column=1)

        render_button = tkinter.Button(self, text="Очистить все", command=self.clear_all)
        render_button.grid(row=0, column=2)

        render_button = tkinter.Button(self, text="Выделить контуры", command=self.select_contur)
        render_button.grid(row=0, column=3)

        self.canvas = tkinter.Canvas(master=self.master,
                                     width=self.master.winfo_screenwidth() * 0.8,
                                     height=self.master.winfo_screenheight() * 0.5,
                                     bg="white")

        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.start_select_area)
        self.canvas.bind("<B1-Motion>", self.draw_sub_area)
        self.canvas.bind("<ButtonRelease-1>", self.add_line_to_area)

        self.drawing_utils = DrawingUtils(canvas=self.canvas)
        self.closed_area_finder = ClosedAreaFinder()

        self.task_select_contur = Task(SelectContur.select_contur)

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

        self.drawing_utils.remove_last_line()
        self.drawing_utils.draw_line(start_point, Point(event.x, event.y))

    def add_line_to_area(self, event):
        if self.closed_area_finder.closed_area:
            return

        self.drawing_utils.remove_last_line()

        start_point = self.closed_area_finder.get_last_point()
        self.closed_area_finder.add_point(Point(event.x, event.y))
        if start_point is not None:
            self.drawing_utils.draw_line(start_point, self.closed_area_finder.get_last_point())

    def clear_line(self):
        self.drawing_utils.remove_last_line()
        self.closed_area_finder.remove_last_point()

    def clear_all(self):
        self.drawing_utils.remove_all_lines()
        self.closed_area_finder.remove_all_points()

    def select_contur(self):
        if not self.image_path:
            messagebox.showinfo("Внимание", "Не выбрано изображение")
            return

        if not self.closed_area_finder.closed_area:
            messagebox.showinfo("Внимание", "Не выбран контур")
            return

        if self.task_select_contur.is_work:
            messagebox.showinfo("Внимание", "Уже запущено выделение контура")
            return

        self.thread = threading.Thread(target=self.task_select_contur.execute,
                                       args=(self.pil_image.copy(), self.closed_area_finder.points))
        self.thread.start()
