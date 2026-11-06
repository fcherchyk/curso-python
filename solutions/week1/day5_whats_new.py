"""Day 5 — What's new in 3.8 to 3.14: match, walrus, ExceptionGroup, f-strings, tomllib.

    uv run pytest week1/day5_whats_new
"""

import tomllib
from dataclasses import dataclass
from typing import IO, Any


@dataclass
class Circle:
    radius: float


@dataclass
class Rectangle:
    width: float
    height: float


# ---------------------------------------------------------------------------
# match / case (3.10)
# ---------------------------------------------------------------------------


def parse_command(command: str) -> str:
    """Interpret text commands with `match` on `command.split()`:

    - "exit" or "quit"          -> "bye"
    - "go <dir>"                -> "going <dir>"   (dir: north/south/east/west)
    - "go <anything else>"      -> "invalid direction"
    - "take <obj> [<obj>...]"   -> "you took: a, b"   (one or more objects)
    - ""                        -> "say something"
    - anything else             -> "I don't understand"

    Hint: sequence patterns, `|`, captures with `*rest` and `if` guards.
    """
    match command.split():
        case []:
            return "say something"
        case ["exit" | "quit"]:
            return "bye"
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            return f"going {direction}"
        case ["go", _]:
            return "invalid direction"
        case ["take", *objects] if objects:
            return "you took: " + ", ".join(objects)
        case _:
            return "I don't understand"


def process_event(event: dict[str, Any]) -> str:
    """Mapping patterns on JSON-like events:

    - {"type": "click", "x": int, "y": int}   -> "click at (x, y)"
    - {"type": "key", "key": "enter"}         -> "confirm"
    - {"type": "key", "key": str}             -> "key <key>"
    - {"type": "scroll", "delta": d} with d<0 -> "scroll down" / d>0 -> "scroll up"
    - other                                   -> "unknown"

    Extra keys are ignored (that's how mapping patterns work).
    Hint: `{"x": int(x)}` checks the type and captures at the same time.
    """
    match event:
        case {"type": "click", "x": int(x), "y": int(y)}:
            return f"click at ({x}, {y})"
        case {"type": "key", "key": "enter"}:
            return "confirm"
        case {"type": "key", "key": str(key)}:
            return f"key {key}"
        case {"type": "scroll", "delta": d} if d < 0:
            return "scroll down"
        case {"type": "scroll", "delta": d} if d > 0:
            return "scroll up"
        case _:
            return "unknown"


def describe_shape(shape: object) -> str:
    """Class patterns:

    - Circle with radius 0 or Rectangle with a side of 0 -> "degenerate"
    - Circle(r)                                          -> "circle of radius r"
    - Rectangle(a, a) (equal sides)                      -> "square of side a"
    - Rectangle(a, b)                                    -> "rectangle a x b"
    - anything else                                      -> TypeError

    Hint: `case Circle(radius=0)`, `case Rectangle(width=a, height=b) if a == b`.
    """
    match shape:
        case Circle(radius=0) | Rectangle(width=0) | Rectangle(height=0):
            return "degenerate"
        case Circle(radius=r):
            return f"circle of radius {r}"
        case Rectangle(width=a, height=b) if a == b:
            return f"square of side {a}"
        case Rectangle(width=a, height=b):
            return f"rectangle {a} x {b}"
        case _:
            raise TypeError(f"unknown shape: {shape!r}")


# ---------------------------------------------------------------------------
# Walrus := (3.8)
# ---------------------------------------------------------------------------


def read_in_chunks(file: IO[str], size: int) -> list[str]:
    """Read the file in chunks of `size` characters until the end.

    Hint: `while (chunk := file.read(size)):`
    """
    chunks = []
    while chunk := file.read(size):
        chunks.append(chunk)
    return chunks


def lengths_above(words: list[str], minimum: int) -> list[int]:
    """Lengths of the words whose length is > minimum, computing len() ONCE
    per word.

    Hint: `[n for w in words if (n := len(w)) > minimum]`.
    """
    return [n for w in words if (n := len(w)) > minimum]


# ---------------------------------------------------------------------------
# ExceptionGroup and except* (3.11)
# ---------------------------------------------------------------------------


def validate_user(data: dict[str, Any]) -> None:
    """Validate ALL the fields and report all the errors together.

    - "name": non-empty str                   -> otherwise, ValueError("name")
    - "age": int                              -> if not an int, TypeError("age")
    - "age" >= 0                              -> if negative, ValueError("age")
    - "email": contains "@"                   -> otherwise, ValueError("email")

    If there are errors, raise `ExceptionGroup("invalid user", errors)`.
    Missing fields count as invalid.
    """
    errors: list[Exception] = []
    name = data.get("name")
    if not isinstance(name, str) or not name:
        errors.append(ValueError("name"))
    age = data.get("age")
    if not isinstance(age, int):
        errors.append(TypeError("age"))
    elif age < 0:
        errors.append(ValueError("age"))
    if "@" not in str(data.get("email", "")):
        errors.append(ValueError("email"))
    if errors:
        raise ExceptionGroup("invalid user", errors)


def classify_errors(data: dict[str, Any]) -> dict[str, list[str]]:
    """Call `validate_user` and classify the errors with `except*`.

    Return {"value": [...ValueError messages], "type": [...TypeError messages]}.
    If there are no errors, both lists are empty.

    Hint: inside `except* ValueError as group:`, `group.exceptions` is
    the tuple with the ValueErrors.
    """
    result: dict[str, list[str]] = {"value": [], "type": []}
    try:
        validate_user(data)
    except* ValueError as group:
        result["value"] = [str(e) for e in group.exceptions]
    except* TypeError as group:
        result["type"] = [str(e) for e in group.exceptions]
    return result


# ---------------------------------------------------------------------------
# f-strings with format specs
# ---------------------------------------------------------------------------


def price_table(rows: list[tuple[str, float]]) -> str:
    """Format a fixed-width table, one line per row, joined with "\\n":

    - name left-aligned in 12 characters
    - price right-aligned in 10, with a thousands separator and 2 decimal places
    - at the end, a "TOTAL" line with the same format

    >>> print(price_table([("coffee", 1500.5)]))
    coffee        1,500.50
    TOTAL         1,500.50
    """
    lines = [f"{name:<12}{price:>10,.2f}" for name, price in rows]
    total = sum(p for _, p in rows)
    lines.append(f"{'TOTAL':<12}{total:>10,.2f}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# tomllib (3.11) + dict | operator (3.9) + removeprefix (3.9)
# ---------------------------------------------------------------------------

DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def load_config(toml_text: str) -> dict[str, Any]:
    """Parse TOML and return the [server] section merged over DEFAULTS.

    If there is no [server] section, return a copy of DEFAULTS.
    Also, if "host" starts with "http://" or "https://", strip the prefix.

    Hint: `tomllib.loads`, `DEFAULTS | section`, `str.removeprefix`.
    """
    section = tomllib.loads(toml_text).get("server", {})
    config = DEFAULTS | section
    config["host"] = config["host"].removeprefix("https://").removeprefix("http://")
    return config
