# ruff and mypy: automated quality

Two tools handle almost all automated quality checks in a modern Python project. **ruff** is
an ultra-fast linter and formatter that replaces flake8, isort, black, pyupgrade and dozens
of plugins. **mypy** is the type checker that verifies your type hints are consistent. Set
them up once and they warn you about bugs and outdated code before you run anything.

## ruff: linter

```bash
uv run ruff check                  # analyzes the whole project
uv run ruff check --fix            # fixes what can be fixed automatically
uv run ruff check app/main.py      # a single file
uv run ruff rule E711              # explains a rule
```

Rules are grouped by **prefix**, inherited from the original tool:

| Prefix  | Origin        | What it detects                                          |
|---------|---------------|----------------------------------------------------------|
| `E`/`W` | pycodestyle   | style: long lines, whitespace, `== None`                 |
| `F`     | pyflakes      | unused imports, undefined names, unused variables        |
| `I`     | isort         | import order                                             |
| `UP`    | pyupgrade     | old syntax: `List[int]`, `Optional`, `%` formatting      |
| `B`     | bugbear       | pitfalls: mutable defaults, bare `except:`               |
| `SIM`   | simplify      | code that can be simplified                              |
| `N`     | pep8-naming   | naming conventions                                       |
| `RUF`   | ruff          | ruff's own rules                                         |

Configuration in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"          # for UP: which modern syntax you can use

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501"]                 # if you want to ignore one

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]              # for example, allow assert in tests
```

To ignore a single case, add a comment on the line (with the rule code, never bare):

```python
from module import *  # noqa: F403
```

### Examples of what it finds

```python
import os, sys                   # E401: multiple imports on one line; F401: unused
from typing import List, Optional   # UP035: deprecated import
def f(x: List[int]) -> Optional[str]:   # UP006/UP045: use list[int] and str | None
    if x == None:                # E711: compare to None with `is`
        return None
    try: ...
    except: ...                  # E722/B001: bare except
```

## ruff: formatter

```bash
uv run ruff format               # formats everything (black-compatible)
uv run ruff format --check       # only checks, for CI
```

A formatter ends style debates: quotes, whitespace and line breaks. There's almost nothing
to configure, and that's exactly the point.

## mypy: type checker

```bash
uv run mypy app                  # checks a package
uv run mypy --strict file.py     # strict mode
```

mypy reads the annotations and **reasons** about the code:

```python
def find(ids: dict[int, str], id: int) -> str:
    return ids.get(id)       # error: Incompatible return value type (got "str | None", expected "str")
```

The error is real: `.get` can return `None`. The fix is to handle that case or change the
return type to `str | None`.

### `--strict`

Strict mode turns on a set of checks, including:

- every function must be **fully annotated** (`--disallow-untyped-defs`);
- no implicit `Any`;
- it warns when a `# type: ignore` isn't needed.

For new projects, start with `strict`. For legacy code, turn it on gradually, module by
module:

```toml
[tool.mypy]
python_version = "3.12"
strict = true

[[tool.mypy.overrides]]
module = ["legacy.*"]
disallow_untyped_defs = false
```

### Handy tools

```python
reveal_type(x)           # mypy tells you the inferred type (only used when checking)
x = f()  # type: ignore[arg-type]   # silence ONE specific error, with its code
from typing import cast
y = cast(int, value)     # "trust me" (no effect at runtime)
```

Alternatives to mypy: **pyright** (used by VS Code with Pylance, very fast) and **ty** (from
Astral, in development). The concepts are the same.

## Fitting it into your workflow

- **In the editor**: the ruff extension flags problems as you type and can format on save.
- **Before committing**: `pre-commit` with the ruff hooks.
- **In CI**: `ruff check`, `ruff format --check`, `mypy` and `pytest`. If any of them fails,
  it doesn't get merged.

```bash
uv run ruff check && uv run ruff format --check && uv run mypy . && uv run pytest
```

## Summary

- `ruff check [--fix]` as the linter, with rules by prefix (`E`, `F`, `I`, `UP`, `B`, `SIM`)
  and configuration in `pyproject.toml`.
- `ruff format` as a no-debate formatter.
- `mypy --strict` for new projects; gradual adoption with `overrides` in legacy code.
- `# noqa: CODE` and `# type: ignore[code]` always with the specific code.
- Everything runs in CI.

## Exercise

The file has **legacy** code: badly written imports, pre-3.10 type syntax and unannotated
functions. Implement the functions and make it **clean for ruff** (`E, F, I, UP, B, SIM`)
**and for `mypy --strict`**. The tests run both tools on your file.

**Further reading:** [ruff rules](https://docs.astral.sh/ruff/rules/),
[mypy: getting started](https://mypy.readthedocs.io/en/stable/getting_started.html).
