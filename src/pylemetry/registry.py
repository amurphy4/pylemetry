from collections.abc import Mapping
from typing import Optional, Union

from pylemetry.meters import Counter, Gauge, Timer, Meter, MeterType

METERS: dict[MeterType, dict[str, Meter]] = {
    MeterType.COUNTER: {},
    MeterType.GAUGE: {},
    MeterType.TIMER: {},
}


def clear() -> None:
    """
    Remove all meters from the global registry
    """

    for _, meters in METERS.items():
        meters.clear()


def add_meter(meter: Meter) -> None:
    """
    Add a meter to the global registry

    :param meter: Meter to add

    :raises AttributeError: When the name provided for the meter of this type is already in use in the global registry
    """

    serialized_tags = [f"{key}-{value}" for key, value in meter.get_tags().items()]

    combined_name = f"{meter.name}{'_'.join(serialized_tags)}"

    if combined_name in METERS[meter.meter_type]:
        raise AttributeError(
            f"A {meter.meter_type.value} with the name '{meter.name}' and the same tags already exists"
        )

    METERS[meter.meter_type][combined_name] = meter


def get_meter(
    name, meter_type: MeterType, tags: Optional[Mapping[str, Union[str, int, float]]] = None
) -> Optional[Meter]:
    """
    Get a meter from the global registry by its name

    :param name: Name of the meter
    :param meter_type: Meter type of the meter to retrieve
    :param tags: The tags associated with the meter you want to retrieve
    :return: Meter in the global registry
    """

    if tags is None:
        tags = {}

    serialized_tags = [f"{key}-{value}" for key, value in tags.items()]

    combined_name = f"{name}{'_'.join(serialized_tags)}"

    return METERS[meter_type].get(combined_name)


def remove_meter(name, meter_type: MeterType) -> None:
    """
    Remove a meter from the global registry

    :param name: Name of the meter to remove
    :param meter_type: Meter type of the meter to remove
    """

    if name in METERS[meter_type]:
        del METERS[meter_type][name]


def add_counter(counter: Counter) -> None:
    """
    Add a counter to the global registry

    :param counter: Counter to add

    :raises AttributeError: When the name provided for the counter metric is already in use in the global registry
    """

    add_meter(counter)


def get_counter(name: str, tags: Optional[Mapping[str, Union[str, int, float]]] = None) -> Optional[Counter]:
    """
    Get a counter from the global registry by its name

    :param name: Name of the counter
    :param tags: The tags associated with the counter you want to retrieve
    :return: Counter in the global registry
    """

    return get_meter(name, MeterType.COUNTER, tags)  # type: ignore


def remove_counter(name: str) -> None:
    """
    Remove a counter from the global registry

    :param name: Name of the counter to remove
    """

    remove_meter(name, MeterType.COUNTER)


def add_gauge(gauge: Gauge) -> None:
    """
    Add a gauge to the global registry

    :param gauge: Gauge to add

    :raises AttributeError: When the name provided for the gauge metric is already in use in the global registry
    """

    add_meter(gauge)


def get_gauge(name: str, tags: Optional[Mapping[str, Union[str, int, float]]] = None) -> Optional[Gauge]:
    """
    Get a gauge from the global registry by its name

    :param name: Name of the gauge
    :param tags: The tags associated with the gauge you want to retrieve
    :return: Gauge in the global registry
    """

    return get_meter(name, MeterType.GAUGE, tags)  # type: ignore


def remove_gauge(name: str) -> None:
    """
    Remove a gauge from the global registry

    :param name: Name of the gauge to remove
    """

    remove_meter(name, MeterType.GAUGE)


def add_timer(timer: Timer) -> None:
    """
    Add a timer to the global registry

    :param timer: Timer to add

    :raises AttributeError: When the name provided for the timer metric is already in use in the global registry
    """

    add_meter(timer)


def get_timer(name: str, tags: Optional[Mapping[str, Union[str, int, float]]] = None) -> Optional[Timer]:
    """
    Get a timer from the global registry by its name

    :param name: Name of the timer
    :param tags: The tags associated with the timer you want to retrieve
    :return: Timer in the global registry
    """

    return get_meter(name, MeterType.TIMER, tags)  # type: ignore


def remove_timer(name: str) -> None:
    """
    Remove a timer from the global registry

    :param name: Name of the timer to remove
    """

    remove_meter(name, MeterType.TIMER)
