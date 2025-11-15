import pytest

from pylemetry import registry
from pylemetry.meters import Counter, Gauge, Timer, MeterType


def test_add_counter() -> None:
    counter_name = "test_counter"
    counter = Counter(counter_name)

    registry.add_counter(counter)

    assert len(registry.METERS[MeterType.COUNTER]) == 1
    assert counter_name in registry.METERS[MeterType.COUNTER]
    assert registry.METERS[MeterType.COUNTER][counter_name] == counter


def test_add_counter_already_exists() -> None:
    counter_name = "test_counter"
    counter = Counter(counter_name)

    registry.add_counter(counter)

    with pytest.raises(AttributeError) as exec_info:
        new_counter = Counter(counter_name)

        registry.add_counter(new_counter)

    assert exec_info.value.args[0] == f"A counter with the name '{counter_name}' and the same tags already exists"


def test_get_counter() -> None:
    counter_name = "test_counter"
    counter = Counter(counter_name)

    registry.add_counter(counter)

    new_counter = registry.get_counter(counter_name)

    assert new_counter == counter


def test_remove_counter() -> None:
    counter_name = "test_counter"
    counter = Counter(counter_name)

    registry.add_counter(counter)

    assert counter_name in registry.METERS[MeterType.COUNTER]

    registry.remove_counter(counter_name)

    assert len(registry.METERS[MeterType.COUNTER]) == 0
    assert counter_name not in registry.METERS[MeterType.COUNTER]


def test_add_gauge() -> None:
    gauge_name = "test_gauge"
    gauge = Gauge(gauge_name)

    registry.add_gauge(gauge)

    assert len(registry.METERS[MeterType.GAUGE]) == 1
    assert gauge_name in registry.METERS[MeterType.GAUGE]
    assert registry.METERS[MeterType.GAUGE][gauge_name] == gauge


def test_add_gauge_already_exists() -> None:
    gauge_name = "test_gauge"
    gauge = Gauge(gauge_name)

    registry.add_gauge(gauge)

    with pytest.raises(AttributeError) as exec_info:
        new_gauge = Gauge(gauge_name)

        registry.add_gauge(new_gauge)

    assert exec_info.value.args[0] == f"A gauge with the name '{gauge_name}' and the same tags already exists"


def test_get_gauge() -> None:
    gauge_name = "test_gauge"
    gauge = Gauge(gauge_name)

    registry.add_gauge(gauge)

    new_gauge = registry.get_gauge(gauge_name)

    assert new_gauge == gauge


def test_remove_gauge() -> None:
    gauge_name = "test_gauge"
    gauge = Gauge(gauge_name)

    registry.add_gauge(gauge)

    assert gauge_name in registry.METERS[MeterType.GAUGE]

    registry.remove_gauge(gauge_name)

    assert len(registry.METERS[MeterType.GAUGE]) == 0
    assert gauge_name not in registry.METERS[MeterType.GAUGE]


def test_add_timer() -> None:
    timer_name = "test_timer"
    timer = Timer(timer_name)

    registry.add_timer(timer)

    assert len(registry.METERS[MeterType.TIMER]) == 1
    assert timer_name in registry.METERS[MeterType.TIMER]
    assert registry.METERS[MeterType.TIMER][timer_name] == timer


def test_add_timer_already_exists() -> None:
    timer_name = "test_timer"
    timer = Timer(timer_name)

    registry.add_timer(timer)

    with pytest.raises(AttributeError) as exec_info:
        new_timer = Timer(timer_name)

        registry.add_timer(new_timer)

    assert exec_info.value.args[0] == f"A timer with the name '{timer_name}' and the same tags already exists"


def test_get_timer() -> None:
    timer_name = "test_timer"
    timer = Timer(timer_name)

    registry.add_timer(timer)

    new_timer = registry.get_timer(timer_name)

    assert new_timer == timer


def test_remove_timer() -> None:
    timer_name = "test_timer"
    timer = Timer(timer_name)

    registry.add_timer(timer)

    assert timer_name in registry.METERS[MeterType.TIMER]

    registry.remove_timer(timer_name)

    assert len(registry.METERS[MeterType.TIMER]) == 0
    assert timer_name not in registry.METERS[MeterType.TIMER]


def test_clear_registry() -> None:
    counter_name = "test_counter"
    counter = Counter(counter_name)

    gauge_name = "test_gauge"
    gauge = Gauge(gauge_name)

    timer_name = "test_timer"
    timer = Timer(timer_name)

    registry.add_counter(counter)
    registry.add_gauge(gauge)
    registry.add_timer(timer)

    assert counter_name in registry.METERS[MeterType.COUNTER]
    assert gauge_name in registry.METERS[MeterType.GAUGE]
    assert timer_name in registry.METERS[MeterType.TIMER]

    registry.clear()

    assert len(registry.METERS[MeterType.COUNTER]) == 0
    assert len(registry.METERS[MeterType.GAUGE]) == 0
    assert len(registry.METERS[MeterType.TIMER]) == 0

    assert counter_name not in registry.METERS[MeterType.COUNTER]
    assert gauge_name not in registry.METERS[MeterType.GAUGE]
    assert timer_name not in registry.METERS[MeterType.TIMER]
