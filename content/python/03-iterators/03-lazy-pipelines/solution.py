import itertools
from collections.abc import Iterable, Iterator


def first_even_squares(numbers: Iterable[int], n: int) -> list[int]:
    squares = (x * x for x in numbers)
    evens = (s for s in squares if s % 2 == 0)
    return list(itertools.islice(evens, n))


def in_batches(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def parse_access_log(lines: Iterable[str]) -> Iterator[tuple[str, int, int]]:
    for line in lines:
        try:
            ip, _method, _path, status, bytes_ = line.split()
            yield ip, int(status), int(bytes_)
        except ValueError:  # wrong number of fields or invalid numbers
            continue


def bytes_by_status(lines: Iterable[str]) -> dict[int, int]:
    totals: dict[int, int] = {}
    for _ip, status, bytes_ in parse_access_log(lines):
        totals[status] = totals.get(status, 0) + bytes_
    return dict(sorted(totals.items()))
