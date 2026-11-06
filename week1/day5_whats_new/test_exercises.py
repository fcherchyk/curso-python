import io

import pytest

from week1.day5_whats_new.exercises import (
    DEFAULTS,
    Circle,
    Rectangle,
    classify_errors,
    describe_shape,
    lengths_above,
    load_config,
    parse_command,
    price_table,
    process_event,
    read_in_chunks,
    validate_user,
)


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
def test_parse_command(command, expected):
    assert parse_command(command) == expected


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
    with pytest.raises(TypeError):
        describe_shape("triangle")


def test_read_in_chunks():
    assert read_in_chunks(io.StringIO("abcdefg"), 3) == ["abc", "def", "g"]
    assert read_in_chunks(io.StringIO(""), 3) == []


def test_lengths_above():
    assert lengths_above(["a", "tree", "world", "me"], 2) == [4, 5]


def test_validate_user_ok():
    validate_user({"name": "Alice", "age": 30, "email": "a@b.com"})


def test_validate_user_reports_everything():
    with pytest.raises(ExceptionGroup) as info:
        validate_user({"name": "", "age": "thirty", "email": "no-at-sign"})
    messages = sorted(str(e) for e in info.value.exceptions)
    assert messages == ["age", "email", "name"]


def test_classify_errors():
    assert classify_errors({"name": "", "age": -1, "email": "x"}) == {
        "value": ["name", "age", "email"],
        "type": [],
    }
    assert classify_errors({"name": "A", "age": "x", "email": "a@b"}) == {
        "value": [],
        "type": ["age"],
    }
    assert classify_errors({"name": "A", "age": 1, "email": "a@b"}) == {
        "value": [],
        "type": [],
    }


def test_price_table():
    table = price_table([("coffee", 1500.5), ("croissants", 12.0)])
    assert table == ("coffee        1,500.50\ncroissants       12.00\nTOTAL         1,512.50")


def test_load_config():
    toml = """
    [server]
    host = "https://api.example.com"
    port = 9000
    """
    assert load_config(toml) == {"host": "api.example.com", "port": 9000, "debug": False}


def test_load_config_without_section_does_not_mutate_defaults():
    config = load_config('title = "x"')
    assert config == DEFAULTS
    config["port"] = 1
    assert DEFAULTS["port"] == 8000
