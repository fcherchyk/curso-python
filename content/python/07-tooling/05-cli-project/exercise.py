"""Capstone project: access log analyzer with a CLI.

Implement the pieces in order (see the lesson). Format of each line:

    2026-09-20T10:15:32 GET /api/users 200 123ms
"""

import argparse  # noqa: F401
import re
import statistics  # noqa: F401
import sys  # noqa: F401
from collections import Counter  # noqa: F401
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path  # noqa: F401


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class InvalidLine(ValueError):
    """The line doesn't match the expected format."""


@dataclass(frozen=True, slots=True)
class Record:
    timestamp: datetime
    method: Method
    path: str
    status: int
    duration_ms: int

    @property
    def is_error(self) -> bool:
        """True if the status is 5xx."""
        raise NotImplementedError("TODO")


PATTERN = re.compile(
    r"^(?P<timestamp>\S+) (?P<method>[A-Z]+) (?P<path>/\S*) (?P<status>\d{3}) (?P<ms>\d+)ms$"
)


def parse_line(line: str) -> Record:
    """Turn a line into a Record.

    Any problem (regex doesn't match, invalid date, unknown method) must
    raise `InvalidLine` with the line in the message. Use `raise ... from e`
    to chain the original cause.

    Hint: `PATTERN.match(line.strip())`, `datetime.fromisoformat`, `Method(...)`.
    """
    raise NotImplementedError("TODO")


def parse(lines: Iterable[str], invalid: list[str] | None = None) -> Iterator[Record]:
    """Generator of Records. Skips empty lines.

    Invalid lines don't stop processing: they're discarded and, if the
    `invalid` list was passed, appended to it (without the newline).
    """
    raise NotImplementedError("TODO")


@dataclass(frozen=True)
class Summary:
    total: int
    errors: int
    by_status: dict[int, int]
    p50_ms: float
    p95_ms: float
    slowest_path: str

    @property
    def error_rate(self) -> float:
        """errors / total (0.0 if total is 0)."""
        raise NotImplementedError("TODO")


def summarize(records: Iterable[Record]) -> Summary:
    """Compute the summary in ONE pass over `records` (it may be a generator:
    materialize it into a list just once).

    - by_status: dict status -> count, sorted by status ascending.
    - p50_ms / p95_ms: `statistics.quantiles(durations, n=100, method="inclusive")`,
      indexes 49 and 94. With fewer than 2 records, both are the single duration (or 0.0).
    - slowest_path: the path with the HIGHEST AVERAGE duration ("" if there are no records).
      On a tie, the one that appeared first.
    """
    raise NotImplementedError("TODO")


def top_paths(records: Iterable[Record], n: int = 5) -> list[tuple[str, int]]:
    """The `n` most requested paths with their count (ties: order of appearance)."""
    raise NotImplementedError("TODO")


def format_report(summary: Summary, top: list[tuple[str, int]], invalid: int) -> str:
    """Report text. Exact format (see the test):

        Requests: 10 (invalid: 1)
        5xx errors: 2 (20.0%)
        Latency p50: 120.0 ms | p95: 900.0 ms
        Slowest path: /api/report
        Status:
          200: 7
          500: 2
        Top paths:
          /api/users      4
          /api/orders     3
    (path left-aligned in 15 characters, count right-aligned in 4)
    """
    raise NotImplementedError("TODO")


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: `file` (positional) and `--top N` (default 5).

    Prints the report to stdout and returns 0. If the file doesn't exist,
    prints "Not found: <file>" to stderr and returns 1.

    Hint: `argparse.ArgumentParser`, `type=Path`, `type=int`. Read the file
    ONCE into a list of records (you'll use it twice).
    """
    raise NotImplementedError("TODO")


if __name__ == "__main__":
    raise SystemExit(main())
