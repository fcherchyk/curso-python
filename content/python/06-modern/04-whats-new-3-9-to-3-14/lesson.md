# What's new from 3.9 to 3.14

If you learned Python a few years ago, there's quite a bit of new syntax and standard library
that shows up in any current codebase. This chapter is a map by version plus a hands-on review
of the most-used features we haven't covered yet: `tomllib`, `zoneinfo`, the f-string
improvements and t-strings.

## The map

| Version | What matters                                                                  |
|---------|-------------------------------------------------------------------------------|
| 3.8     | walrus `:=`, `f"{x=}"`, positional-only parameters `/`                        |
| 3.9     | `dict \| dict`, `list[int]` without `typing`, `str.removeprefix/removesuffix`, **`zoneinfo`** |
| 3.10    | **`match`/`case`**, `X \| Y` in types, `zip(strict=True)`, `pairwise`, better error messages |
| 3.11    | **10% to 60% faster**, `ExceptionGroup`/`except*`, `add_note`, **`tomllib`**, `Self`, `StrEnum`, `TaskGroup` |
| 3.12    | **`class C[T]` generics**, `type Alias = …`, f-strings without limits, `itertools.batched`, `@override` |
| 3.13    | New REPL (colors, multiline editing), **free-threaded** build (no GIL, experimental), experimental JIT |
| 3.14    | **t-strings** `t"…"`, deferred evaluation of annotations, officially supported free-threading, `compression.zstd` |

Reading the "What's New in Python 3.X" pages for recent versions is a great way to catch up.

## `tomllib` (3.11): reading TOML

TOML is the format of `pyproject.toml` and many config files. The stdlib **reads** it (to
write it you need a package like `tomli-w`):

```python
import tomllib

with open("pyproject.toml", "rb") as f:        # in binary mode!
    data = tomllib.load(f)

config = tomllib.loads('[server]\nport = 8000')   # from a string
config["server"]["port"]                          # 8000 (already an int)
```

TOML has types (`int`, `float`, `bool`, dates, arrays and tables), so you don't have to
convert by hand as you do with `.ini` files.

A very common pattern is merging the loaded config over the defaults with `|`:

```python
DEFAULTS = {"host": "localhost", "port": 8000, "debug": False}
config = DEFAULTS | data.get("server", {})     # doesn't mutate DEFAULTS
```

## `zoneinfo` (3.9): time zones without external libraries

```python
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

now_utc = datetime.now(UTC)                            # always store in UTC
ba = now_utc.astimezone(ZoneInfo("America/Argentina/Buenos_Aires"))
madrid = now_utc.astimezone(ZoneInfo("Europe/Madrid"))     # knows about daylight saving time
```

Golden rules for dates:

- Work with **aware** datetimes (with a zone). *Naive* ones (no zone) are ambiguous.
- **Store and compare in UTC**; convert to the local zone only for display.
- `datetime.utcnow()` is deprecated: use `datetime.now(UTC)`.
- `datetime.fromisoformat()` parses almost any ISO 8601 since 3.11, including the `Z` suffix.

We go deeper in the essential stdlib module.

## f-strings: what's new

```python
f"{x=}"                        # 3.8: 'x=42'
f"{x = :.2f}"                  # combinable with formatting: 'x = 42.00'
f"{user['name']}"              # 3.12: same quotes inside
f"{'\n'.join(lines)}"          # 3.12: backslashes allowed
f"{
    price       # 3.12: multiline expressions and comments
    * quantity
}"
```

And the good old format mini-language, worth keeping handy for tables:

```python
f"{name:<12}"            # left, width 12
f"{price:>10,.2f}"       # right, width 10, thousands, 2 decimals
f"{'TOTAL':^20}"         # centered
f"{n:08.3f}"             # zero-padded
```

## t-strings (3.14): safe templates

`t"Hello {name}"` looks like an f-string, but it **doesn't return a `str`**: it returns a
`Template` object that keeps the literal parts and the interpolated values separate. The idea
is that a library decides **how** to combine them safely:

```python
from string.templatelib import Template

name = "<script>"
t = t"<p>Hello {name}</p>"
t.strings        # ('<p>Hello ', '</p>')
t.values         # ('<script>',)
html(t)          # a function that escapes the values → '<p>Hello &lt;script&gt;</p>'
```

They solve injection problems (SQL, HTML, shell commands) without giving up the convenience of
interpolation syntax. They're still very new: recognizing them is enough. (This course's
environment uses 3.13, so you won't be able to run them here.)

## Others you'll see

```python
from typing import override            # 3.12: marks a method as overriding the parent's
from itertools import batched          # 3.12: batches of n
import tomllib, zoneinfo
"file.tar.gz".removesuffix(".gz")      # 3.9
sorted(d.items(), key=...)             # ordered dicts (3.7) → dict(sorted(...))
```

And in tooling: `uv` replaced pip, venv and pyenv, and `ruff` replaced flake8, isort and black
(next module).

## Summary

- 3.10 brought `match` and `X | Y`; 3.11, speed, `ExceptionGroup` and `tomllib`; 3.12, new
  generics and f-strings without limits; 3.14, t-strings.
- `tomllib.load` in binary mode; merge over the defaults with `|`.
- `zoneinfo` + `datetime.now(UTC)`: store in UTC and display in the local zone.
- f-strings: `=`, nested quotes and the format mini-language for tables.

## Exercise

A fixed-width table with f-strings, a TOML config merged over defaults and a time zone
conversion with `zoneinfo`.

**Further reading:** "What's New" for [3.11](https://docs.python.org/3/whatsnew/3.11.html),
[3.12](https://docs.python.org/3/whatsnew/3.12.html),
[3.13](https://docs.python.org/3/whatsnew/3.13.html) and
[3.14](https://docs.python.org/3/whatsnew/3.14.html).
