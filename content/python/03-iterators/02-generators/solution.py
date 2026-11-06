from collections.abc import Iterable, Iterator
from itertools import count


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def useful_lines(lines: Iterable[str]) -> Iterator[str]:
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            yield line


def deep_flatten(nested: Iterable[object]) -> Iterator[object]:
    for x in nested:
        if isinstance(x, (list, tuple)):
            yield from deep_flatten(x)
        else:
            yield x


def decimal_range(start: float, stop: float, step: float) -> Iterator[float]:
    # Since this is a generator, this check only runs on the first next().
    if step <= 0:
        raise ValueError("step must be positive")
    for i in count():
        value = round(start + i * step, 10)
        if value >= stop:
            return
        yield value
