import dataclasses

import pytest
from exercise import Order, Point, Version


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


class TestOrder:
    def test_independent_defaults(self):
        a, b = Order("alice"), Order("bob")
        a.items.append("coffee")
        assert b.items == []
        assert a.status == "new"

    def test_validates_customer(self):
        with pytest.raises(ValueError):
            Order("   ")

    def test_with_status_does_not_mutate(self):
        p = Order("alice", ["bread"])
        q = p.with_status("shipped")
        assert q.status == "shipped"
        assert p.status == "new"
        assert q.items == ["bread"]

    def test_to_dict(self):
        assert Order("alice", ["bread"]).to_dict() == {
            "customer": "alice",
            "items": ["bread"],
            "status": "new",
        }

    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(Order)
