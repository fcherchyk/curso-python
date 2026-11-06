"""Context managers."""

import os  # noqa: F401
import time  # noqa: F401
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


class Timer:
    """Context manager that measures how long the block takes.

        with Timer() as t:
            do_something()
        print(t.duration)   # seconds (float)

    Use `time.perf_counter()`. `duration` is None until the block finishes
    (and it's set even if the block fails). It doesn't suppress exceptions.
    """

    def __init__(self) -> None:
        self.duration: float | None = None

    def __enter__(self) -> "Timer":
        raise NotImplementedError("TODO")

    def __exit__(self, *exc_info: object) -> None:
        raise NotImplementedError("TODO")


@contextmanager
def in_directory(path: str | Path) -> Iterator[Path]:
    """Change the working directory for the duration of the block and restore it on
    exit, EVEN if there's an exception. `yield` the new directory as a Path.
    """
    raise NotImplementedError("TODO")
    yield  # (so it's a generator; delete this line when you implement it)


@contextmanager
def capture_errors(*types: type[Exception]) -> Iterator[list[Exception]]:
    """Suppress exceptions of the given `types` and append them to the list the
    `with` hands out. Any other exception propagates.

        with capture_errors(ValueError) as errors:
            int("x")
        errors  # [ValueError(...)]
    """
    raise NotImplementedError("TODO")
    yield  # (so it's a generator; delete this line when you implement it)
