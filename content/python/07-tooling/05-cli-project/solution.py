"""Access log analyzer: reference solution."""

import argparse
import re
import statistics
import sys
from collections import Counter
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path


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
        return 500 <= self.status < 600


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
    line = line.strip()
    if not (m := PATTERN.match(line)):
        raise InvalidLine(line)
    try:
        return Record(
            timestamp=datetime.fromisoformat(m["timestamp"]),
            method=Method(m["method"]),
            path=m["path"],
            status=int(m["status"]),
            duration_ms=int(m["ms"]),
        )
    except ValueError as e:
        raise InvalidLine(line) from e


def parse(lines: Iterable[str], invalid: list[str] | None = None) -> Iterator[Record]:
    """Generator of Records. Skips empty lines.

    Invalid lines don't stop processing: they're discarded and, if the
    `invalid` list was passed, appended to it (without the newline).
    """
    for line in lines:
        if not line.strip():
            continue
        try:
            yield parse_line(line)
        except InvalidLine:
            if invalid is not None:
                invalid.append(line.rstrip("\n"))


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
        return self.errors / self.total if self.total else 0.0


def summarize(records: Iterable[Record]) -> Summary:
    """Compute the summary in ONE pass over `records` (it may be a generator:
    materialize it into a list just once).

    - by_status: dict status -> count, sorted by status ascending.
    - p50_ms / p95_ms: `statistics.quantiles(durations, n=100, method="inclusive")`,
      indexes 49 and 94. With fewer than 2 records, both are the single duration (or 0.0).
    - slowest_path: the path with the HIGHEST AVERAGE duration ("" if there are no records).
      On a tie, the one that appeared first.
    """
    recs = list(records)
    if not recs:
        return Summary(0, 0, {}, 0.0, 0.0, "")
    durations = [r.duration_ms for r in recs]
    if len(durations) >= 2:
        q = statistics.quantiles(durations, n=100, method="inclusive")
        p50, p95 = q[49], q[94]
    else:
        p50 = p95 = float(durations[0])
    by_path: dict[str, list[int]] = {}
    for r in recs:
        by_path.setdefault(r.path, []).append(r.duration_ms)
    slowest_path = max(by_path, key=lambda path: statistics.fmean(by_path[path]))
    return Summary(
        total=len(recs),
        errors=sum(r.is_error for r in recs),
        by_status=dict(sorted(Counter(r.status for r in recs).items())),
        p50_ms=p50,
        p95_ms=p95,
        slowest_path=slowest_path,
    )


def top_paths(records: Iterable[Record], n: int = 5) -> list[tuple[str, int]]:
    """The `n` most requested paths with their count (ties: order of appearance)."""
    return Counter(r.path for r in records).most_common(n)


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
    lines = [
        f"Requests: {summary.total} (invalid: {invalid})",
        f"5xx errors: {summary.errors} ({summary.error_rate:.1%})",
        f"Latency p50: {summary.p50_ms:.1f} ms | p95: {summary.p95_ms:.1f} ms",
        f"Slowest path: {summary.slowest_path}",
        "Status:",
        *(f"  {status}: {count}" for status, count in summary.by_status.items()),
        "Top paths:",
        *(f"  {path:<15}{count:>4}" for path, count in top),
    ]
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: `file` (positional) and `--top N` (default 5).

    Prints the report to stdout and returns 0. If the file doesn't exist,
    prints "Not found: <file>" to stderr and returns 1.

    Hint: `argparse.ArgumentParser`, `type=Path`, `type=int`. Read the file
    ONCE into a list of records (you'll use it twice).
    """
    parser = argparse.ArgumentParser(description="Analyze access logs")
    parser.add_argument("file", type=Path)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)

    if not args.file.exists():
        print(f"Not found: {args.file}", file=sys.stderr)
        return 1

    invalid: list[str] = []
    with args.file.open(encoding="utf-8") as f:
        records = list(parse(f, invalid))
    print(format_report(summarize(records), top_paths(records, args.top), len(invalid)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
