import csv
import json
from enum import StrEnum
from pathlib import Path
from typing import TextIO

from pylemetry import registry
from pylemetry.meters import Meter
from pylemetry.reporting.reporter import Reporter
from pylemetry.reporting.reporting_type import ReportingType
from pylemetry.utils.types import Tags


class FileType(StrEnum):
    JSON = "json"
    CSV = "csv"
    TEXT = "txt"


class FileReporter(Reporter):
    def __init__(
        self,
        interval: float,
        file_path: str | Path,
        reporting_type: ReportingType,
        file_type: FileType = FileType.JSON,
        clear_registry_on_exit: bool = False,
        universal_tags: Tags | None = None,
        verbose_tags: bool = False,
    ):
        super().__init__(interval, reporting_type, clear_registry_on_exit, universal_tags, verbose_tags)

        self.file_path = file_path
        self.reporting_type = reporting_type
        self.file_type = file_type

    def flush(self) -> None:
        with open(self.file_path, "a", encoding="utf-8") as file:
            for _, meters in registry.METERS.items():
                for _, meter in meters.items():
                    match self.file_type:
                        case FileType.JSON:
                            self._flush_json(file, meter)
                        case FileType.CSV:
                            self._flush_csv(file, meter)
                        case FileType.TEXT:
                            self._flush_text(file, meter)

                    if self.since_last_interval:
                        meter.mark_interval()

    def _flush_json(self, file: TextIO, meter: Meter) -> None:
        data = meter.to_dict()
        data["tags"] = self._format_tags(meter.get_tags(), verbose=self.verbose_tags)

        file.write(json.dumps(data) + "\n")

    def _flush_csv(self, file: TextIO, meter: Meter) -> None:
        data = meter.to_dict()
        data["tags"] = json.dumps(self._format_tags(meter.get_tags()))

        csv.writer(file).writerow(data.values())

    def _flush_text(self, file: TextIO, meter: Meter) -> None:
        file.write(self.format_message(self.message_formats[meter.meter_type], meter, self.since_last_interval) + "\n")
