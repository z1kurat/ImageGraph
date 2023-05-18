from Geometry.Rectangle import Rectangle


class BoundingBox:
    def __init__(self, points):
        self.rectangle = self.create_bounding_box(points)

    def contains(self, point) -> bool:
        return self.rectangle.contains(point)

    @staticmethod
    def create_bounding_box(points):
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for point in points:
            if point.x > max_x:
                max_x = point.x
            if point.x < min_x:
                min_x = point.x
            if point.y > max_y:
                max_y = point.y
            if point.y < min_y:
                min_y = point.y

        return Rectangle(min_x, min_y, max_x, max_y)
