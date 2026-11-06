# Project: a log analyzer with a CLI

Time to put it all together in a real program: a command-line tool that reads an access log,
parses it in an error-tolerant way, computes metrics and prints a report. It's small, but it
has the shape of any professional tool: immutable models, parsing with validation, a lazy
pipeline, aggregations, output formatting and a testable CLI.

```
$ python exercise.py access.log --top 3
Requests: 120 (invalid: 2)
5xx errors: 6 (5.0%)
Latency p50: 113.5 ms | p95: 365.4 ms
Slowest path: /api/report
Status:
  200: 95
  201: 15
  404: 4
  500: 6
Top paths:
  /api/orders      40
  /api/users       37
  /api/products    20
```

## The design, piece by piece

| Piece                     | What it practices                                         |
|---------------------------|-----------------------------------------------------------|
| `Method(StrEnum)`         | enums (module 05)                                         |
| frozen `Record` + `is_error` | dataclasses and `@property`                            |
| `InvalidLine(ValueError)` | custom exceptions chained with `from`                     |
| `parse_line`              | regex with named groups, walrus and validation            |
| `parse`                   | error-tolerant generator (module 03)                      |
| `summarize`               | `Counter`, `statistics`, grouping and `max(key=...)`      |
| `format_report`           | f-strings with format specs and unpacking in lists        |
| `main`                    | `argparse`, `pathlib`, `with`, stderr and exit codes      |

The golden rule of the design: **the logic knows nothing about the console**. `parse`,
`summarize` and `format_report` take and return data. Only `main` reads arguments, opens files
and prints. That's why everything can be tested without files or subprocesses.

## Regex with named groups

```python
import re

PATTERN = re.compile(
    r"^(?P<timestamp>\S+) (?P<method>[A-Z]+) (?P<path>/\S*) (?P<status>\d{3}) (?P<ms>\d+)ms$"
)

if m := PATTERN.match(line.strip()):
    m["status"], m["ms"]          # or m.group("status")
```

- Compile the regex **once**, at module level.
- `(?P<name>...)` makes the code that uses the match readable.
- `^` and `$` anchor the pattern: without them, a line with trailing garbage could slip through.
- Use raw strings (`r"..."`) so `\d` and `\S` reach the regex intact.

## Translating errors: chained custom exceptions

```python
class InvalidLine(ValueError):        # inherit from the closest standard exception
    """The line doesn't match the expected format."""

try:
    timestamp = datetime.fromisoformat(m["timestamp"])
    method = Method(m["method"])
except ValueError as e:
    raise InvalidLine(line) from e
```

The caller handles **a single error type** (`InvalidLine`) without losing the original cause
(`__cause__`). Since it inherits from `ValueError`, code that already caught `ValueError`
keeps working.

## Statistics without numpy: `statistics`

```python
import statistics

statistics.fmean([100, 120, 900])                          # average (float, fast)
statistics.median(durations)
q = statistics.quantiles(durations, n=100, method="inclusive")
p50, p95 = q[49], q[94]                                    # percentiles
```

**Percentiles** are better than the average for latencies: a single 10-second request ruins
the average, but p95 tells you "95% of requests took less than X".

## CLI with `argparse`

```python
import argparse
from pathlib import Path

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze access logs")
    parser.add_argument("file", type=Path)                      # positional
    parser.add_argument("--top", type=int, default=5, help="number of paths")
    args = parser.parse_args(argv)          # argv=None → uses sys.argv[1:]
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Keys to a well-built CLI:

- **`main(argv)` takes the arguments**, so tests call `main(["x.log", "--top", "2"])` without
  subprocesses.
- **It returns an exit code**: 0 on success, nonzero on error. That way it can be chained in
  shell scripts (`&&`).
- **Errors go to stderr** (`print(..., file=sys.stderr)`) and useful output to stdout: that
  way `analyze log > report.txt` doesn't mix errors with the report.
- `argparse` gives you `--help` and type validation for free.

For bigger CLIs, **Typer** (from the author of FastAPI, based on type hints) or **Click**.

## Installing it as a command

With a `pyproject.toml` and a `[project.scripts]` section, uv creates an executable:

```toml
[project.scripts]
analyze-logs = "logs.cli:main"
```

```bash
uv tool install .            # available as `analyze-logs` on your PATH
```

## Suggested steps

1. `Record.is_error` and `parse_line` (tests `test_parse_line*`).
2. `parse` (a generator that collects the invalid lines).
3. `Summary.error_rate`, `summarize` and `top_paths`.
4. `format_report` (exact format: check the test).
5. `main`, and try it for real: the final test runs it on `access.log`.

## Summary

- Separate pure logic (parse, summarize, format) from input and output (`main`).
- Compiled, anchored regexes with named groups.
- Translate errors into a custom exception chained with `from`.
- Percentiles with `statistics.quantiles` for latencies.
- `main(argv) -> int`, errors to stderr, `raise SystemExit(main())`.

## Exercise

Implement the full analyzer: models, parsing, metrics, report and CLI.

**Extra challenges** (no tests): `--since`/`--until` to filter by date, `--json` to emit the
summary with `asdict` + `json.dumps`, and accepting `-` as the file to read from stdin.

**Further reading:** [argparse tutorial](https://docs.python.org/3/howto/argparse.html),
[re](https://docs.python.org/3/library/re.html),
[statistics](https://docs.python.org/3/library/statistics.html), [Typer](https://typer.tiangolo.com/).
