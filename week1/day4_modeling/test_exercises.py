import dataclasses
import math

import pytest

from week1.day4_modeling.exercises import (
    Cart,
    Circle,
    Item,
    Point,
    Rectangle,
    Stack,
    Status,
    Version,
    first,
    total_area,
)


class TestPoint:
    def test_distance(self):
        assert Point(0, 0).distance(Point(3, 4)) == 5

    def test_add(self):
        assert Point(1, 2) + Point(3, 4) == Point(4, 6)

    def test_immutable_and_hashable(self):
        p = Point(1, 1)
        with pytest.raises(dataclasses.FrozenInstanceError):
            p.x = 5
        assert len({Point(1, 1), Point(1, 1), Point(2, 2)}) == 2


class TestVersion:
    def test_from_str(self):
        assert Version.from_str("1.2.3") == Version(1, 2, 3)
        assert Version.from_str("2") == Version(2, 0, 0)
        with pytest.raises(ValueError):
            Version.from_str("1.x")

    def test_ordering(self):
        vs = [Version.from_str(s) for s in ["1.10.0", "1.2.0", "0.9.9", "1.2.10"]]
        assert [str(v) for v in sorted(vs)] == ["0.9.9", "1.2.0", "1.2.10", "1.10.0"]
        assert Version(2) > Version(1, 99, 99)

    def test_str_and_repr(self):
        v = Version(1, 2, 3)
        assert str(v) == "1.2.3"
        assert repr(v) == "Version(major=1, minor=2, patch=3)"


class TestStatus:
    def test_is_string(self):
        assert Status.PENDING == "pending"
        assert Status("in_progress") is Status.IN_PROGRESS

    def test_next_status(self):
        assert Status.PENDING.next_status() is Status.IN_PROGRESS
        assert Status.IN_PROGRESS.next_status() is Status.DONE
        with pytest.raises(ValueError):
            Status.DONE.next_status()


class TestCart:
    def test_cart(self):
        c = Cart().add(Item("bread", 1.5, 2)).add(Item("milk", 0.99))
        assert c.total == 3.99
        assert len(c) == 3
        assert "bread" in c
        assert "wine" not in c
        assert [i.name for i in c] == ["bread", "milk"]

    def test_carts_do_not_share_list(self):
        a, b = Cart(), Cart()
        a.add(Item("x", 1))
        assert len(b) == 0


class TestShapes:
    def test_total_area_duck_typing(self):
        class Square:  # doesn't inherit from anything
            def area(self):
                return 4.0

        total = total_area([Circle(1), Rectangle(2, 3), Square()])
        assert total == pytest.approx(math.pi + 6 + 4)

    def test_rectangle_validates(self):
        with pytest.raises(ValueError):
            Rectangle(-1, 2)


class TestStack:
    def test_operations(self):
        s: Stack[int] = Stack()
        assert len(s) == 0
        assert not s
        assert s.peek() is None
        s.push(1)
        s.push(2)
        assert s
        assert s.peek() == 2
        assert s.pop() == 2
        assert s.pop() == 1
        with pytest.raises(IndexError):
            s.pop()

    def test_repr(self):
        assert repr(Stack([1, 2])) == "Stack([1, 2])"


def test_first():
    assert first([3, 4]) == 3
    assert first(x for x in "abc") == "a"
    assert first([]) is None
    assert first([], default=0) == 0
