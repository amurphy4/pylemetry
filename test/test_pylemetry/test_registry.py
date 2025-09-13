import pytest

from pylemetry import Registry
from pylemetry.meters import Counter, Gauge, Timer


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


def test_add_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    Registry().add_timer(timer_name, timer)

    assert len(Registry().timers) == 1
    assert timer_name in Registry().timers
    assert Registry().timers[timer_name] == timer


def test_add_timer_already_exists() -> None:
    timer = Timer()
    timer_name = "test_timer"

    Registry().add_timer(timer_name, timer)

    with pytest.raises(AttributeError) as exec_info:
        new_timer = Timer()

        Registry().add_timer(timer_name, new_timer)

    assert exec_info.value.args[0] == f"A timer with the name '{timer_name}' already exists"


def test_get_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    Registry().add_timer(timer_name, timer)

    new_timer = Registry().get_timer(timer_name)

    assert new_timer == timer


def test_remove_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    Registry().add_timer(timer_name, timer)

    assert timer_name in Registry().timers

    Registry().remove_timer(timer_name)

    assert len(Registry().timers) == 0
    assert timer_name not in Registry().timers


def test_clear_registry() -> None:
    counter = Counter()
    counter_name = "test_counter"

    gauge = Gauge()
    gauge_name = "test_gauge"

    timer = Timer()
    timer_name = "test_timer"

    Registry().add_counter(counter_name, counter)
    Registry().add_gauge(gauge_name, gauge)
    Registry().add_timer(timer_name, timer)

    assert counter_name in Registry().counters
    assert gauge_name in Registry().gauges
    assert timer_name in Registry().timers

    Registry().clear()

    assert len(Registry().counters) == 0
    assert len(Registry().gauges) == 0
    assert len(Registry().timers) == 0

    assert counter_name not in Registry().counters
    assert gauge_name not in Registry().gauges
    assert timer_name not in Registry().timers
