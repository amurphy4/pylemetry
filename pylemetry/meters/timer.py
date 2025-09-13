from typing import Generator

import time

from contextlib import contextmanager
from threading import Lock


class Timer:
    def __init__(self):
        self.lock = Lock()
        self.ticks = []

    def tick(self, tick: float) -> None:
        with self.lock:
            self.ticks.append(tick)

    @contextmanager
    def time(self) -> Generator[None, None, None]:
        start_time = time.perf_counter()

        try:
            yield
        finally:
            end_time = time.perf_counter()

            self.tick(end_time - start_time)

    def get_count(self) -> int:
        return len(self.ticks)

    def get_mean_tick_time(self) -> float:
        return sum(self.ticks) / len(self.ticks)
