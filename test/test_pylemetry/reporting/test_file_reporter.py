import csv
import json
from collections.abc import Generator
from pathlib import Path

import pytest

from pylemetry import registry
from pylemetry.meters import Counter, Timer
from pylemetry.reporting import FileReporter, FileType, ReportingType


@pytest.fixture(scope="function")
def temp_file() -> Generator[Path, None, None]:
    file = Path(__file__).parent / "temp_file"

    yield file

    file.unlink(missing_ok=True)


def test_file_reporter_json_counter(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    registry.add_counter(counter)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        data = json.loads(file.read())

        assert data == {
            "name": "test_counter",
            "value": 1,
            "type": "counter",
            "tags": {"tag1": "value1", "tag2": "value2"},
        }


def test_file_reporter_json_timer(temp_file: Path) -> None:
    timer = Timer("test_timer", tags={"tag1": "value1", "tag2": "value2"})

    registry.add_timer(timer)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        data = json.loads(file.read())

        assert data == {
            "name": "test_timer",
            "count": 0,
            "type": "timer",
            "unit": "nanoseconds",
            "tags": {"tag1": "value1", "tag2": "value2"},
            "value": 0,
            "min": 0,
            "max": 0,
            "avg": 0,
        }


def test_file_reporter_csv_counter(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    registry.add_counter(counter)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE, file_type=FileType.CSV)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            assert row == ["test_counter", "counter", "1.0", "{'tag1': 'value1', 'tag2': 'value2'}"]


def test_file_reporter_csv_timer(temp_file: Path) -> None:
    timer = Timer("test_timer", tags={"tag1": "value1", "tag2": "value2"})

    registry.add_timer(timer)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE, file_type=FileType.CSV)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            assert row == [
                "test_timer",
                "timer",
                "nanoseconds",
                "0",
                "0",
                "0",
                "0",
                "0",
                "{'tag1': 'value1', 'tag2': 'value2'}",
            ]


def test_file_reporter_text(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    registry.add_counter(counter)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE, file_type=FileType.TEXT)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        assert file.read() == "test_counter [counter] -- 1.0\n"


def test_file_reporter_json_multiple_meters_output_to_file(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    counter_2 = Counter("test_counter_2", {"tag1": "value1", "tag2": "value2"})
    counter_2 += 10

    registry.add_counter(counter)
    registry.add_counter(counter_2)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        lines = file.readlines()

        counter_data = json.loads(lines[0])
        counter_2_data = json.loads(lines[1])

        assert counter_data == {
            "name": "test_counter",
            "value": 1,
            "type": "counter",
            "tags": {"tag1": "value1", "tag2": "value2"},
        }
        assert counter_2_data == {
            "name": "test_counter_2",
            "value": 10,
            "type": "counter",
            "tags": {"tag1": "value1", "tag2": "value2"},
        }


def test_file_reporter_csv_multiple_meters_output_to_file(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    counter_2 = Counter("test_counter_2", {"tag1": "value1", "tag2": "value2"})
    counter_2 += 10

    registry.add_counter(counter)
    registry.add_counter(counter_2)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE, file_type=FileType.CSV)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        reader = csv.reader(file)

        lines = list(reader)

        assert lines[0] == ["test_counter", "counter", "1.0", "{'tag1': 'value1', 'tag2': 'value2'}"]
        assert lines[1] == ["test_counter_2", "counter", "10.0", "{'tag1': 'value1', 'tag2': 'value2'}"]


def test_file_reporter_text_multiple_meters_output_to_file(temp_file: Path) -> None:
    counter = Counter("test_counter", {"tag1": "value1", "tag2": "value2"})
    counter += 1

    counter_2 = Counter("test_counter_2", {"tag1": "value1", "tag2": "value2"})
    counter_2 += 10

    registry.add_counter(counter)
    registry.add_counter(counter_2)

    reporter = FileReporter(10, temp_file, ReportingType.CUMULATIVE, file_type=FileType.TEXT)
    reporter.flush()

    with open(temp_file, encoding="utf-8") as file:
        lines = file.readlines()

        assert lines[0] == "test_counter [counter] -- 1.0\n"
        assert lines[1] == "test_counter_2 [counter] -- 10.0\n"
