import pytest

from pylemetry import Registry


@pytest.fixture(autouse=True)
def clear_registry() -> None:
    Registry().clear()
