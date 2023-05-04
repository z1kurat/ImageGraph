class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def contains(self, point):
        return (self.x1 <= point.x <= self.x2 and
                self.y1 <= point.y <= self.y2)
