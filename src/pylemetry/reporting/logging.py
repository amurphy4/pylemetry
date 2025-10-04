from typing import Protocol, ParamSpec, TypeVar, Optional

from pylemetry import registry
from pylemetry.meters import MeterType
from pylemetry.reporting.reporter import Reporter
from pylemetry.reporting.reporting_type import ReportingType

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
    def __init__(self, interval: float, logger: Loggable, level: int, _type: ReportingType):
        super().__init__(interval)

        self.logger = logger
        self.level = level
        self._type = _type

        self.message_formats = {
            MeterType.COUNTER: "{name} [{type}] -- {value}",
            MeterType.GAUGE: "{name} [{type}] -- {value}",
            MeterType.TIMER: "{name} [{type}] -- {value}",
        }

    def configure_message_format(self, message_format: str, meter_type: Optional[MeterType] = None):
        if not meter_type:
            for _type in list(MeterType):
                self.message_formats[_type] = message_format
        else:
            self.message_formats[meter_type] = message_format

    def flush(self) -> None:
        since_last_interval = self._type == ReportingType.INTERVAL

        for meters in [registry.COUNTERS, registry.GAUGES, registry.TIMERS]:
            for name, meter in meters.items():  # type: ignore
                self.logger.log(
                    self.level,
                    self.format_message(self.message_formats[meter.meter_type], name, meter, since_last_interval),
                )

                if since_last_interval:
                    meter.mark_interval()
