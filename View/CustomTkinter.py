import tkinter
from tkinter import filedialog, NW, messagebox

from PIL import Image, ImageTk, ImageDraw

import Algorithm.SelectContur

from Geometry.Point import Point
from Geometry.Rectangle import Rectangle

from Utils.ClosedAreaFinder import ClosedAreaFinder
from Utils.DrawingUtils import DrawingUtils

from Parameters.Constant import FILE_NAME


class Application(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.current_step = None
        self.load_image_button = None
        self.speed_box = None
        self.scaling_button = None
        self.start_recovering_point = None
        self.end_scaling_rectangle = None
        self.start_scaling_rectangle = None
        self.render_button = None
        self.undo_button = None
        self.select_button = None
        self.clear_button = None
        self.image = None
        self.pil_image = None
        self.image_path = None
        self.canvas = None
        self.drawing_utils = None
        self.closed_area_finder = None
        self.is_contur_selected = False
        self.areas = []
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.load_image_button = tkinter.Button(self, text="Выбрать фотографию", command=self.load_image)
        self.load_image_button.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.undo_button = tkinter.Button(self, text="Отменить", command=self.undo)
        self.undo_button.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.clear_button = tkinter.Button(self, text="Очистить все", command=self.clear_all)
        self.clear_button.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        self.scaling_button = tkinter.Button(self, text="Задать масштаб", command=self.set_scaling_mode)
        self.scaling_button.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        self.select_button = tkinter.Button(self, text="Выделить контуры", command=self.select_contur)
        self.select_button.grid(row=0, column=4, padx=10, pady=5, sticky='w')

        self.render_button = tkinter.Button(self, text="Обработка контура", command=self.render_graph)
        self.render_button.grid(row=0, column=5, padx=10, pady=5, sticky='w')

        self.speed_box = tkinter.Entry(self, validate="key")
        self.speed_box.grid(row=0, column=6, padx=10, pady=5, sticky='w')

        self.current_step = tkinter.Label(self, text="")
        self.current_step.grid(row=0, column=8, padx=10, pady=5, sticky='w')

        self.canvas = tkinter.Canvas(master=self.master,
                                     width=self.master.winfo_screenwidth() * 0.8,
                                     height=self.master.winfo_screenheight() * 0.5,
                                     bg="white")

        self.canvas.pack(side="top", fill="both", expand=True)

        self.drawing_utils = DrawingUtils(canvas=self.canvas)
        self.closed_area_finder = ClosedAreaFinder()

    # Image block
    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if self.image_path:
            self.update_image(self.image_path)
            self.set_scaling_mode()

    def update_image(self, path, need_resize=True):
        self.pil_image = Image.open(path)

        if need_resize:
            self.pil_image = self.pil_image.resize((self.master.winfo_screenwidth(),
                                                    self.master.winfo_screenheight()))

        self.image = ImageTk.PhotoImage(self.pil_image)
        self.canvas.create_image(0, 0, image=self.image, anchor=NW)
        self.clear_all()

    # Undo block
    def undo(self):
        self.drawing_utils.remove_last_object()
        self.closed_area_finder.remove_last_point()

    def clear_all(self):
        self.drawing_utils.remove_all_object()
        self.closed_area_finder.remove_all_points()

    # Select contur
    def is_set_all_value_for_select_contur(self) -> bool:
        if not self.image_path:
            messagebox.showinfo("Внимание", "Не выбрано изображение")
            return False

        if not self.closed_area_finder.closed_area:
            messagebox.showinfo("Внимание", "Не выбран контур")
            return False

        return True

    def select_contur(self):
        if not self.is_set_all_value_for_select_contur():
            return

        Algorithm.SelectContur.convert_to_binary(self.pil_image.copy(), self.closed_area_finder.points)

        self.update_image(FILE_NAME, False)
        self.set_recovering_mode()

        self.is_contur_selected = True

    # Render graph
    def is_set_all_value_for_render_graph(self):
        if not self.is_contur_selected:
            messagebox.showinfo("Внимание", "Не выделен контур")
            return False

        if not self.start_scaling_rectangle or not self.end_scaling_rectangle:
            messagebox.showinfo("Внимание", "Не задан масштаб")
            return False

        if not self.is_scaling_correct():
            messagebox.showinfo("Внимание", "Не задана скорость")
            return False

        return True

    def render_graph(self):
        if not self.is_set_all_value_for_render_graph():
            return

        self.current_step.config(text="Обработка графика")

        Algorithm.SelectContur.render_graph(self.pil_image,
                                            Rectangle.create(self.start_scaling_rectangle, self.end_scaling_rectangle),
                                            self.get_scaling_value())
        self.update_image(self.image_path)
        self.is_contur_selected = False
        self.set_selecting_mode()

    # Scaling mode
    def set_scaling_mode(self):
        self.current_step.config(text="Задание масштаба")

        self.clear_all()

        self.canvas.bind("<Button-1>", self.start_scaling)
        self.canvas.bind("<B1-Motion>", self.draw_sub_scaling)
        self.canvas.bind("<ButtonRelease-1>", self.end_scaling)

    def start_scaling(self, event):
        self.start_scaling_rectangle = Point(event.x, event.y)

    def draw_sub_scaling(self, event):
        self.drawing_utils.remove_all_object()
        self.drawing_utils.draw_rectangle(self.start_scaling_rectangle, Point(event.x, event.y))

    def end_scaling(self, event):
        self.end_scaling_rectangle = Point(event.x, event.y)
        self.set_selecting_mode()

    def get_scaling_value(self) -> str:
        return self.speed_box.get()

    def is_scaling_correct(self) -> bool:
        return self.get_scaling_value().isdigit()

    # Selecting mode
    def set_selecting_mode(self):
        self.current_step.config(text="Выделение контура")

        self.clear_all()

        self.canvas.bind("<Button-1>", self.start_selecting)
        self.canvas.bind("<B1-Motion>", self.draw_sub_selecting)
        self.canvas.bind("<ButtonRelease-1>", self.end_selecting)

    def start_selecting(self, event):
        if self.closed_area_finder.closed_area:
            return

        start_point = self.closed_area_finder.get_last_point()
        if start_point is not None:
            self.drawing_utils.draw_line(start_point, Point(event.x, event.y))

        if self.closed_area_finder.start_point is None:
            self.closed_area_finder.add_point(Point(event.x, event.y))

    def draw_sub_selecting(self, event):
        if self.closed_area_finder.closed_area:
            return

        start_point = self.closed_area_finder.get_last_point()
        if start_point is None:
            return

        self.drawing_utils.remove_last_object()
        self.drawing_utils.draw_line(start_point, Point(event.x, event.y))

    def end_selecting(self, event):
        if self.closed_area_finder.closed_area:
            return

        self.drawing_utils.remove_last_object()

        start_point = self.closed_area_finder.get_last_point()
        self.closed_area_finder.add_point(Point(event.x, event.y))
        if start_point is not None:
            self.drawing_utils.draw_line(start_point, self.closed_area_finder.get_last_point())

    # Recovering mode
    def set_recovering_mode(self):
        self.current_step.config(text="Восстановление графика")

        self.clear_all()

        self.canvas.bind("<Button-1>", self.start_recovering)
        self.canvas.bind("<B1-Motion>", self.draw_sub_recovering)
        self.canvas.bind("<ButtonRelease-1>", self.end_recovering)

    def start_recovering(self, event):
        self.start_recovering_point = Point(event.x, event.y)

    def draw_sub_recovering(self, event):
        self.drawing_utils.remove_last_object()
        self.drawing_utils.draw_line(self.start_recovering_point, Point(event.x, event.y))

    def end_recovering(self, event):
        self.drawing_utils.remove_last_object()

        draw = ImageDraw.Draw(self.pil_image)

        start_line = (self.start_recovering_point.x, self.start_recovering_point.y)
        end_line = (event.x, event.y)

        draw.line([start_line, end_line], fill=(0, 0, 0), width=2)

        self.pil_image.save(FILE_NAME)
        self.update_image(FILE_NAME, False)
