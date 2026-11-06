import re
from collections.abc import Callable
from typing import IO

PRICE = re.compile(r"\$\s*(\d+(?:\.\d+)?)")


def read_in_chunks(file: IO[str], size: int) -> list[str]:
    chunks = []
    while chunk := file.read(size):
        chunks.append(chunk)
    return chunks


def long_lengths(words: list[str], minimum: int) -> list[int]:
    return [n for w in words if (n := len(w)) > minimum]


def extract_prices(lines: list[str]) -> list[float]:
    return [float(m[1]) for line in lines if (m := PRICE.search(line))]


def first_ok(attempt: Callable[[], str | None], max_tries: int) -> str | None:
    for _ in range(max_tries):
        if (result := attempt()) is not None:
            return result
    return None
