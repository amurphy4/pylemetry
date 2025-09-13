import pytest

from pylemetry.meters import Counter


def test_counter_starts_at_0() -> None:
    counter = Counter()

    assert counter.get_count() == 0


def test_counter_add_default() -> None:
    counter = Counter()
    counter.add()

    assert counter.get_count() == 1


@pytest.mark.parametrize("value", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_counter_add(value: int) -> None:
    counter = Counter()
    counter.add(value)

    assert counter.get_count() == value


@pytest.mark.parametrize("value", [1, 2, 3, 10, 20, 30, 100, 200, 300])
def test_counter_dunder_add(value: int) -> None:
    counter = Counter()
    counter += value

    assert counter.get_count() == value
