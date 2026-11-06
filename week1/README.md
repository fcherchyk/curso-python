# Week 1: Modern, idiomatic syntax

About 6 hours in total, 1 hour per day. Each day builds on the previous one.

| Day | Folder              | Topic                                                    | Tests |
|-----|---------------------|----------------------------------------------------------|-------|
| 1   | `day1_idiomatic`    | comprehensions, unpacking, zip/enumerate, sort, signatures, dicts | 13 |
| 2   | `day2_iterators`    | iteration protocol, generators, lazy pipelines, itertools | 11 |
| 3   | `day3_functions`    | closures, decorators (with and without parameters), context managers | 13 |
| 4   | `day4_modeling`     | dataclasses, StrEnum, dunder methods, Protocol, 3.12 generics | 15 |
| 5   | `day5_whats_new`    | match/case, walrus, ExceptionGroup/except*, f-strings, tomllib | 28 |
| 6   | `day6_project`      | project: log analyzer with a CLI + ruff + mypy           | 15 |

## Checklist

- [ ] Setup: `uv sync` and `uv run pytest` runs (red)
- [ ] Day 1: `uv run pytest week1/day1_idiomatic` green
- [ ] Day 2: `uv run pytest week1/day2_iterators` green
- [ ] Day 3: `uv run pytest week1/day3_functions` green
- [ ] Day 4: `uv run pytest week1/day4_modeling` green
- [ ] Day 5: `uv run pytest week1/day5_whats_new` green
- [ ] Day 6: tests green and the CLI runs on `access.log`
- [ ] Day 6: `ruff check` and `mypy --strict` clean on the project
- [ ] Bonus: at least 3 "Extra challenges"

## End-of-week self-assessment

If you can answer these without looking, the week did its job:

1. What's the difference between an iterable and an iterator? Why can `Countdown` be
   iterated twice and a generator can't?
2. Why is `def f(x, acc=[])` a bug? And why `field(default_factory=list)`?
3. What does `functools.wraps` do and what breaks if you don't use it?
4. When would you use `@contextmanager` and when a class with `__enter__`/`__exit__`?
5. In a `case`, what's the difference between `case RED:` and `case Color.RED:`?
6. Protocol or abstract base class? What changes for the implementer?
7. What does `frozen=True` give you besides immutability?
