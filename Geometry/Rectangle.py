class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    @staticmethod
    def create(point1, point2):
        return Rectangle(point1.x, point1.y, point2.x, point2.y)

    def contains(self, point):
        return (self.x1 <= point.x <= self.x2 and
                self.y1 <= point.y <= self.y2)
