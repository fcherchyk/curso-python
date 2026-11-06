"""Pattern matching: match / case.

Solve all three functions with `match` (no if/elif chains).
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Circle:
    radius: float


@dataclass
class Rectangle:
    width: float
    height: float


def interpret_command(command: str) -> str:
    """Interpret text commands with `match` on `command.split()`:

    - "exit" or "quit"           -> "bye"
    - "go <dir>"                 -> "going <dir>"   (dir: north/south/east/west)
    - "go <anything else>"       -> "invalid direction"
    - "take <obj> [<obj>...]"    -> "you took: a, b"   (one or more objects)
    - ""                         -> "say something"
    - anything else              -> "I don't understand"
    """
    raise NotImplementedError("TODO")


def process_event(event: dict[str, Any]) -> str:
    """Mapping patterns over JSON-like events:

    - {"type": "click", "x": int, "y": int}   -> "click at (x, y)"
    - {"type": "key", "key": "enter"}         -> "confirm"
    - {"type": "key", "key": str}             -> "key <key>"
    - {"type": "scroll", "delta": d} with d<0 -> "scroll down" / d>0 -> "scroll up"
    - other                                   -> "unknown"
    """
    raise NotImplementedError("TODO")


def describe_shape(shape: object) -> str:
    """Class patterns:

    - Circle with radius 0 or Rectangle with a side of 0 -> "degenerate"
    - Circle(r)                                          -> "circle of radius r"
    - Rectangle(a, a) (equal sides)                      -> "square of side a"
    - Rectangle(a, b)                                    -> "rectangle a x b"
    - anything else                                      -> TypeError
    """
    raise NotImplementedError("TODO")
