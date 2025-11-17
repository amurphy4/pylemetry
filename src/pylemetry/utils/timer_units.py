from enum import Enum


class TimerUnits(Enum):
    HOURS = "hours"
    MINUTES = "minutes"
    SECONDS = "seconds"
    MILLISECONDS = "milliseconds"
    MICROSECONDS = "microseconds"
    NANOSECONDS = "nanoseconds"

    def conversion_from_ns(self) -> int:
        conversions = {
            self.HOURS: 10**9 * 60 * 60,
            self.MINUTES: 10**9 * 60,
            self.SECONDS: 10**9,
            self.MILLISECONDS: 10**6,
            self.MICROSECONDS: 10**3,
            self.NANOSECONDS: 1,
        }

        return conversions[self]
