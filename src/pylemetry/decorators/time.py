import re

from typing import Callable, Optional, ParamSpec, TypeVar, Union

from functools import wraps

from pylemetry import registry
from pylemetry.meters import Timer
from pylemetry.utils import TimerUnits


P = ParamSpec("P")
R = TypeVar("R", covariant=True)


def time(
    name: Optional[str] = None,
    unit: TimerUnits = TimerUnits.NANOSECONDS,
    tags: Optional[dict[str, Union[str, int, float]]] = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to time the invocations of a given callable. Creates a Timer meter in the Registry with either the
    provided name or the fully qualified name of the callable object as the metric name.

    :param name: Name of the meter to create, if None the function name is used
    :param unit: Unit of time to measure in
    :param tags: Optional key-value pairs of tags for this meter
    :return: Result of the wrapped function
    """

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            time_name = f.__qualname__ if name is None else name

            _tags: dict[str, Union[str, int, float]] = {}

            if tags:
                for key, value in tags.items():
                    args_match = re.search(r"^args\[[0-9]+]", str(value))
                    kwargs_match = re.search(r"^kwargs\[[a-zA-Z0-9_]+]", str(value))

                    if args_match:
                        args_index = int(args_match.group().replace("args[", "").replace("]", ""))

                        if args_index >= len(args):
                            raise IndexError(f"args index {args_index} out of range, args has length {len(args)}")

                        if not isinstance(args[args_index], (str, int, float)):
                            raise ValueError(
                                f"Only args of types (str | int | float) may be added as tags. "
                                f"Got {args[args_index].__class__}"
                            )

                        _tags[key] = args[args_index]  # type: ignore
                    elif kwargs_match:
                        kwargs_key = kwargs_match.group().replace("kwargs[", "").replace("]", "")

                        if kwargs_key not in kwargs:
                            raise KeyError(f"Key '{kwargs_key}' not present in kwargs")

                        if not isinstance(kwargs[kwargs_key], (str, int, float)):
                            raise ValueError(
                                f"Only kwargs of types (str | int | float) may be added as tags. "
                                f"Got {kwargs[kwargs_key].__class__}"
                            )

                        _tags[key] = kwargs[kwargs_key]  # type: ignore
                    else:
                        _tags[key] = value

            _timer = registry.get_timer(time_name, tags=_tags)

            if not _timer:
                _timer = Timer(time_name, unit=unit, tags=_tags)
                registry.add_timer(_timer)

            with _timer.time():
                return f(*args, **kwargs)

        return wrapper

    return decorator
