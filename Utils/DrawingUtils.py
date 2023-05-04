from tkinter import Canvas

from Geometry.Point import Point

from Utils.Constant import COLOR_LINE
from Utils.Constant import WIDTH_LINE


class DrawingUtils:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas_lines = []

    def draw_line(self, point_start: Point, point_end: Point):
        self.canvas_lines.append(self.canvas.create_line(point_start.x, point_start.y,
                                                         point_end.x, point_end.y,
                                                         fill=COLOR_LINE, width=WIDTH_LINE))

    def remove_last_line(self):
        if len(self.canvas_lines) != 0:
            self.canvas.delete(self.canvas_lines[-1])
            self.canvas_lines.pop()

    def remove_all_lines(self):
        if len(self.canvas_lines) != 0:
            for line in self.canvas_lines:
                self.canvas.delete(line)
