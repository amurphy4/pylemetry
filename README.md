# Pylemetry

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/pylemetry.svg)](https://pypi.python.org/pypi/pylemetry)
[![image](https://img.shields.io/pypi/l/pylemetry.svg)](https://pypi.python.org/pypi/pylemetry)
[![image](https://img.shields.io/pypi/pyversions/pylemetry.svg)](https://pypi.python.org/pypi/pylemetry)
[![Release](https://github.com/amurphy4/pylemetry/actions/workflows/release.yaml/badge.svg?branch=main)](https://github.com/amurphy4/pylemetry/actions/workflows/release.yaml)

Add metrics to your Python applications with Pylemetry

Currently, three meters are supported, `Counter`, `Gauge`, and `Timer`

## Counter

The counter meter allows you to keep track of the number of times a block of code is executed.
A `Counter` can be created either directly

```python
from pylemetry.meters import Counter


def some_method() -> None:
    counter = Counter()

    for _ in range(100):
        counter.add()  # counter += 1 is also supported

    counter.get_count()  # 100
```

or via a decorator

```python
from pylemetry import registry
from pylemetry.decorators import count


@count()
def some_method() -> None:
    ...


@count("named_counter")
def another_method() -> None:
    ...


def main() -> None:
    for _ in range(100):
        some_method()
        another_method()

    counter = registry.get_counter("some_method")
    counter.get_count()  # 100

    counter = registry.get_counter("named_counter")
    counter.get_count()  # 100
```

When using this meter via a decorator, the meter gets added to the global `registry`, with the method name it's decorating as the meter name. Alternatively, you can provide a name for the meter as a parameter to the decorator

## Gauge

A `Gauge` meter allows you to keep track of varying metrics, e.g. memory usage or items on a queue. This meter currently isn't supported as a decorator

```python
from pylemetry import registry
from pylemetry.meters import Gauge


def some_method() -> None:
    gauge = Gauge()
    
    registry.add_gauge("sample_gauge", gauge)
```

The `Gauge` supports incrementing, decrementing, and setting a value directly

```python
from pylemetry import registry


gauge = registry.get_gauge("sample_gauge")

gauge.add(10)
gauge += 1.5
gauge.get_value()  # 11.5

gauge.subtract(10)
gauge -= 8.5
gauge.get_value()  # -7

gauge.set_value(7.5)
gauge.get_value()  # 7.5
```

## Timer

A `Timer` meter allows for tracking the time taken for a block of code. This can be done either directly

```python
from pylemetry.meters import Timer


def some_method() -> None:
    timer = Timer()

    for _ in range(100):
        with timer.time():
            ...

    timer.get_count()  # 100
    timer.get_mean_tick_time()  # Mean execution time of the code block
```

or via a decorator

```python
from pylemetry import registry
from pylemetry.decorators import time


@time()
def some_method() -> None:
    ...


@time("named_timer")
def another_method() -> None:
    ...


def main() -> None:
    for _ in range(100):
        some_method()
        another_method()
        
    timer = registry.get_timer("some_method")
    timer.get_count()  # 100
    timer.get_mean_tick_time()  # Mean execution time of the some_method function
    timer.get_max_tick_time()  # Maximum execution time of the some_method function
    timer.get_min_tick_time()  # Minimum execution time of the some_method function

    timer = registry.get_timer("named_timer")
    timer.get_count()  # 100
    ...
```

When using this meter via a decorator, the meter gets added to the global `registry`, with the method name it's decorating as the meter name. Alternatively, you can provide a name for the meter as a parameter to the decorator

## The Registry

Pylemetry maintains a global registry of meters, allowing you to share a meter across multiple files, or reference metrics from a central location.
This registry is also used to keep track of all metrics created by decorators, with those meters registered using the method name they are decorating

```python
from pylemetry import registry
from pylemetry.meters import Counter, Gauge, Timer


counter = Counter()
gauge = Gauge()
timer = Timer()

registry.add_counter("example", counter)
registry.add_gauge("example", gauge)
registry.add_timer("example", timer)
```

Each meter type has an `add_meter`, `get_meter` and `remove_meter` method to manage meters in the `registry`, each requiring a unique meter name.

The `registry` can be cleared through the `clear()` method