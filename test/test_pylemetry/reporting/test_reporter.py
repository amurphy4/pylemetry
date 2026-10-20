import logging
import time
from collections.abc import Generator
from pathlib import Path

import pytest
from pytest import LogCaptureFixture

from pylemetry import registry
from pylemetry.meters import Counter, Gauge, Timer
from pylemetry.reporting import (
    CSVFileReporter,
    FileReporter,
    JSONFileReporter,
    LoggingReporter,
    Reporter,
    ReportingType,
    TextFileReporter,
)


@pytest.fixture(scope="function")
def temp_file() -> Generator[Path, None, None]:
    file = Path(__file__).parent / "temp_file"

    yield file

    file.unlink(missing_ok=True)


def test_reporter_base_class_cant_flush() -> None:
    with pytest.raises(TypeError) as exec_info:
        Reporter(1)  # type: ignore[abstract]

    assert exec_info.value.args[0].startswith("Can't instantiate abstract class Reporter")


def test_logging_reporter_flushing_on_timer(caplog: LogCaptureFixture) -> None:
    logger = logging.getLogger(__name__)

    counter = Counter("test_counter")
    counter += 1

    registry.add_counter(counter)

    with caplog.at_level(logging.INFO):
        reporter = LoggingReporter(0.1, logger, logging.INFO, ReportingType.CUMULATIVE)
        reporter.start()

        time.sleep(0.5)

        reporter.stop()

        assert len(caplog.records) == 5


@pytest.mark.parametrize("file_reporter", [CSVFileReporter, JSONFileReporter, TextFileReporter])
def test_file_reporter_flushing_on_timer(temp_file: Path, file_reporter: type[FileReporter]) -> None:
    counter = Counter("test_counter")
    counter += 1

    registry.add_counter(counter)

    reporter = file_reporter(0.1, temp_file, ReportingType.CUMULATIVE)
    reporter.start()

    time.sleep(0.5)

    reporter.stop()

    with open(temp_file) as file:
        assert len(file.readlines()) == 5


def test_reporter_context_manager(caplog: LogCaptureFixture) -> None:
    logger = logging.getLogger(__name__)

    counter = Counter("test_counter")
    counter += 1

    registry.add_counter(counter)

    with caplog.at_level(logging.INFO):
        with LoggingReporter(0.1, logger, logging.INFO, ReportingType.CUMULATIVE) as reporter:
            reporter.configure_message_format("{name} - {count}")

            time.sleep(0.5)

        assert len(caplog.records) == 5
        assert caplog.records[0].msg == "test_counter - 1.0"


def test_reporter_context_manager_clear_registry_on_exit() -> None:
    logger = logging.getLogger(__name__)

    counter = Counter("test_counter")
    counter += 1

    registry.add_counter(counter)

    with LoggingReporter(0.1, logger, logging.INFO, ReportingType.CUMULATIVE):
        counter += 1

    assert registry.get_counter("test_counter") == counter

    with LoggingReporter(0.1, logger, logging.INFO, ReportingType.CUMULATIVE, clear_registry_on_exit=True):
        counter += 1

    assert registry.get_counter("test_counter") is None


def test_message_format_counter() -> None:
    logger = logging.getLogger(__name__)

    message_format = (
        "{{'name': '{name}', 'type': '{type}', 'value': {value}, "
        "'min': {min}, 'max': {max}, 'average': {avg}, 'tags': {tags}}}"
    )

    counter = Counter("test_counter")
    counter += 10

    message = LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE).format_message(
        message_format, counter, False
    )

    assert (
        message == "{'name': 'test_counter', 'type': 'counter', 'value': 10.0, "
        "'min': 10.0, 'max': 10.0, 'average': 10.0, 'tags': {}}"
    )


def test_message_format_gauge() -> None:
    logger = logging.getLogger(__name__)

    message_format = (
        "{{'name': '{name}', 'type': '{type}', 'value': {value}, 'min': {min}, "
        "'max': {max}, 'average': {avg}, 'tags': {tags}}}"
    )

    gauge = Gauge("test_gauge")
    gauge += 10

    message = LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE).format_message(
        message_format, gauge, False
    )

    assert (
        message == "{'name': 'test_gauge', 'type': 'gauge', 'value': 10.0, "
        "'min': 10.0, 'max': 10.0, 'average': 10.0, 'tags': {}}"
    )


def test_message_format_timer() -> None:
    logger = logging.getLogger(__name__)

    message_format = (
        "{{'name': '{name}', 'type': '{type}', 'value': {value}, 'count': {count}, 'min': {min}, "
        "'max': {max}, 'average': {avg}, 'tags': {tags}}}"
    )

    timer = Timer("test_timer")
    timer.ticks = [1, 2, 3, 4, 5]

    message = LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE).format_message(
        message_format, timer, False
    )

    assert (
        message == "{'name': 'test_timer', 'type': 'timer', 'value': 15, "
        "'count': 5, 'min': 1, 'max': 5, 'average': 3.0, 'tags': {}}"
    )


def test_message_format_with_tags() -> None:
    logger = logging.getLogger(__name__)

    message_format = "{{'name': '{name}', 'tags': {tags}}}"

    timer = Timer("test_timer", tags={"tag_1": "value", "tag_2": 2, "tag_3": 1.5})

    message = LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE).format_message(
        message_format, timer, False
    )

    assert message == "{'name': 'test_timer', 'tags': {'tag_1': 'value', 'tag_2': 2, 'tag_3': 1.5}}"


def test_message_format_with_universal_tags() -> None:
    logger = logging.getLogger(__name__)

    message_format = "{{'name': '{name}', 'tags': {tags}}}"

    timer = Timer("test_timer", tags={"tag_2": 2, "tag_3": 1.5})

    message = LoggingReporter(
        1.0, logger, logging.INFO, ReportingType.CUMULATIVE, universal_tags={"tag_1": "value"}
    ).format_message(message_format, timer, False)

    assert message == "{'name': 'test_timer', 'tags': {'tag_1': 'value', 'tag_2': 2, 'tag_3': 1.5}}"


def test_message_format_with_verbose_tags() -> None:
    logger = logging.getLogger(__name__)

    message_format = "{{'name': '{name}', 'tags': {tags}}}"

    timer = Timer("test_timer", tags={"tag_1": "value", "tag_2": 2, "tag_3": 1.5})

    message = LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE, verbose_tags=True).format_message(
        message_format, timer, False
    )

    assert (
        message
        == "{'name': 'test_timer', 'tags': [{'name': 'tag_1', 'value': 'value'}, {'name': 'tag_2', 'value': 2}, "
        "{'name': 'tag_3', 'value': 1.5}]}"
    )


def test_message_format_with_verbose_universal_tags() -> None:
    logger = logging.getLogger(__name__)

    message_format = "{{'name': '{name}', 'tags': {tags}}}"

    timer = Timer("test_timer", tags={"tag_2": 2, "tag_3": 1.5})

    message = LoggingReporter(
        1.0, logger, logging.INFO, ReportingType.CUMULATIVE, universal_tags={"tag_1": "value"}, verbose_tags=True
    ).format_message(message_format, timer, False)

    assert (
        message
        == "{'name': 'test_timer', 'tags': [{'name': 'tag_1', 'value': 'value'}, {'name': 'tag_2', 'value': 2}, "
        "{'name': 'tag_3', 'value': 1.5}]}"
    )


def test_message_format_unsupported_meter() -> None:
    logger = logging.getLogger(__name__)

    with pytest.raises(ValueError) as exec_info:
        LoggingReporter(1.0, logger, logging.INFO, ReportingType.CUMULATIVE).format_message(
            "Hello World!",
            "fake meter",  # type: ignore[arg-type]
            False,
        )

    assert exec_info.value.args[0] == "Unsupported meter of type <class 'str'>"
