from typing import Callable, Any

from functools import wraps

from pylemetry import Registry
from pylemetry.meters import Counter


def count(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to count the number of invocations of a given callable. Creates a Counter meter in the Registry
    with the fully qualified name of the callable object as the metric name.

    :param f: Callable to wrap
    :return: Result of f
    """

    @wraps(f)
    def wrapper() -> Any:
        counter_name = f.__qualname__

        counter = Registry().get_counter(counter_name)

        if not counter:
            counter = Counter()
            Registry().add_counter(counter_name, counter)

        counter += 1

        return f()

    return wrapper
