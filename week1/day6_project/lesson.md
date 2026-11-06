# Day 6: Capstone project and modern tooling

**Goal:** bring everything from the week together in a real program (a log analyzer with a
CLI) and work like you would on a professional project: tests, linter, formatter and type checker.

## 1. The 2026 tool stack

| Tool        | Replaces                             | Usage                                    |
|-------------|--------------------------------------|------------------------------------------|
| **uv**      | pip, venv, pip-tools, pyenv, pipx    | `uv init`, `uv add httpx`, `uv run ...`, `uv python install 3.13` |
| **ruff**    | flake8, isort, black, pyupgrade      | `uv run ruff check --fix` / `uv run ruff format` |
| **mypy** or **pyright** | —                        | `uv run mypy week1`                      |
| **pytest**  | unittest                             | `uv run pytest -x -k pattern`            |

Everything is configured in **`pyproject.toml`**; look at this repo's. `uv.lock` pins the exact
versions and goes into version control.

```bash
uv init my-project && cd my-project
uv add fastapi                 # dependency
uv add --dev pytest ruff       # development dependency
uv run pytest
uvx ruff check                 # run a tool without installing it
```

## 2. What you'll practice in the project

| Piece                  | Concept from the week                                    |
|------------------------|----------------------------------------------------------|
| `Method(StrEnum)`      | enums (day 4)                                            |
| frozen `Record` + `is_error` | dataclasses and `@property` (day 4)                |
| `parse_line`           | regex with named groups, walrus, `raise ... from e` (day 5) |
| `parse`                | lazy generator that tolerates errors (day 2)             |
| `summarize`            | `Counter`, `statistics`, `max(key=...)`, sorted dict (day 1) |
| `format_report`        | f-strings with format specs, unpacking in lists (days 1 and 5) |
| `main`                 | `argparse`, `pathlib`, `with open`, exit codes (day 3)   |

### Custom and chained exceptions

```python
class InvalidLine(ValueError): ...  # inherit from the closest standard exception


try:
    date = datetime.fromisoformat(text)
except ValueError as e:
    raise InvalidLine(line) from e  # keeps the original cause in the traceback
```

### Regex with named groups

```python
PATTERN = re.compile(r"(?P<status>\d{3}) (?P<ms>\d+)ms$")
if m := PATTERN.search(line):
    m["status"], m["ms"]  # or m.group("status")
```

### CLI with argparse

```python
def main(argv=None) -> int:  # argv=None uses sys.argv; in tests you pass a list
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)
    ...
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Taking `argv` as a parameter makes the CLI testable without subprocess (look at `test_main`).
For bigger CLIs, use **Typer** (from the author of FastAPI) or **Click**.

## 3. Suggested steps

1. `Record.is_error` and `parse_line`. Make the `test_parse_line*` tests pass.
2. `parse`
3. `summarize`, `Summary.error_rate` and `top_paths`
4. `format_report`
5. `main`. Then try it for real:

```bash
uv run python -m week1.day6_project.exercises week1/day6_project/access.log --top 3
```

6. Run the tools and fix whatever they flag:

```bash
uv run ruff check week1/day6_project
uv run ruff format week1/day6_project
uv run mypy week1/day6_project/exercises.py --strict
```

## Extra challenge

- Add `--since` and `--until` (ISO dates) to filter records by range.
- Add `--json` to emit the summary as JSON (`dataclasses.asdict` + `json.dumps`).
- Make it accept `-` as the file to read from stdin (`cat access.log | ...`).

## Further reading

- [uv documentation](https://docs.astral.sh/uv/) and [ruff rules](https://docs.astral.sh/ruff/rules/)
- [pytest docs: fixtures and parametrize](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
