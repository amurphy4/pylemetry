from typing import Protocol, ParamSpec, TypeVar

from pylemetry import registry
from pylemetry.reporting import Reporter, ReportingType

P = ParamSpec("P")
R = TypeVar("R", covariant=True)


class Loggable(Protocol[P, R]):
    def log(self, level: int, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def debug(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def info(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def warn(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def error(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def critical(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...

    def exception(self, msg: str, *args: P.args, **kwargs: P.kwargs) -> R: ...


class LoggingReporter(Reporter):
    def __init__(self, interval: int, message_format: str, logger: Loggable, level: int, _type: ReportingType):
        super().__init__(interval)

        self.message_format = message_format
        self.logger = logger
        self.level = level
        self._type = _type

    def flush(self) -> None:
        since_last_interval = self._type == ReportingType.INTERVAL

        for meters in [registry.COUNTERS, registry.GAUGES, registry.TIMERS]:
            for name, meter in meters.items():  # type: ignore
                self.logger.log(self.level, self.format_message(self.message_format, name, meter, since_last_interval))
