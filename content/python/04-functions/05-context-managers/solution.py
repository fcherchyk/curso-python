import os
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Timer:
    def __init__(self) -> None:
        self.duration: float | None = None
        self._start = 0.0

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info: object) -> None:
        # Returning None (falsy) lets the exception, if any, keep propagating.
        self.duration = time.perf_counter() - self._start


@contextmanager
def in_directory(path: str | Path) -> Iterator[Path]:
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)


@contextmanager
def capture_errors(*types: type[Exception]) -> Iterator[list[Exception]]:
    errors: list[Exception] = []
    try:
        yield errors
    except types as e:
        errors.append(e)  # we don't re-raise: it stays suppressed
