# Day 5: What changed from 3.8 to 3.14

**Goal:** catch up on the new syntax you'll see in current code (and in
interviews).

## Summary by version

| Version | What matters                                                                |
|---------|-----------------------------------------------------------------------------|
| 3.8     | walrus `:=`, `f"{x=}"`, positional-only parameters `/`                      |
| 3.9     | `dict \| dict`, `list[int]` without `typing`, `str.removeprefix/removesuffix`, `zoneinfo` |
| 3.10    | **`match`/`case`**, `X \| Y` in types, `zip(strict=True)`, better error messages |
| 3.11    | **10–60% faster**, `ExceptionGroup` + `except*`, `tomllib`, `Self`, `StrEnum`, `asyncio.TaskGroup` |
| 3.12    | **generics `class C[T]`**, `type Alias = ...`, f-strings without quote limits, `itertools.batched`, `@override` |
| 3.13    | new REPL (colors, multiline), **free-threaded** build (no GIL, experimental), experimental JIT |
| 3.14    | **t-strings** `t"..."` (templates), deferred evaluation of annotations, officially supported free-threading |

## 1. `match` / `case`

It isn't a `switch`: it's **structural pattern matching**. It takes structures apart and
captures variables.

```python
match command.split():
    case ["go", direction]:  # sequence of 2, capture
        ...
    case ["take", *objects] if objects:  # rest + guard
        ...
    case ["exit" | "quit"]:  # alternatives
        ...
    case _:  # wildcard
        ...

match event:  # mappings: extra keys are ignored
    case {"type": "click", "x": int(x), "y": int(y)}:
        ...

match shape:  # classes (uses attributes)
    case Circle(radius=0):
        ...
    case Rectangle(width=a, height=b) if a == b:
        ...
```

**Trap:** a bare name in a `case` **captures**, it doesn't compare.
`case RED:` captures anything into the variable `RED`. To compare against constants,
use dotted names: `case Color.RED:`.

## 2. Walrus `:=`

Assigns and returns the value inside an expression.

```python
while line := f.readline():
    ...
if m := re.match(pattern, text):
    print(m.group(1))
[y for x in data if (y := f(x)) is not None]  # computes f(x) only once
```

Use it when it removes duplication, not to save a line.

## 3. `ExceptionGroup` and `except*`

They let you report **several errors at once**: validations or concurrent tasks
(`asyncio.TaskGroup` raises them this way).

```python
raise ExceptionGroup("validation", [ValueError("a"), TypeError("b")])

try:
    ...
except* ValueError as eg:  # eg is an ExceptionGroup with only the ValueErrors
    for e in eg.exceptions:
        ...
except* TypeError as eg:  # several branches can run!
    ...
```

## 4. f-strings

```python
f"{name:<12}"  # left-aligned in 12
f"{price:>10,.2f}"  # right-aligned in 10, comma thousands separator, 2 decimals
f"{n:08.3f}"  # zero padding
f"{pct:.1%}"  # 0.256 -> '25.6%'
f"{date:%Y-%m-%d}"  # datetime
f"{x=}"  # 'x=42'
f"{d['key']}"  # 3.12+: same quotes inside
```

## 5. t-strings (3.14, optional)

`t"Hello {name}"` does **not** return a `str` but a `Template` object with the parts
kept separate. It lets libraries do safe interpolation (SQL, HTML, logs) without
injection. It's still very new; recognizing it is enough.

## 6. Others you'll see

- `tomllib.loads()` / `tomllib.load(f)` (binary): read `pyproject.toml` and configs.
- `from typing import Self, override`.
- `asyncio.TaskGroup` (covered in week 3).
- `pathlib.Path` everywhere instead of `os.path`: `Path("a") / "b" / "c.txt"`,
  `.read_text()`, `.glob("*.py")`.

## Exercises

```bash
uv run pytest week1/day5_whats_new
```

**Extra challenge:** rewrite the exercise's `process_event` with an `if/elif` chain and
compare the readability.

## Further reading

- [PEP 636: pattern matching tutorial](https://peps.python.org/pep-0636/). It's the best
  resource for `match`.
- "What's New in Python 3.X" on docs.python.org. Read at least 3.10, 3.11 and 3.12.
