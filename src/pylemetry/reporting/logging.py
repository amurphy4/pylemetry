import logging
from typing import Protocol

from pylemetry import registry
from pylemetry.meters import MeterType
from pylemetry.reporting.reporter import Reporter
from pylemetry.reporting.reporting_type import ReportingType
from pylemetry.utils.types import Tags


class Loggable(Protocol):
    def debug(self, msg: str) -> None: ...

    def info(self, msg: str) -> None: ...

    def warning(self, msg: str) -> None: ...

    def error(self, msg: str) -> None: ...

    def critical(self, msg: str) -> None: ...


class LoggingReporter(Reporter):
    def __init__(
        self,
        interval: float,
        logger: Loggable,
        level: int,
        _type: ReportingType,
        clear_registry_on_exit: bool = False,
        universal_tags: Tags | None = None,
    ) -> None:
        super().__init__(interval, clear_registry_on_exit, universal_tags)

        self.logger = logger
        self.level = level
        self._type = _type

        self.message_formats = {
            MeterType.COUNTER: "{name} [{type}] -- {value}",
            MeterType.GAUGE: "{name} [{type}] -- {value}",
            MeterType.TIMER: "{name} [{type}] -- {value}",
        }

    def configure_message_format(self, message_format: str, meter_type: MeterType | None = None) -> None:
        if not meter_type:
            for _type in list(MeterType):
                self.message_formats[_type] = message_format
        else:
            self.message_formats[meter_type] = message_format

    def flush(self) -> None:
        since_last_interval = self._type == ReportingType.INTERVAL

        for _, meters in registry.METERS.items():
            for _, meter in meters.items():
                self._log(
                    self.format_message(self.message_formats[meter.meter_type], meter, since_last_interval),
                )

                if since_last_interval:
                    meter.mark_interval()

    def _log(self, message: str) -> None:
        # Check the log level manually for compatibility with libraries like Loguru
        if self.level == logging.DEBUG:
            self.logger.debug(message)
        elif self.level == logging.INFO:
            self.logger.info(message)
        elif self.level == logging.WARNING or self.level == logging.WARN:
            self.logger.warning(message)
        elif self.level == logging.ERROR:
            self.logger.error(message)
        elif self.level == logging.CRITICAL:
            self.logger.critical(message)
