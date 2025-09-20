from typing import Optional

from pylemetry.meters import Counter, Gauge, Timer


COUNTERS: dict[str, Counter] = {}
GAUGES: dict[str, Gauge] = {}
TIMERS: dict[str, Timer] = {}


def clear() -> None:
    """
    Remove all meters from the global registry
    """

    COUNTERS.clear()
    GAUGES.clear()
    TIMERS.clear()


def add_counter(name: str, counter: Counter) -> None:
    """
    Add a counter to the global registry

    :param name: Unique name of the counter
    :param counter: Counter to add

    :raises AttributeError: When the name provided for the counter metric is already in use in the global registry
    """

    if name in COUNTERS:
        raise AttributeError(f"A counter with the name '{name}' already exists")

    COUNTERS[name] = counter


def get_counter(name: str) -> Optional[Counter]:
    """
    Get a counter from the global registry by its name

    :param name: Name of the counter
    :return: Counter in the global registry
    """

    return COUNTERS.get(name)


def remove_counter(name: str) -> None:
    """
    Remove a counter from the global registry

    :param name: Name of the counter to remove
    """

    if name in COUNTERS:
        del COUNTERS[name]


def add_gauge(name: str, gauge: Gauge) -> None:
    """
    Add a gauge to the global registry

    :param name: Unique name of the gauge
    :param gauge: Gauge to add

    :raises AttributeError: When the name provided for the gauge metric is already in use in the global registry
    """

    if name in GAUGES:
        raise AttributeError(f"A gauge with the name '{name}' already exists")

    GAUGES[name] = gauge


def get_gauge(name: str) -> Optional[Gauge]:
    """
    Get a gauge from the global registry by its name

    :param name: Name of the gauge
    :return: Gauge in the global registry
    """

    return GAUGES.get(name)


def remove_gauge(name: str) -> None:
    """
    Remove a gauge from the global registry

    :param name: Name of the gauge to remove
    """

    if name in GAUGES:
        del GAUGES[name]


def add_timer(name: str, timer: Timer) -> None:
    """
    Add a timer to the global registry

    :param name: Unique name of the timer
    :param timer: Timer to add

    :raises AttributeError: When the name provided for the timer metric is already in use in the global registry
    """

    if name in TIMERS:
        raise AttributeError(f"A timer with the name '{name}' already exists")

    TIMERS[name] = timer


def get_timer(name: str) -> Optional[Timer]:
    """
    Get a timer from the global registry by its name

    :param name: Name of the timer
    :return: Timer in the global registry
    """

    return TIMERS.get(name)


def remove_timer(name: str) -> None:
    """
    Remove a timer from the global registry

    :param name: Name of the timer to remove
    """

    if name in TIMERS:
        del TIMERS[name]
