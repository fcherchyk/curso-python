from collections.abc import Iterable, Iterator


class Countdown:
    def __init__(self, n: int) -> None:
        self.n = n

    def __iter__(self) -> Iterator[int]:
        # A new generator on every call: it can be iterated many times.
        yield from range(self.n, 0, -1)


class Counter:
    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> "Counter":
        return self

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def first[T](iterable: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(iterable), default)


def totals_and_percentages(amounts: Iterable[float]) -> list[float]:
    amounts = list(amounts)  # materialize: we are going to iterate twice
    total = sum(amounts)
    if total == 0:
        return [0.0] * len(amounts)
    return [round(a * 100 / total, 1) for a in amounts]
