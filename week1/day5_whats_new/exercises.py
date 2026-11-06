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
    raise NotImplementedError("TODO")


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
    raise NotImplementedError("TODO")


def describe_shape(shape: object) -> str:
    """Class patterns:

    - Circle with radius 0 or Rectangle with a side of 0 -> "degenerate"
    - Circle(r)                                          -> "circle of radius r"
    - Rectangle(a, a) (equal sides)                      -> "square of side a"
    - Rectangle(a, b)                                    -> "rectangle a x b"
    - anything else                                      -> TypeError

    Hint: `case Circle(radius=0)`, `case Rectangle(width=a, height=b) if a == b`.
    """
    raise NotImplementedError("TODO")


def read_in_chunks(file: IO[str], size: int) -> list[str]:
    """Read the file in chunks of `size` characters until the end.

    Hint: `while (chunk := file.read(size)):`
    """
    raise NotImplementedError("TODO")


def lengths_above(words: list[str], minimum: int) -> list[int]:
    """Lengths of the words whose length is > minimum, computing len() ONCE
    per word.

    Hint: `[n for w in words if (n := len(w)) > minimum]`.
    """
    raise NotImplementedError("TODO")


def validate_user(data: dict[str, Any]) -> None:
    """Validate ALL the fields and report all the errors together.

    - "name": non-empty str                   -> otherwise, ValueError("name")
    - "age": int                              -> if not an int, TypeError("age")
    - "age" >= 0                              -> if negative, ValueError("age")
    - "email": contains "@"                   -> otherwise, ValueError("email")

    If there are errors, raise `ExceptionGroup("invalid user", errors)`.
    Missing fields count as invalid.
    """
    raise NotImplementedError("TODO")


def classify_errors(data: dict[str, Any]) -> dict[str, list[str]]:
    """Call `validate_user` and classify the errors with `except*`.

    Return {"value": [...ValueError messages], "type": [...TypeError messages]}.
    If there are no errors, both lists are empty.

    Hint: inside `except* ValueError as group:`, `group.exceptions` is
    the tuple with the ValueErrors.
    """
    raise NotImplementedError("TODO")


def price_table(rows: list[tuple[str, float]]) -> str:
    """Format a fixed-width table, one line per row, joined with "\\n":

    - name left-aligned in 12 characters
    - price right-aligned in 10, with a thousands separator and 2 decimal places
    - at the end, a "TOTAL" line with the same format

    >>> print(price_table([("coffee", 1500.5)]))
    coffee        1,500.50
    TOTAL         1,500.50
    """
    raise NotImplementedError("TODO")


DEFAULTS: dict[str, Any] = {"host": "localhost", "port": 8000, "debug": False}


def load_config(toml_text: str) -> dict[str, Any]:
    """Parse TOML and return the [server] section merged over DEFAULTS.

    If there is no [server] section, return a copy of DEFAULTS.
    Also, if "host" starts with "http://" or "https://", strip the prefix.

    Hint: `tomllib.loads`, `DEFAULTS | section`, `str.removeprefix`.
    """
    raise NotImplementedError("TODO")
