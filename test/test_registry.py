import pytest

from pylemetry import Registry
from pylemetry.meters import Counter, Gauge


def test_registry_singleton() -> None:
    registry = Registry()
    second_registry = Registry()

    assert registry == second_registry


def test_add_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    assert len(Registry().counters) == 1
    assert counter_name in Registry().counters
    assert Registry().counters[counter_name] == counter


def test_add_counter_already_exists() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    with pytest.raises(AttributeError) as exec_info:
        new_counter = Counter()

        Registry().add_counter(counter_name, new_counter)

    assert exec_info.value.args[0] == f"A counter with the name '{counter_name}' already exists"


def test_get_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    new_counter = Registry().get_counter(counter_name)

    assert new_counter == counter


def test_remove_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    assert counter_name in Registry().counters

    Registry().remove_counter(counter_name)

    assert len(Registry().counters) == 0
    assert counter_name not in Registry().counters


def test_add_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    Registry().add_gauge(gauge_name, gauge)

    assert len(Registry().gauges) == 1
    assert gauge_name in Registry().gauges
    assert Registry().gauges[gauge_name] == gauge


def test_add_gauge_already_exists() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    Registry().add_gauge(gauge_name, gauge)

    with pytest.raises(AttributeError) as exec_info:
        new_gauge = Gauge()

        Registry().add_gauge(gauge_name, new_gauge)

    assert exec_info.value.args[0] == f"A gauge with the name '{gauge_name}' already exists"


def test_get_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    Registry().add_gauge(gauge_name, gauge)

    new_gauge = Registry().get_gauge(gauge_name)

    assert new_gauge == gauge


def test_remove_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    Registry().add_gauge(gauge_name, gauge)

    assert gauge_name in Registry().gauges

    Registry().remove_gauge(gauge_name)

    assert len(Registry().gauges) == 0
    assert gauge_name not in Registry().gauges


def test_clear_registry() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    assert counter_name in Registry().counters

    Registry().clear()

    assert len(Registry().counters) == 0
    assert counter_name not in Registry().counters
