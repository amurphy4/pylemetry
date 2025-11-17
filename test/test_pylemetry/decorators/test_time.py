from typing import Union

import pytest

from pylemetry import registry
from pylemetry.decorators import time
from pylemetry.meters import Timer, MeterType
from pylemetry.utils import TimerUnits


@time(unit=TimerUnits.SECONDS)
def mock_function(message: str) -> str:
    return f"A function decorated with the timer decorator with message {message}"


def test_time_decorator_creates_counter_in_registry() -> None:
    timer_name = "mock_function"

    assert registry.get_timer(timer_name) is None

    mock_function("Hello World!")

    timer = registry.get_timer(timer_name)

    assert isinstance(timer, Timer)
    assert timer.get_count() == 1
    assert 0 < timer.get_value() < 0.05
    assert 0 < timer.get_mean_tick_time() < 0.05


@pytest.mark.parametrize("call_count", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_time_decorator_updates_existing_counter(call_count: int) -> None:
    timer_name = "mock_function"

    assert registry.get_timer(timer_name) is None

    for _ in range(call_count):
        mock_function("Hello World!")

    timer = registry.get_timer(timer_name)

    assert isinstance(timer, Timer)
    assert timer.get_count() == call_count
    assert 0 < timer.get_mean_tick_time() < 0.05


def test_time_decorator_with_name() -> None:
    @time(name="test_timer_meter")
    def mock() -> None:
        print("Mock method")

    mock()

    assert "test_timer_meter" in registry.METERS[MeterType.TIMER]


def test_time_decorator_with_tags() -> None:
    @time(tags={"tag_1": "args[0]", "tag_2": "kwargs[value_2]", "tag_3": "another_value"})
    def mock(value: str, value_2: int) -> None:
        print(f"Mocked with '{value}' and '{value_2}'")

    mock("value 1", value_2=2)

    timer = next(iter(registry.METERS[MeterType.TIMER].values()))

    tags = timer.get_tags()

    assert "tag_1" in tags
    assert tags["tag_1"] == "value 1"
    assert "tag_2" in tags
    assert tags["tag_2"] == 2
    assert "tag_3" in tags
    assert tags["tag_3"] == "another_value"


def test_time_decorator_with_tags_raises_error_args_index() -> None:
    @time(tags={"tag_1": "args[0]"})
    def mock() -> None:
        pass

    with pytest.raises(IndexError) as exec_info:
        mock()

    assert exec_info.value.args[0] == "args index 0 out of range, args has length 0"


def test_time_decorator_with_tags_raises_error_args_invalid_type() -> None:
    @time(tags={"tag_1": "args[0]"})
    def mock(value: dict[str, str]) -> None:
        print(value)

    with pytest.raises(ValueError) as exec_info:
        mock({"key": "value"})

    assert exec_info.value.args[0] == "Only args of types (str | int | float) may be added as tags. Got <class 'dict'>"


def test_time_decorator_with_tags_raises_error_kwargs_non_existent() -> None:
    @time(tags={"tag_1": "kwargs[test_kwargs]"})
    def mock() -> None:
        pass

    with pytest.raises(KeyError) as exec_info:
        mock()

    assert exec_info.value.args[0] == "Key 'test_kwargs' not present in kwargs"


def test_time_decorator_with_tags_raises_error_kwargs_invalid_type() -> None:
    @time(tags={"tag_1": "kwargs[value]"})
    def mock(value: dict[str, str]) -> None:
        print(value)

    with pytest.raises(ValueError) as exec_info:
        mock(value={"key": "value"})

    assert (
        exec_info.value.args[0] == "Only kwargs of types (str | int | float) may be added as tags. Got <class 'dict'>"
    )


@pytest.mark.parametrize("call_count", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_time_decorator_updates_existing_timer_with_tags(call_count: int) -> None:
    timer_name = "mock_function"

    @time(
        name=timer_name,
        unit=TimerUnits.SECONDS,
        tags={"tag_1": "args[0]", "tag_2": "kwargs[value_2]", "tag_3": "another_value"},
    )
    def mock(value: str, value_2: int) -> None:
        print(f"Mocked with '{value}' and '{value_2}'")

    tags: dict[str, Union[str, int]] = {"tag_1": "Hello World!", "tag_2": 2, "tag_3": "another_value"}

    assert registry.get_timer(timer_name, tags=tags) is None

    for _ in range(call_count):
        mock("Hello World!", value_2=2)

    timer = registry.get_timer(timer_name, tags=tags)

    assert isinstance(timer, Timer)
    assert timer.get_count() == call_count
    assert 0 < timer.get_mean_tick_time() < 0.05
