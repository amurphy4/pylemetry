import pytest

from pylemetry import Registry
from pylemetry.meters import Counter


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


def test_clear_registry() -> None:
    counter = Counter()
    counter_name = "test_counter"

    Registry().add_counter(counter_name, counter)

    assert counter_name in Registry().counters

    Registry().clear()

    assert len(Registry().counters) == 0
    assert counter_name not in Registry().counters
