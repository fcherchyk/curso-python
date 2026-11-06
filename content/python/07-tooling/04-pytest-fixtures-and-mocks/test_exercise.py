"""Checks YOUR tests with mutation testing (see the previous chapter)."""

import ast
import subprocess
import sys
import tempfile
from functools import cache
from pathlib import Path

import pytest

HERE = Path(__file__).parent
YOUR_TESTS = (HERE / "exercise.py").read_text(encoding="utf-8")
ORIGINAL = (HERE / "weather.py").read_text(encoding="utf-8")

MUTANTS = {
    "ignores_city_in_url": ("/current?city={city}", "/current"),
    "does_not_round": ('return round(data["temp_c"], 1)', 'return data["temp_c"]'),
    "does_not_skip_failures": (
        "except LookupError:\n            continue",
        "finally:\n            pass",
    ),
    "unsorted_report": ("sorted(temperatures.items())", "temperatures.items()"),
}


@cache
def run(weather_code: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "weather.py").write_text(weather_code, encoding="utf-8")
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
    tests = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
    assert len(tests) >= 4, "write at least 4 tests"
    assert "@pytest.fixture" in YOUR_TESTS, "define at least one fixture of your own"
    assert "Mock(" in YOUR_TESTS, "use unittest.mock.Mock"
    assert "tmp_path" in YOUR_TESTS, "use the tmp_path fixture"


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
