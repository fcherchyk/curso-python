import subprocess
import sys
import types
from datetime import datetime
from pathlib import Path

import pytest
from exercise import (
    InvalidLine,
    Method,
    Record,
    Summary,
    format_report,
    main,
    parse,
    parse_line,
    summarize,
    top_paths,
)

HERE = Path(__file__).parent

LOG = """\
2026-09-20T10:00:00 GET /api/users 200 100ms
2026-09-20T10:00:01 GET /api/users 200 120ms
2026-09-20T10:00:02 POST /api/orders 201 300ms
2026-09-20T10:00:03 GET /api/report 500 900ms

2026-09-20T10:00:04 GET /api/users 404 80ms
broken line
2026-09-20T10:00:05 DELETE /api/orders 204 150ms
"""


@pytest.fixture
def records():
    return list(parse(LOG.splitlines(keepends=True)))


# --- parsing --------------------------------------------------------------


def test_parse_line():
    r = parse_line("2026-09-20T10:15:32 GET /api/users 200 123ms\n")
    assert r == Record(datetime(2026, 9, 20, 10, 15, 32), Method.GET, "/api/users", 200, 123)
    assert not r.is_error
    assert parse_line("2026-09-20T10:15:32 POST /x 503 1ms").is_error


@pytest.mark.parametrize(
    "line",
    [
        "anything at all",
        "2026-09-20T10:15:32 GET /api 200",  # missing duration
        "2026-09-20T10:15:32 FOO /api 200 5ms",  # unknown method
        "2026-13-45T10:15:32 GET /api 200 5ms",  # impossible date
    ],
)
def test_parse_line_invalid(line):
    with pytest.raises(InvalidLine, match="api|anything"):
        parse_line(line)


def test_invalid_line_chains_the_cause():
    with pytest.raises(InvalidLine) as info:
        parse_line("2026-13-45T10:15:32 GET /api 200 5ms")
    assert isinstance(info.value.__cause__, ValueError), "use `raise ... from e`"


def test_parse_is_generator_and_collects_invalid():
    invalid = []
    gen = parse(LOG.splitlines(keepends=True), invalid)
    assert isinstance(gen, types.GeneratorType)
    recs = list(gen)
    assert len(recs) == 6
    assert invalid == ["broken line"]


def test_parse_without_invalid_list():
    assert len(list(parse(["garbage", ""]))) == 0


# --- analysis -------------------------------------------------------------


def test_summarize(records):
    s = summarize(records)
    assert s.total == 6
    assert s.errors == 1
    assert s.error_rate == pytest.approx(1 / 6)
    assert s.by_status == {200: 2, 201: 1, 204: 1, 404: 1, 500: 1}
    assert list(s.by_status) == [200, 201, 204, 404, 500]
    assert s.p50_ms == 135.0
    assert s.p95_ms == 750.0
    assert s.slowest_path == "/api/report"


def test_summarize_accepts_generator():
    assert summarize(parse(LOG.splitlines())).total == 6


def test_summarize_edge_cases():
    empty = summarize([])
    assert empty == Summary(0, 0, {}, 0.0, 0.0, "")
    assert empty.error_rate == 0.0
    one = summarize([parse_line("2026-09-20T10:00:00 GET /a 200 42ms")])
    assert (one.p50_ms, one.p95_ms) == (42.0, 42.0)


def test_top_paths(records):
    assert top_paths(records, 2) == [("/api/users", 3), ("/api/orders", 2)]
    assert len(top_paths(records)) == 3


# --- output and CLI -------------------------------------------------------

REPORT = """\
Requests: 6 (invalid: 1)
5xx errors: 1 (16.7%)
Latency p50: 135.0 ms | p95: 750.0 ms
Slowest path: /api/report
Status:
  200: 2
  201: 1
  204: 1
  404: 1
  500: 1
Top paths:
  /api/users        3
  /api/orders       2"""


def test_format_report(records):
    assert format_report(summarize(records), top_paths(records, 2), 1) == REPORT


def test_main(tmp_path, capsys):
    log = tmp_path / "access.log"
    log.write_text(LOG, encoding="utf-8")
    assert main([str(log), "--top", "2"]) == 0
    assert capsys.readouterr().out == REPORT + "\n"


def test_main_missing_file(tmp_path, capsys):
    assert main([str(tmp_path / "missing.log")]) == 1
    assert "Not found" in capsys.readouterr().err


def test_real_cli_on_access_log():
    r = subprocess.run(
        [sys.executable, "exercise.py", "access.log", "--top", "3"],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("Requests: ")
    assert r.stdout.count("\n  /") == 3, "it must list 3 paths in the top"
