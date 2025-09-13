from threading import Lock


class Counter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def get_count(self) -> int:
        return self.count

    def add(self, value: int = 1) -> None:
        with self.lock:
            self.count += value

    def __add__(self, other: int) -> "Counter":
        self.add(other)

        return self
