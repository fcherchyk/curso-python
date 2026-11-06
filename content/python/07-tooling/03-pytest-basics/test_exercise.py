"""Checks YOUR tests with mutation testing: they must pass with the correct code and
fail with each mutant (a version of business_calendar.py with an injected bug)."""

import ast
import subprocess
import sys
import tempfile
from functools import cache
from pathlib import Path

import pytest

HERE = Path(__file__).parent
YOUR_TESTS = (HERE / "exercise.py").read_text(encoding="utf-8")
ORIGINAL = (HERE / "business_calendar.py").read_text(encoding="utf-8")

MUTANTS = {
    "leap_year_without_100_rule": (
        "year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)",
        "year % 4 == 0",
    ),
    "leap_year_without_400_rule": (
        "year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)",
        "year % 4 == 0 and year % 100 != 0",
    ),
    "does_not_validate_month": ("if not 1 <= month <= 12:", "if not 1 <= month <= 13:"),
    "february_always_28": ("return 29 if is_leap_year(year) else 28", "return 28"),
    "november_with_31": ("month in (4, 6, 9, 11)", "month in (4, 6, 9)"),
}


@cache
def run(calendar_code: str) -> subprocess.CompletedProcess[str]:
    """Runs your tests against the given version of business_calendar.py."""
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "business_calendar.py").write_text(calendar_code, encoding="utf-8")
        (d / "test_yours.py").write_text(YOUR_TESTS, encoding="utf-8")
        (d / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=line"],
            cwd=d,
            capture_output=True,
            text=True,
            timeout=30,
        )


def test_structure_of_your_tests():
    tree = ast.parse(YOUR_TESTS)
    names = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
    assert len([n for n in names if n.startswith("test_")]) >= 4, "write at least 4 tests"
    assert "parametrize" in YOUR_TESTS, "use @pytest.mark.parametrize"
    assert "pytest.raises" in YOUR_TESTS, "use pytest.raises"


def test_your_tests_pass_with_correct_code():
    r = run(ORIGINAL)
    assert r.returncode == 0, "your tests fail with the correct code:\n" + r.stdout[-1500:]


@pytest.mark.parametrize("mutant", MUTANTS)
def test_catches_mutant(mutant):
    assert run(ORIGINAL).returncode == 0, "first, your tests must pass with the original"
    search, replacement = MUTANTS[mutant]
    assert search in ORIGINAL
    r = run(ORIGINAL.replace(search, replacement))
    assert r.returncode != 0, f"mutant '{mutant}' survived: no test caught it"
