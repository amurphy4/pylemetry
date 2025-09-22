from typing import Optional, Union

import threading

from pylemetry.meters import Counter, Gauge, Timer


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

    @staticmethod
    def format_message(
        message_format: str, meter_name: str, meter: Union[Counter, Gauge, Timer], since_last_interval: bool = False
    ) -> str:
        if isinstance(meter, Counter):
            message = message_format.format(
                name=meter_name,
                value=meter.get_count(since_last_interval),
                min=meter.get_count(since_last_interval),
                max=meter.get_count(since_last_interval),
                avg=meter.get_count(since_last_interval),
            )
        elif isinstance(meter, Gauge):
            message = message_format.format(
                name=meter_name,
                value=meter.get_value(since_last_interval),
                min=meter.get_value(since_last_interval),
                max=meter.get_value(since_last_interval),
                avg=meter.get_value(since_last_interval),
            )
        elif isinstance(meter, Timer):
            message = message_format.format(
                name=meter_name,
                value=meter.get_count(since_last_interval),
                min=meter.get_min_tick_time(since_last_interval),
                max=meter.get_max_tick_time(since_last_interval),
                avg=meter.get_mean_tick_time(since_last_interval),
            )
        else:
            raise ValueError(f"Unsupported meter of type {type(meter)}")

        return message
