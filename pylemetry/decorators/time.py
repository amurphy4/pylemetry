from typing import Callable, Any

from functools import wraps

from pylemetry import Registry
from pylemetry.meters import Timer


def time(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper() -> Any:
        time_name = f.__qualname__

        _timer = Registry().get_timer(time_name)

        if not _timer:
            _timer = Timer()
            Registry().add_timer(time_name, _timer)

        with _timer.time():
            return f()

    return wrapper
