import re

from typing import Callable, Optional, ParamSpec, TypeVar, Union

from functools import wraps

from pylemetry import registry
from pylemetry.meters import Counter


P = ParamSpec("P")
R = TypeVar("R", covariant=True)


def count(
    name: Optional[str] = None, tags: Optional[dict[str, Union[str, int, float]]] = None
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to count the number of invocations of a given callable. Creates a Counter meter in the Registry
    with either the provided name or the fully qualified name of the callable object as the metric name.

    :param name: Name of the meter to create, if None the function name is used
    :param tags: Optional key-value pairs of tags for this meter
    :return: Result of the wrapped function
    """

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            counter_name = f.__qualname__ if name is None else name

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

            counter = registry.get_counter(counter_name, tags=_tags)

            if not counter:
                counter = Counter(name=counter_name, tags=_tags)
                registry.add_counter(counter)

            counter += 1

            return f(*args, **kwargs)

        return wrapper

    return decorator
