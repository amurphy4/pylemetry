from typing import Protocol, ParamSpec, TypeVar, Union

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
    def __init__(self, interval: int, message_format: str, sink: Loggable, level: int, _type: ReportingType):
        super().__init__(interval)

        self.message_format = message_format
        self.sink = sink
        self.level = level
        self._type = _type

        self.__values_at_interval: dict[str, dict[str, Union[int, float]]] = {}

    def flush(self) -> None:
        self.sink.log(self.level, "Hello world!")
