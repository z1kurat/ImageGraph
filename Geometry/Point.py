from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance_with_points(point, other_point) -> float:
        distance = sqrt((point.x - other_point.x) ** 2 + (point.y - other_point.y) ** 2)
        return distance
