from typing import Generator

import time

from contextlib import contextmanager
from threading import Lock


class Timer:
    def __init__(self):
        self.lock = Lock()
        self.ticks = []
        self.last_interval_tick_count = 0

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

    def get_count(self, since_last_interval: bool = False) -> int:
        """
        Get the count of the number of ticks within this timer

        :param since_last_interval: If true, returns the value since the last marked interval, otherwise returns the
        full value
        :return: Number of ticks
        """

        ticks = self.get_ticks_since_last_interval() if since_last_interval else self.ticks

        return len(ticks)

    def get_mean_tick_time(self, since_last_interval: bool = False) -> float:
        """
        Get the mean tick time from the list of ticks within this timer

        :param since_last_interval: If true, returns the value since the last marked interval, otherwise returns the
        full value
        :return: Mean tick time
        """

        ticks = self.get_ticks_since_last_interval() if since_last_interval else self.ticks

        return sum(ticks) / len(ticks)

    def get_max_tick_time(self, since_last_interval: bool = False) -> float:
        """
        Get the maximum tick time from the list of ticks within this timer

        :param since_last_interval: If true, returns the value since the last marked interval, otherwise returns the
        full value
        :return: Maximum tick time
        """

        ticks = self.get_ticks_since_last_interval() if since_last_interval else self.ticks

        return max(ticks)

    def get_min_tick_time(self, since_last_interval: bool = False) -> float:
        """
        Get the minimum tick time from the list of ticks within this timer

        :param since_last_interval: If true, returns the value since the last marked interval, otherwise returns the
        full value
        :return: Minimum tick time
        """

        ticks = self.get_ticks_since_last_interval() if since_last_interval else self.ticks

        return min(ticks)

    def get_ticks_since_last_interval(self) -> list[float]:
        """
        Get a list of the ticks since the most recent marked interval

        :return: List of ticks since the most recent marked interval
        """

        return self.ticks[self.last_interval_tick_count :]

    def mark_interval(self) -> None:
        with self.lock:
            self.last_interval_tick_count = len(self.ticks)
