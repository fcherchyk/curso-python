import io
import math

import pytest
from exercise import Circle, InMemoryNotifier, Notifier, close_all, total_area


def test_total_area_duck_typing():
    class Square:  # doesn't inherit from anything
        def area(self):
            return 4.0

    assert total_area([Circle(1), Square()]) == pytest.approx(math.pi + 4)
    assert total_area([]) == 0


def test_notifier_is_abstract():
    with pytest.raises(TypeError):
        Notifier()


def test_incomplete_subclass_cannot_be_instantiated():
    class Incomplete(Notifier):
        pass

    with pytest.raises(TypeError):
        Incomplete()


def test_in_memory_notifier():
    n = InMemoryNotifier()
    assert n.send("alice", "hello") is True
    assert n.send("", "hello") is False
    assert n.sent == [("alice", "hello")]


def test_send_to_all_uses_send():
    n = InMemoryNotifier()
    assert n.send_to_all(["a", "", "b"], "x") == 2
    assert n.sent == [("a", "x"), ("b", "x")]


def test_close_all():
    file = io.StringIO("x")

    class Connection:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    c = Connection()
    assert close_all([file, c, 42, "text"]) == 2
    assert file.closed and c.closed
