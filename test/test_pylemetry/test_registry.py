import pytest

from pylemetry import registry
from pylemetry.meters import Counter, Gauge, Timer


def test_add_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    registry.add_counter(counter_name, counter)

    assert len(registry.COUNTERS) == 1
    assert counter_name in registry.COUNTERS
    assert registry.COUNTERS[counter_name] == counter


def test_add_counter_already_exists() -> None:
    counter = Counter()
    counter_name = "test_counter"

    registry.add_counter(counter_name, counter)

    with pytest.raises(AttributeError) as exec_info:
        new_counter = Counter()

        registry.add_counter(counter_name, new_counter)

    assert exec_info.value.args[0] == f"A counter with the name '{counter_name}' already exists"


def test_get_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    registry.add_counter(counter_name, counter)

    new_counter = registry.get_counter(counter_name)

    assert new_counter == counter


def test_remove_counter() -> None:
    counter = Counter()
    counter_name = "test_counter"

    registry.add_counter(counter_name, counter)

    assert counter_name in registry.COUNTERS

    registry.remove_counter(counter_name)

    assert len(registry.COUNTERS) == 0
    assert counter_name not in registry.COUNTERS


def test_add_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    registry.add_gauge(gauge_name, gauge)

    assert len(registry.GAUGES) == 1
    assert gauge_name in registry.GAUGES
    assert registry.GAUGES[gauge_name] == gauge


def test_add_gauge_already_exists() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    registry.add_gauge(gauge_name, gauge)

    with pytest.raises(AttributeError) as exec_info:
        new_gauge = Gauge()

        registry.add_gauge(gauge_name, new_gauge)

    assert exec_info.value.args[0] == f"A gauge with the name '{gauge_name}' already exists"


def test_get_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    registry.add_gauge(gauge_name, gauge)

    new_gauge = registry.get_gauge(gauge_name)

    assert new_gauge == gauge


def test_remove_gauge() -> None:
    gauge = Gauge()
    gauge_name = "test_gauge"

    registry.add_gauge(gauge_name, gauge)

    assert gauge_name in registry.GAUGES

    registry.remove_gauge(gauge_name)

    assert len(registry.GAUGES) == 0
    assert gauge_name not in registry.GAUGES


def test_add_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    registry.add_timer(timer_name, timer)

    assert len(registry.TIMERS) == 1
    assert timer_name in registry.TIMERS
    assert registry.TIMERS[timer_name] == timer


def test_add_timer_already_exists() -> None:
    timer = Timer()
    timer_name = "test_timer"

    registry.add_timer(timer_name, timer)

    with pytest.raises(AttributeError) as exec_info:
        new_timer = Timer()

        registry.add_timer(timer_name, new_timer)

    assert exec_info.value.args[0] == f"A timer with the name '{timer_name}' already exists"


def test_get_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    registry.add_timer(timer_name, timer)

    new_timer = registry.get_timer(timer_name)

    assert new_timer == timer


def test_remove_timer() -> None:
    timer = Timer()
    timer_name = "test_timer"

    registry.add_timer(timer_name, timer)

    assert timer_name in registry.TIMERS

    registry.remove_timer(timer_name)

    assert len(registry.TIMERS) == 0
    assert timer_name not in registry.TIMERS


def test_clear_registry() -> None:
    counter = Counter()
    counter_name = "test_counter"

    gauge = Gauge()
    gauge_name = "test_gauge"

    timer = Timer()
    timer_name = "test_timer"

    registry.add_counter(counter_name, counter)
    registry.add_gauge(gauge_name, gauge)
    registry.add_timer(timer_name, timer)

    assert counter_name in registry.COUNTERS
    assert gauge_name in registry.GAUGES
    assert timer_name in registry.TIMERS

    registry.clear()

    assert len(registry.COUNTERS) == 0
    assert len(registry.GAUGES) == 0
    assert len(registry.TIMERS) == 0

    assert counter_name not in registry.COUNTERS
    assert gauge_name not in registry.GAUGES
    assert timer_name not in registry.TIMERS
