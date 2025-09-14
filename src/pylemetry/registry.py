from threading import Lock

from pylemetry.meters import Counter, Gauge, Timer


class SingletonMeta(type):
    _instances: dict[type, object] = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance

        return cls._instances[cls]


class Registry(metaclass=SingletonMeta):
    def __init__(self):
        self.counters = {}
        self.gauges = {}
        self.timers = {}

    def clear(self) -> None:
        """
        Remove all meters from the global registry
        """

        self.counters = {}
        self.gauges = {}
        self.timers = {}

    def add_counter(self, name: str, counter: Counter) -> None:
        """
        Add a counter to the global registry

        :param name: Unique name of the counter
        :param counter: Counter to add

        :raises AttributeError: When the name provided for the counter metric is already in use in the global registry
        """

        if name in self.counters:
            raise AttributeError(f"A counter with the name '{name}' already exists")

        self.counters[name] = counter

    def get_counter(self, name: str) -> Counter:
        """
        Get a counter from the global registry by its name

        :param name: Name of the counter
        :return: Counter in the global registry
        """

        return self.counters.get(name)

    def remove_counter(self, name: str) -> None:
        """
        Remove a counter from the global registry

        :param name: Name of the counter to remove
        """

        if name in self.counters:
            del self.counters[name]

    def add_gauge(self, name: str, gauge: Gauge) -> None:
        """
        Add a gauge to the global registry

        :param name: Unique name of the gauge
        :param gauge: Gauge to add

        :raises AttributeError: When the name provided for the gauge metric is already in use in the global registry
        """

        if name in self.gauges:
            raise AttributeError(f"A gauge with the name '{name}' already exists")

        self.gauges[name] = gauge

    def get_gauge(self, name: str) -> Gauge:
        """
        Get a gauge from the global registry by its name

        :param name: Name of the gauge
        :return: Gauge in the global registry
        """

        return self.gauges.get(name)

    def remove_gauge(self, name: str) -> None:
        """
        Remove a gauge from the global registry

        :param name: Name of the gauge to remove
        """

        if name in self.gauges:
            del self.gauges[name]

    def add_timer(self, name: str, timer: Timer) -> None:
        """
        Add a timer to the global registry

        :param name: Unique name of the timer
        :param timer: Timer to add

        :raises AttributeError: When the name provided for the timer metric is already in use in the global registry
        """

        if name in self.timers:
            raise AttributeError(f"A timer with the name '{name}' already exists")

        self.timers[name] = timer

    def get_timer(self, name: str) -> Timer:
        """
        Get a timer from the global registry by its name

        :param name: Name of the timer
        :return: Timer in the global registry
        """

        return self.timers.get(name)

    def remove_timer(self, name: str) -> None:
        """
        Remove a timer from the global registry

        :param name: Name of the timer to remove
        """

        if name in self.timers:
            del self.timers[name]
