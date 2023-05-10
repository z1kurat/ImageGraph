import numpy as np

import matplotlib.path as mpl_path


class ClosedAreaDetector:
    def __init__(self, points):
        self.detector = mpl_path.Path(np.array(self.convert_to_array(points)))

    def contains(self, point) -> bool:
        return self.detector.contains_point(point)

    @staticmethod
    def convert_to_array(points):
        coords = [(point.x, point.y) for point in points]
        return coords
