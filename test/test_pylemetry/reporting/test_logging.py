import logging
import time

from pylemetry import registry
from pylemetry.meters import Counter
from pylemetry.reporting import LoggingReporter, ReportingType


def test_logging_reporter_logs_messages(caplog) -> None:
    logger = logging.getLogger(__name__)

    counter = Counter()
    counter += 1

    registry.add_counter("test_counter", counter)

    with caplog.at_level(logging.INFO):
        reporter = LoggingReporter(10, "Hello World!", logger, logging.INFO, ReportingType.CUMULATIVE)
        reporter.flush()

    assert "Hello World!" in caplog.text


def test_logging_reporter_marks_meter_intervals() -> None:
    logger = logging.getLogger(__name__)

    counter = Counter()
    counter += 1

    registry.add_counter("test_counter", counter)

    registry_counter = registry.get_counter("test_counter")

    assert registry_counter is not None
    assert registry_counter.get_value() == 1
    assert registry_counter.get_value(since_last_interval=True) == 1

    reporter = LoggingReporter(0.1, "", logger, logging.INFO, ReportingType.INTERVAL)
    reporter.start()

    time.sleep(0.5)

    registry_counter = registry.get_counter("test_counter")

    assert registry_counter is not None
    assert registry_counter.get_value() == 1
    assert registry_counter.get_value(since_last_interval=True) == 0

    registry_counter.add(1)

    assert registry_counter.get_value() == 2
    assert registry_counter.get_value(since_last_interval=True) == 1

    reporter.stop()

    registry_counter = registry.get_counter("test_counter")

    assert registry_counter is not None
    assert registry_counter.get_value() == 2
    assert registry_counter.get_value(since_last_interval=True) == 0
