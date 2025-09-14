from threading import Lock


class Counter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def get_count(self) -> int:
        """
        Get the count from this counter

        :return: Count from this counter
        """

        return self.count

    def add(self, value: int = 1) -> None:
        """
        Add a value to the count within this counter

        :param value: Value to add, default 1
        """

        with self.lock:
            self.count += value

    def __add__(self, other: int) -> "Counter":
        self.add(other)

        return self
