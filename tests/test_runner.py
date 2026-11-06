from pathlib import Path

import pytest

from app.runner import run_tests

TESTS = """\
from exercise import double


def test_double():
    assert double(2) == 4


def test_double_negative():
    assert double(-3) == -6
"""


@pytest.fixture
def files(tmp_path: Path) -> list[Path]:
    path = tmp_path / "test_exercise.py"
    path.write_text(TESTS)
    return [path]


def test_correct_code(files):
    r = run_tests("def double(x):\n    return x * 2\n", files)
    assert r.passed
    assert r.passed_count == 2
    assert [t.name for t in r.tests] == ["test_double", "test_double_negative"]


def test_wrong_code_shows_the_assert(files):
    r = run_tests("def double(x):\n    return x + 2\n", files)
    assert not r.passed
    assert r.passed_count == 1
    failed = next(t for t in r.tests if not t.ok)
    assert "assert" in failed.message
    assert "/tmp" not in failed.message and "course-" not in failed.message


def test_everything_pending(files):
    r = run_tests('def double(x):\n    raise NotImplementedError("TODO")\n', files)
    assert r.passed_count == 0
    assert all("Pending" in t.message for t in r.tests)


def test_syntax_error(files):
    r = run_tests("def double(x:\n", files)
    assert not r.passed
    assert r.error is not None and "SyntaxError" in r.error
    assert "site-packages" not in r.error


def test_infinite_loop_stops_on_timeout(files):
    r = run_tests("while True:\n    pass\n", files, timeout=2)
    assert not r.passed
    assert r.error is not None and "stopped" in r.error


def test_copies_support_folders(tmp_path):
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "hello.txt").write_text("hello")
    tests = tmp_path / "test_exercise.py"
    tests.write_text(
        "from pathlib import Path\n\n\n"
        "def test_reads_template():\n"
        "    assert Path('templates/hello.txt').read_text() == 'hello'\n"
    )
    r = run_tests("", [tests, templates])
    assert r.passed, r.tests
