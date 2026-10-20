import logging
from typing import Protocol

from pylemetry import registry
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
        reporting_type: ReportingType,
        clear_registry_on_exit: bool = False,
        universal_tags: Tags | None = None,
        verbose_tags: bool = False,
    ) -> None:
        super().__init__(interval, reporting_type, clear_registry_on_exit, universal_tags, verbose_tags)

        self.logger = logger
        self.level = level

    def flush(self) -> None:
        for _, meters in registry.METERS.items():
            for _, meter in meters.items():
                self._log(
                    self.format_message(self.message_formats[meter.meter_type], meter, self.since_last_interval),
                )

                if self.since_last_interval:
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
