import threading


class Task:
    def __init__(self, func):
        self.func = func
        self.is_work = False
        self.event = threading.Event()

    def execute(self, pil_image, points):
        self.is_work = True
        self.func(pil_image, points)
        self.is_work = False
