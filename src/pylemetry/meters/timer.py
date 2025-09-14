from typing import Generator

import time

from contextlib import contextmanager
from threading import Lock


class Timer:
    def __init__(self):
        self.lock = Lock()
        self.ticks = []

    def tick(self, tick: float) -> None:
        """
        Add a value to the list of ticks within this timer

        :param tick: Value to add to the ticks list
        """

        with self.lock:
            self.ticks.append(tick)

    @contextmanager
    def time(self) -> Generator[None, None, None]:
        """
        Context manager to time in seconds a code block and add the result to the internal ticks list
        """

        start_time = time.perf_counter()

        try:
            yield
        finally:
            end_time = time.perf_counter()

            self.tick(end_time - start_time)

    def get_count(self) -> int:
        """
        Get the count of the number of ticks within this timer

        :return: Number of ticks
        """

        return len(self.ticks)

    def get_mean_tick_time(self) -> float:
        """
        Get the mean tick time from the list of ticks within this timer

        :return: Mean tick time
        """

        return sum(self.ticks) / len(self.ticks)

    def get_max_tick_time(self) -> float:
        """
        Get the maximum tick time from the list of ticks within this timer

        :return: Maximum tick time
        """

        return max(self.ticks)

    def get_min_tick_time(self) -> float:
        """
        Get the minimum tick time from the list of ticks within this timer

        :return: Minimum tick time
        """

        return min(self.ticks)
