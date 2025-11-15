from typing import Union, Optional

from pylemetry.meters.meter import Meter, MeterType


class Counter(Meter):
    def __init__(self, name: str, tags: Optional[dict[str, Union[str, int, float]]] = None) -> None:
        super().__init__(MeterType.COUNTER, name, tags)

    def add(self, value: int = 1) -> None:
        """
        Add a value to the count within this counter

        :param value: Value to add, default 1
        """

        with self.lock:
            self.value += value

    def __add__(self, other: int) -> "Counter":
        self.add(other)

        return self
