from tkinter import Canvas

from Geometry.Point import Point

from Parameters.Constant import COLOR_LINE
from Parameters.Constant import COLOR_OVAL
from Parameters.Constant import COLOR_RECTANGLE
from Parameters.Constant import WIDTH_LINE


class DrawingUtils:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas_object = []

    def draw_line(self, point_start: Point, point_end: Point):
        self.canvas_object.append(self.canvas.create_line(point_start.x, point_start.y,
                                                          point_end.x, point_end.y,
                                                          fill=COLOR_LINE, width=WIDTH_LINE))

    def draw_rectangle(self, point_start: Point, point_end: Point):
        self.canvas_object.append(self.canvas.create_rectangle(point_start.x, point_start.y,
                                                               point_end.x, point_end.y,
                                                               outline=COLOR_RECTANGLE, width=WIDTH_LINE))

    def draw_ellipse(self, point: Point):
        self.canvas_object.append(self.canvas.create_oval((point.x - 10, point.y - 10, point.x + 10, point.y + 10),
                                                          fill=COLOR_OVAL))

    def remove_last_object(self):
        if len(self.canvas_object) != 0:
            self.canvas.delete(self.canvas_object[-1])
            self.canvas_object.pop()

    def remove_all_object(self):
        if len(self.canvas_object) != 0:
            for line in self.canvas_object:
                self.canvas.delete(line)
