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
    match command.split():
        case []:
            return "say something"
        case ["exit" | "quit"]:
            return "bye"
        case ["go", ("north" | "south" | "east" | "west") as direction]:
            return f"going {direction}"
        case ["go", _]:
            return "invalid direction"
        case ["take", *items] if items:
            return "you took: " + ", ".join(items)
        case _:
            return "I don't understand"


def process_event(event: dict[str, Any]) -> str:
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
