class Gauge:
    def __init__(self):
        self.value = 0.0

    def get_value(self) -> float:
        return self.value

    def add(self, value: float) -> None:
        self.value += value

    def subtract(self, value: float) -> None:
        self.value -= value

    def __add__(self, other: float) -> "Gauge":
        self.add(other)

        return self

    def __sub__(self, other: float) -> "Gauge":
        self.subtract(other)

        return self
