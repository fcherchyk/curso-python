import pytest
from exercise import Circle, Rectangle, describe_shape, interpret_command, process_event


@pytest.mark.parametrize(
    ("command", "expected"),
    [
        ("exit", "bye"),
        ("quit", "bye"),
        ("go north", "going north"),
        ("go up", "invalid direction"),
        ("take sword", "you took: sword"),
        ("take sword shield", "you took: sword, shield"),
        ("take", "I don't understand"),
        ("", "say something"),
        ("dance tango", "I don't understand"),
        ("exit now", "I don't understand"),
    ],
)
def test_interpret_command(command, expected):
    assert interpret_command(command) == expected


@pytest.mark.parametrize(
    ("event", "expected"),
    [
        ({"type": "click", "x": 10, "y": 20}, "click at (10, 20)"),
        ({"type": "click", "x": 1, "y": 2, "button": "left"}, "click at (1, 2)"),
        ({"type": "click", "x": "10", "y": 20}, "unknown"),
        ({"type": "key", "key": "enter"}, "confirm"),
        ({"type": "key", "key": "a"}, "key a"),
        ({"type": "scroll", "delta": -3}, "scroll down"),
        ({"type": "scroll", "delta": 2}, "scroll up"),
        ({"type": "scroll", "delta": 0}, "unknown"),
        ({"other": 1}, "unknown"),
    ],
)
def test_process_event(event, expected):
    assert process_event(event) == expected


def test_describe_shape():
    assert describe_shape(Circle(2)) == "circle of radius 2"
    assert describe_shape(Rectangle(3, 3)) == "square of side 3"
    assert describe_shape(Rectangle(2, 5)) == "rectangle 2 x 5"
    assert describe_shape(Circle(0)) == "degenerate"
    assert describe_shape(Rectangle(0, 4)) == "degenerate"


def test_describe_shape_unknown():
    with pytest.raises(TypeError):
        describe_shape("triangle")
