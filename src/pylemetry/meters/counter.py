from threading import Lock


class Counter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0
        self.last_interval_count = 0

    def get_count(self, since_last_interval: bool = False) -> int:
        """
        Get the count from this counter

        :param since_last_interval: If true, returns the count since the last marked interval, otherwise returns the
        full count
        :return: Count from this counter
        """

        if since_last_interval:
            return self.count - self.last_interval_count
        else:
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

    def mark_interval(self) -> None:
        """
        Mark an interval and update the most recent interval value
        """

        with self.lock:
            self.last_interval_count = self.count
