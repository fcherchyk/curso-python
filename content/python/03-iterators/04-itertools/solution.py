import itertools
from collections import deque
from collections.abc import Iterable, Iterator


def windows(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    window: deque[int] = deque(maxlen=n)
    for x in iterable:
        window.append(x)
        if len(window) == n:
            yield tuple(window)


def compress_runs(text: str) -> list[tuple[str, int]]:
    return [(c, sum(1 for _ in group)) for c, group in itertools.groupby(text)]


def combinations_that_sum(nums: list[int], k: int, target: int) -> list[tuple[int, ...]]:
    return [c for c in itertools.combinations(nums, k) if sum(c) == target]


def balances(initial: float, transactions: Iterable[float]) -> list[float]:
    return list(itertools.accumulate(transactions, initial=initial))
