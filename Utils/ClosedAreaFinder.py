from Geometry.Point import Point
from Utils.Constant import TOLERANCE


class ClosedAreaFinder:
    def __init__(self):
        self.points = []
        self.start_point = None
        self.closed_area = False

    def add_point(self, point: Point):
        if self.is_closed_area(point):
            self.closed_area = True
            self.points.append(self.start_point)
            return

        if self.start_point is None:
            self.start_point = point

        self.points.append(point)

    def is_closed_area(self, point: Point) -> bool:
        if self.start_point is None:
            return False

        distance = Point.distance_with_points(self.start_point, point)
        if distance < TOLERANCE:
            return True

        return False

    def get_last_point(self):
        if len(self.points) == 0:
            return None

        return self.points[-1]

    def remove_last_point(self):
        if len(self.points) == 0:
            return

        if len(self.points) == 1:
            self.points = []
            self.start_point = None
            return

        if len(self.points) > 1:
            self.points.pop()
            self.closed_area = False
            return

    def remove_all_points(self):
        self.points = []
        self.start_point = None
        self.closed_area = False
