import subprocess
import sys
from pathlib import Path

import pytest
from exercise import find_user, normalize_tags, weighted_average

FILE = Path(__file__).parent / "exercise.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", *args, str(FILE)],
        capture_output=True,
        text=True,
        cwd=FILE.parent,
    )


def test_weighted_average():
    assert weighted_average([10, 20], [1, 3]) == 17.5
    with pytest.raises(ValueError):
        weighted_average([1, 2], [1])
    with pytest.raises(ValueError):
        weighted_average([1], [0])


def test_normalize_tags():
    assert normalize_tags([" Python", "python ", "", "  ", "Web", "API"]) == [
        "api",
        "python",
        "web",
    ]


def test_find_user():
    users = {1: "alice", 2: "bob"}
    assert find_user(users, 2) == "BOB"
    assert find_user(users, 9) is None


def test_ruff_clean():
    r = run("ruff", "check", "--isolated", "--select", "E,F,I,UP,B,SIM", "--line-length", "100")
    assert r.returncode == 0, "ruff found problems:\n" + r.stdout


def test_mypy_strict():
    r = run("mypy", "--strict", "--no-incremental", "--cache-dir", "/dev/null")
    assert r.returncode == 0, "mypy found problems:\n" + r.stdout
