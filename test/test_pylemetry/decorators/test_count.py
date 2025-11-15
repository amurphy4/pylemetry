from typing import Union

import pytest

from pylemetry import registry
from pylemetry.decorators import count
from pylemetry.meters import Counter, MeterType


@count()
def mock_function(message: str) -> str:
    return f"A function decorated with the count decorator with message {message}"


def test_count_decorator_creates_counter_in_registry() -> None:
    counter_name = "mock_function"

    assert registry.get_counter(counter_name) is None

    mock_function("Hello World!")

    counter = registry.get_counter(counter_name)

    assert isinstance(counter, Counter)
    assert counter.get_value() == 1


@pytest.mark.parametrize("call_count", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_count_decorator_updates_existing_counter(call_count: int) -> None:
    counter_name = "mock_function"

    assert registry.get_counter(counter_name) is None

    for _ in range(call_count):
        mock_function("Hello World!")

    counter = registry.get_counter(counter_name)

    assert isinstance(counter, Counter)
    assert counter.get_value() == call_count


def test_count_decorator_with_name() -> None:
    @count(name="test_count_meter")
    def mock() -> None:
        print("Mock method")

    mock()

    assert "test_count_meter" in registry.METERS[MeterType.COUNTER]


def test_count_decorator_with_tags() -> None:
    @count(tags={"tag_1": "args[0]", "tag_2": "kwargs[value_2]", "tag_3": "another_value"})
    def mock(value: str, value_2: int) -> None:
        print(f"Mocked with '{value}' and '{value_2}'")

    mock("value 1", value_2=2)

    counter = next(iter(registry.METERS[MeterType.COUNTER].values()))

    tags = counter.get_tags()

    assert "tag_1" in tags
    assert tags["tag_1"] == "value 1"
    assert "tag_2" in tags
    assert tags["tag_2"] == 2
    assert "tag_3" in tags
    assert tags["tag_3"] == "another_value"


def test_count_decorator_with_tags_raises_error_args_index() -> None:
    @count(tags={"tag_1": "args[0]"})
    def mock() -> None:
        pass

    with pytest.raises(IndexError) as exec_info:
        mock()

    assert exec_info.value.args[0] == "args index 0 out of range, args has length 0"


def test_count_decorator_with_tags_raises_error_args_invalid_type() -> None:
    @count(tags={"tag_1": "args[0]"})
    def mock(value: dict[str, str]) -> None:
        pass

    with pytest.raises(ValueError) as exec_info:
        mock({"key": "value"})

    assert exec_info.value.args[0] == "Only args of types (str | int | float) may be added as tags. Got <class 'dict'>"


def test_count_decorator_with_tags_raises_error_kwargs_non_existent() -> None:
    @count(tags={"tag_1": "kwargs[test_kwargs]"})
    def mock() -> None:
        pass

    with pytest.raises(KeyError) as exec_info:
        mock()

    assert exec_info.value.args[0] == "Key 'test_kwargs' not present in kwargs"


def test_count_decorator_with_tags_raises_error_kwargs_invalid_type() -> None:
    @count(tags={"tag_1": "kwargs[value]"})
    def mock(value: dict[str, str]) -> None:
        pass

    with pytest.raises(ValueError) as exec_info:
        mock(value={"key": "value"})

    assert (
        exec_info.value.args[0] == "Only kwargs of types (str | int | float) may be added as tags. Got <class 'dict'>"
    )


@pytest.mark.parametrize("call_count", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_count_decorator_updates_existing_counter_with_tags(call_count: int) -> None:
    counter_name = "mock_function"

    @count(name=counter_name, tags={"tag_1": "args[0]", "tag_2": "kwargs[value_2]", "tag_3": "another_value"})
    def mock(value: str, value_2: int) -> None:
        print(f"Mocked with '{value}' and '{value_2}'")

    tags: dict[str, Union[str, int]] = {"tag_1": "Hello World!", "tag_2": 2, "tag_3": "another_value"}

    assert registry.get_counter(counter_name, tags=tags) is None

    for _ in range(call_count):
        mock("Hello World!", value_2=2)

    counter = registry.get_counter(counter_name, tags=tags)

    assert isinstance(counter, Counter)
    assert counter.get_value() == call_count
