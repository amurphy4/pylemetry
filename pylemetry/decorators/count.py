from typing import Callable, Any

from functools import wraps

from pylemetry import Registry
from pylemetry.meters import Counter


def count(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper() -> Any:
        counter_name = f.__name__ + "_calls"

        counter = Registry().get_counter(counter_name)

        if not counter:
            counter = Counter()
            Registry().add_counter(counter_name, counter)

        counter += 1

        return f()

    return wrapper
