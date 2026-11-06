# uv and pyproject.toml

For years, setting up a Python project meant combining several tools: `pyenv` for the Python
version, `venv` or `virtualenv` for the environment, `pip` to install, `pip-tools` or `poetry`
to pin versions, and `pipx` for global tools. **uv** (from Astral, the makers of ruff) replaces
all of that with a single binary, written in Rust and 10 to 100 times faster. Today it's the
de facto standard for new projects, and it's what this course uses.

## `pyproject.toml`: the central file

Every modern project is described in a single file, `pyproject.toml` (PEP 518/621):

```toml
[project]
name = "python-course"
version = "0.1.0"
description = "Python course"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "httpx[http2]>=0.27",           # [extras]: optional dependencies of the package
    "pydantic>=2,<3",
]

[project.scripts]
analyze = "my_package.cli:main"      # creates the `analyze` command on install

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.6", "mypy>=1.11"]     # development only

[tool.ruff]                          # each tool reads its own [tool.X] section
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- **`[project]`**: standard metadata. `dependencies` are the **runtime** dependencies, with
  version constraints (`>=`, `<`, `~=`, `==`).
- **`[dependency-groups]`** (PEP 735): development dependencies (tests, linters) that don't
  ship with your package.
- **`[tool.*]`**: per-tool configuration. Goodbye `setup.cfg`, `.flake8`, `pytest.ini`,
  `mypy.ini`…

## `uv.lock`: exact, reproducible versions

`pyproject.toml` says **which ranges** you accept (`fastapi>=0.115`). `uv.lock` records
**which exact versions** were installed, including every transitive dependency and its hashes.
That way anyone (or CI) who runs `uv sync` gets exactly the same environment.

**`uv.lock` goes into version control.** Never edit it by hand.

## The commands you'll use

```bash
uv init my-project             # creates pyproject.toml, .python-version, README and main.py
uv add fastapi                 # adds to dependencies, installs and updates the lock
uv add --dev pytest ruff       # to the dev group
uv remove httpx
uv sync                        # makes .venv match the lock exactly
uv lock --upgrade-package fastapi   # upgrades one dependency within its range

uv run pytest                  # runs INSIDE the project environment
uv run python -m my_package
uv run uvicorn app.main:app --reload

uv python install 3.13         # installs Python versions (bye, pyenv)
uv python pin 3.13             # pins the project version in .python-version

uvx ruff check                 # runs a tool without installing it (like pipx run)
uv tool install ruff           # installs a global tool
```

`uv run` is the key: it makes sure the environment is in sync and runs the command in it,
**without activating** the virtualenv by hand. If you prefer to activate it, it's still
there: `.venv/bin/activate`.

## Standalone scripts with dependencies (PEP 723)

A single-file script doesn't need a project: dependencies are declared in a special comment
and `uv run` creates a temporary environment:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich"]
# ///
import httpx, rich
...
```

```bash
uv run script.py
```

## Version specifiers

| Specifier        | Means                                             |
|------------------|---------------------------------------------------|
| `>=2.0`          | 2.0 or higher                                     |
| `>=2,<3`         | any 2.x                                           |
| `~=2.4`          | compatible: `>=2.4, <3.0`                         |
| `~=2.4.1`        | `>=2.4.1, <2.5`                                   |
| `==2.4.*`        | any 2.4.x                                         |

For **applications**, broad ranges in `pyproject.toml` plus the lock. For **libraries**, which
others will install, broad ranges only: never pin exact versions, because they cause conflicts
in the projects that depend on you.

## Recommended project layout

```
my-project/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── my_package/        # "src" layout: prevents importing the code without installing it
│       ├── __init__.py
│       └── cli.py
└── tests/
    └── test_cli.py
```

`uv init --package` or `uv init --lib` create this layout.

## Summary

- `pyproject.toml` describes the project: dependencies, development groups and tool
  configuration.
- `uv.lock` pins the exact versions and goes into git.
- `uv add`, `uv sync`, `uv run`; `uv python install/pin`; `uvx` for one-off tools.
- Single-file scripts with inline dependencies (PEP 723).
- Applications: ranges plus lock. Libraries: ranges only.

## Exercise

Functions that read a `pyproject.toml` (with `tomllib`) and extract information: dependencies
without versions, the required Python, and the dependency groups.

**Further reading:** [uv documentation](https://docs.astral.sh/uv/),
[Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/),
[PEP 723](https://peps.python.org/pep-0723/).
