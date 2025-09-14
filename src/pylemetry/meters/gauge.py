from threading import Lock


class Gauge:
    def __init__(self):
        self.lock = Lock()
        self.value = 0.0

    def get_value(self) -> float:
        """
        Get the value from this gauge

        :return: Value within this gauge
        """

        return self.value

    def set_value(self, value: float):
        """
        Set the value within this gauge

        :param value: Value to set this gauge to
        """

        with self.lock:
            self.value = value

    def add(self, value: float) -> None:
        """
        Add a value to the value within this gauge

        :param value: Value to add
        """

        with self.lock:
            self.value += value

    def subtract(self, value: float) -> None:
        """
        Subtract a value from the value within this gauge

        :param value: Value to subtract
        """

        with self.lock:
            self.value -= value

    def __add__(self, other: float) -> "Gauge":
        self.add(other)

        return self

    def __sub__(self, other: float) -> "Gauge":
        self.subtract(other)

        return self
