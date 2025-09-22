from typing import Optional

import threading


class Reporter:
    def __init__(self, interval: int):
        self.interval = interval
        self.__timer_thread: Optional[threading.Timer] = None
        self.running = False

    def flush(self) -> None:
        raise NotImplementedError()

    def _run(self) -> None:
        self.running = False
        self.flush()
        self.start()

    def start(self) -> None:
        if not self.running:
            self.__timer_thread = threading.Timer(self.interval, self._run)
            self.__timer_thread.start()
            self.running = True

    def stop(self) -> None:
        if self.__timer_thread is not None:
            self.__timer_thread.cancel()

        self.flush()
        self.running = False
