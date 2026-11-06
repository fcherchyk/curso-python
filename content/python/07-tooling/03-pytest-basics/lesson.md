# pytest: tests, asserts and parametrize

You've been using pytest in every exercise of the course. In this chapter we switch roles:
**you write the tests**. pytest is the de facto standard testing framework: tests as plain
functions, plain `assert` with detailed messages, and a very powerful system of fixtures and
plugins.

## The bare minimum

```python
# tests/test_business_calendar.py
from business_calendar import is_leap_year

def test_2024_is_leap_year():
    assert is_leap_year(2024)

def test_2023_is_not_leap_year():
    assert not is_leap_year(2023)
```

```bash
uv run pytest
```

Discovery conventions:

- Files named `test_*.py` or `*_test.py`.
- `test_*` functions (or `test_*` methods inside `Test*` classes without `__init__`).
- `testpaths` in `[tool.pytest.ini_options]` sets where to look.

## `assert` with introspection

There's no `assertEqual`, `assertTrue` or the like: you use a regular `assert`, and pytest
**rewrites** the expression to show you what failed:

```
>       assert days_in_month(2023, 2) == 29
E       assert 28 == 29
E        +  where 28 = days_in_month(2023, 2)
```

With lists, dicts and strings it shows the exact **diff**. You can add a message:
`assert x == y, "explanation"`.

For floats, `pytest.approx`:

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx([1.0, 2.5], rel=1e-3)
```

## Checking exceptions: `pytest.raises`

```python
import pytest

def test_invalid_month():
    with pytest.raises(ValueError, match="invalid month"):
        days_in_month(2024, 13)

def test_exception_details():
    with pytest.raises(ValueError) as info:
        days_in_month(2024, 0)
    assert "0" in str(info.value)
```

`match` is a **regex** searched for in the message. The test fails if the exception isn't
raised, or if a different one is raised.

## `parametrize`: one test, many cases

```python
@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (2024, True),     # divisible by 4
        (2023, False),
        (1900, False),    # divisible by 100 but not by 400
        (2000, True),     # divisible by 400
    ],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) is expected
```

Each tuple generates an independent test, with its own result in the report
(`test_is_leap_year[1900-False]`). It's the best way to cover **edge cases** without copy and
paste. With `ids=[...]` or `pytest.param(..., id="century")` you give them readable names.

## What to test

A good test suite covers:

1. **The happy path**: the typical input.
2. **The edges**: 0, empty, one element, the maximum, the first and the last.
3. **The business rules**, each one separately: `is_leap_year` has **three** rules (every 4,
   except every 100, except every 400). If you don't test 1900 and 2000, two of them could be
   wrong and the tests would still be green.
4. **The errors**: invalid inputs that must raise exceptions.

Structure of each test: **Arrange, Act, Assert**. A test should check **one behavior** and
have a name that says which: `test_february_in_leap_year_has_29`.

### How do I know my tests are good? Mutation testing

**Coverage** (`pytest --cov`) measures which lines ran, but not whether you checked anything.
*Mutation testing* is stricter: it injects bugs on purpose (the **mutants**, like changing a
`<=` to `<` or deleting a condition) and checks that **some test fails**. If a mutant
"survives", your tests are missing a case. Tools: `mutmut` and `cosmic-ray`.

This chapter's exercise works exactly like that.

## Running pytest like a pro

```bash
uv run pytest -x                 # stop at the first failure
uv run pytest -k leap            # only tests whose name contains "leap"
uv run pytest --lf               # only the ones that failed last time
uv run pytest -v                 # one line per test
uv run pytest -q                 # quiet
uv run pytest tests/test_x.py::test_y   # a single test
uv run pytest --pdb              # open the debugger on failure
```

### Useful marks

```python
@pytest.mark.skip(reason="depends on the network")
@pytest.mark.skipif(sys.platform == "win32", reason="unix only")
@pytest.mark.xfail(reason="known bug #123")    # expected to fail
```

## Summary

- `test_*` functions in `test_*.py` files with plain `assert`.
- `pytest.raises(Type, match=...)` for exceptions; `pytest.approx` for floats.
- `@pytest.mark.parametrize` to cover many cases, especially the edges.
- Test each rule separately: coverage isn't enough, think about which mutants you'd kill.
- `-x`, `-k`, `--lf` and `-v` for day-to-day work.

## Exercise

In the Code tab, **you write the tests** for `business_calendar.py` (`is_leap_year` and
`days_in_month`). Requirements: at least 4 tests, using `parametrize` and `pytest.raises`.
Your tests are run against the correct code (they must pass) and against **5 mutants** (each
one must make at least one of your tests fail).

```python
# business_calendar.py (what you have to test)
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def days_in_month(year: int, month: int) -> int:
    if not 1 <= month <= 12:
        raise ValueError(f"invalid month: {month}")
    if month == 2:
        return 29 if is_leap_year(year) else 28
    return 30 if month in (4, 6, 9, 11) else 31
```

**Further reading:** [pytest documentation](https://docs.pytest.org/en/stable/),
[parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html),
[mutmut](https://mutmut.readthedocs.io/).
