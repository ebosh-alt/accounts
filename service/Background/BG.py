from multiprocessing import Process


class BG:
    def __init__(self, ta) -> None:
        self.process = Process()
        self.pid = self.process.pid
        