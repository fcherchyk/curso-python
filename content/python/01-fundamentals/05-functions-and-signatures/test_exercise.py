import pytest
from exercise import add_item, average, create_user, format_attributes


def test_add_item_without_shared_default():
    assert add_item("a") == ["a"]
    assert add_item("b") == ["b"]


def test_add_item_with_list():
    xs = ["x"]
    assert add_item("y", xs) == ["x", "y"]
    assert xs == ["x", "y"]


def test_average():
    assert average(1, 2, 3, 4) == 2.5
    assert average(7) == 7
    assert average(*[2, 4]) == 3


def test_average_without_numbers():
    with pytest.raises(ValueError):
        average()


def test_create_user():
    assert create_user("alice", admin=True, email="a@b.c") == {
        "name": "alice",
        "admin": True,
        "email": "a@b.c",
    }
    assert create_user("bob") == {"name": "bob", "admin": False}


def test_create_user_name_positional_only():
    with pytest.raises(TypeError):
        create_user(name="alice")


def test_create_user_admin_keyword_only():
    with pytest.raises(TypeError):
        create_user("alice", True)


def test_format_attributes():
    assert (
        format_attributes(id="x", disabled=True, hidden=False, title="Hello")
        == 'id="x" disabled title="Hello"'
    )
    assert format_attributes() == ""
    assert format_attributes(n=0, v=None) == 'n="0"'
