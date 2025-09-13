from threading import Lock

from pylemetry.meters import Counter


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

    def clear(self) -> None:
        self.counters = {}

    def add_counter(self, name: str, counter: Counter) -> None:
        if name in self.counters:
            raise AttributeError(f"A counter with the name '{name}' already exists")

        self.counters[name] = counter

    def get_counter(self, name: str) -> Counter:
        return self.counters.get(name)

    def remove_counter(self, name: str) -> None:
        if name in self.counters:
            del self.counters[name]
