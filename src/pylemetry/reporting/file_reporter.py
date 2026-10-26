import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO

from pylemetry import registry
from pylemetry.meters import Meter
from pylemetry.reporting.reporter import Reporter
from pylemetry.reporting.reporting_type import ReportingType
from pylemetry.utils.types import Tags


class FileReporter(Reporter, ABC):
    def __init__(
        self,
        interval: float,
        file_path: str | Path,
        reporting_type: ReportingType,
        clear_registry_on_exit: bool = False,
        universal_tags: Tags | None = None,
        verbose_tags: bool = False,
    ):
        super().__init__(interval, reporting_type, clear_registry_on_exit, universal_tags, verbose_tags)

        self.file_path = file_path
        self.reporting_type = reporting_type

    def flush(self) -> None:
        with open(self.file_path, "a", encoding="utf-8") as file:
            for _, meters in registry.METERS.items():
                for _, meter in meters.items():
                    self.flush_to_file(file, meter)

                    if self.since_last_interval:
                        meter.mark_interval()

    @abstractmethod
    def flush_to_file(self, file: TextIO, meter: Meter) -> None: ...


class JSONFileReporter(FileReporter):
    def flush_to_file(self, file: TextIO, meter: Meter) -> None:
        data = meter.to_dict()
        data["tags"] = self._format_tags(meter.get_tags(), verbose=self.verbose_tags)

        file.write(json.dumps(data) + "\n")


class CSVFileReporter(FileReporter):
    def flush_to_file(self, file: TextIO, meter: Meter) -> None:
        data = meter.to_dict()
        data["tags"] = self._format_tags(meter.get_tags())

        csv.writer(file).writerow(data.values())


class TextFileReporter(FileReporter):
    def flush_to_file(self, file: TextIO, meter: Meter) -> None:
        file.write(self.format_message(self.message_formats[meter.meter_type], meter, self.since_last_interval) + "\n")
