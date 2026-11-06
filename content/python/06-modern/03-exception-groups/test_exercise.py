import pytest
from exercise import classify_errors, run_all, validate_user


def test_validate_user_ok():
    assert validate_user({"name": "Alice", "age": 30, "email": "a@b.com"}) is None


def test_validate_user_reports_everything():
    with pytest.raises(ExceptionGroup) as info:
        validate_user({"name": "", "age": "thirty", "email": "no-at-sign"})
    messages = sorted(str(e) for e in info.value.exceptions)
    assert messages == ["age", "email", "name"]


def test_validate_user_missing_fields():
    with pytest.raises(ExceptionGroup) as info:
        validate_user({})
    assert len(info.value.exceptions) == 3


def test_classify_errors():
    assert classify_errors({"name": "", "age": -1, "email": "x"}) == {
        "value": ["name", "age", "email"],
        "type": [],
    }
    assert classify_errors({"name": "A", "age": "x", "email": "a@b"}) == {
        "value": [],
        "type": ["age"],
    }
    assert classify_errors({"name": "A", "age": 1, "email": "a@b"}) == {
        "value": [],
        "type": [],
    }


def test_run_all_without_errors():
    assert run_all([lambda: 1, lambda: "two"]) == [1, "two"]


def test_run_all_collects_errors_with_notes():
    runs = []

    def ok():
        runs.append("ok")
        return 1

    def boom():
        raise KeyError("x")

    def another():
        raise ValueError("y")

    with pytest.raises(ExceptionGroup) as info:
        run_all([boom, ok, another])
    assert runs == ["ok"], "it must run every task even if some fail"
    excs = info.value.exceptions
    assert [type(e) for e in excs] == [KeyError, ValueError]
    assert excs[0].__notes__ == ["task 0"]
    assert excs[1].__notes__ == ["task 2"]
