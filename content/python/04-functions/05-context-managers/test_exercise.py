import time
from pathlib import Path

import pytest
from exercise import Timer, capture_errors, in_directory


def test_timer():
    t = Timer()
    assert t.duration is None
    with t as same:
        assert same is t
        time.sleep(0.01)
    assert 0.005 < t.duration < 1


def test_timer_does_not_suppress():
    t = Timer()
    with pytest.raises(RuntimeError), t:
        raise RuntimeError
    assert t.duration is not None


def test_in_directory(tmp_path):
    original = Path.cwd()
    with in_directory(tmp_path) as p:
        assert Path.cwd() == tmp_path.resolve()
        assert p == tmp_path
    assert Path.cwd() == original


def test_in_directory_restores_on_exception(tmp_path):
    original = Path.cwd()
    with pytest.raises(ZeroDivisionError), in_directory(tmp_path):
        _ = 1 / 0
    assert Path.cwd() == original


def test_capture_errors():
    with capture_errors(ValueError, KeyError) as errors:
        int("not a number")
    assert len(errors) == 1
    assert isinstance(errors[0], ValueError)


def test_capture_errors_no_error():
    with capture_errors(ValueError) as errors:
        pass
    assert errors == []


def test_capture_errors_propagates_others():
    with pytest.raises(TypeError), capture_errors(ValueError):
        raise TypeError
