import pytest

from pylemetry.utils import TimerUnits


@pytest.mark.parametrize(
    "unit, expected_value",
    [
        (TimerUnits.HOURS, 1),
        (TimerUnits.MINUTES, 60),
        (TimerUnits.SECONDS, 3600),
        (TimerUnits.MILLISECONDS, 3_600_000),
        (TimerUnits.MICROSECONDS, 3_600_000_000),
        (TimerUnits.NANOSECONDS, 3_600_000_000_000),
    ],
)
def test_time_unit_conversion(unit: TimerUnits, expected_value: float) -> None:
    value = 3_600_000_000_000 / unit.conversion_from_ns()

    assert value == expected_value
