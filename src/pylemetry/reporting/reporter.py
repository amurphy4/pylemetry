import threading
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from pylemetry import registry
from pylemetry.meters import Counter, Gauge, Meter, MeterType, Timer
from pylemetry.reporting.reporting_type import ReportingType
from pylemetry.utils.types import Tags


class Reporter(ABC):
    def __init__(
        self,
        interval: float,
        reporting_type: ReportingType = ReportingType.INTERVAL,
        clear_registry_on_exit: bool = False,
        universal_tags: Tags | None = None,
        verbose_tags: bool = False,
    ) -> None:
        self.interval = interval
        self.reporting_type = reporting_type
        self.since_last_interval = self.reporting_type == ReportingType.INTERVAL
        self.__timer_thread: threading.Timer | None = None
        self.running = False
        self.clear_registry_on_exit = clear_registry_on_exit

        if universal_tags is None:
            universal_tags = {}

        self.universal_tags = universal_tags
        self.verbose_tags = verbose_tags

        self.message_formats = {
            MeterType.COUNTER: "{name} [{type}] -- {value}",
            MeterType.GAUGE: "{name} [{type}] -- {value}",
            MeterType.TIMER: "{name} [{type}] -- {value}",
        }

    def __enter__(self) -> Self:
        self.start()

        return self

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        self.stop()

        if self.clear_registry_on_exit:
            registry.clear()

    @abstractmethod
    def flush(self) -> None:
        """
        Flush all meter values in the registry. If the reporter is configured using `ReporterType.INTERVAL`, this will
        mark an interval each time it runs and only flush the meter values since the most recent interval
        """
        ...

    def _run(self) -> None:
        self.running = False
        self.flush()
        self.start()

    def start(self) -> None:
        """
        Start running a thread timer with the provided interval to flush the meters periodically
        """

        if not self.running:
            self.__timer_thread = threading.Timer(self.interval, self._run)
            self.__timer_thread.start()
            self.running = True

    def stop(self) -> None:
        """
        Stop the thread timer and flush all meters for a final time
        """

        if self.__timer_thread is not None:
            self.__timer_thread.cancel()

        self.flush()
        self.running = False

    def configure_message_format(self, message_format: str, meter_type: MeterType | None = None) -> None:
        if not meter_type:
            for _type in list(MeterType):
                self.message_formats[_type] = message_format
        else:
            self.message_formats[meter_type] = message_format

    def format_message(self, message_format: str, meter: Meter, since_last_interval: bool = False) -> str:
        """
        Format output messages with the following format options:
            - name: Name of the meter being logged
            - value: Counter or Gauge value, or Timer count
            - min: Counter or Gauge value, or Timer minimum tick value
            - max: Counter or Gauge value, or Timer maximum tick value
            - avg: Counter or Gauge value, or Timer mean tick value
            - type: Meter type
            - tags: The tags associated with the meter

        :param message_format: Message format string
        :param meter: Meter to be output
        :param since_last_interval: If true, values since the last interval will be used. If false, the full value
        will be used
        :return: Formatted output message containing meter values
        """

        if isinstance(meter, Timer):
            message = message_format.format(
                name=meter.name,
                value=meter.get_value(since_last_interval),
                count=meter.get_count(since_last_interval),
                min=meter.get_min_tick_time(since_last_interval),
                max=meter.get_max_tick_time(since_last_interval),
                avg=meter.get_mean_tick_time(since_last_interval),
                type=meter.meter_type,
                tags=self._format_tags(meter.get_tags(), verbose=self.verbose_tags),
            )
        elif isinstance(meter, Counter) or isinstance(meter, Gauge):
            message = message_format.format(
                name=meter.name,
                value=meter.get_value(since_last_interval),
                count=meter.get_value(since_last_interval),
                min=meter.get_value(since_last_interval),
                max=meter.get_value(since_last_interval),
                avg=meter.get_value(since_last_interval),
                type=meter.meter_type,
                tags=self._format_tags(meter.get_tags(), verbose=self.verbose_tags),
            )
        else:
            raise ValueError(f"Unsupported meter of type {type(meter)}")

        return message

    def _format_tags(self, meter_tags: Tags, verbose: bool = False) -> Tags | list[Tags]:
        if verbose:
            return [
                {"name": name, "value": value}
                for tags in [self.universal_tags, meter_tags]
                for name, value in tags.items()
            ]
        else:
            return {**self.universal_tags, **meter_tags}
