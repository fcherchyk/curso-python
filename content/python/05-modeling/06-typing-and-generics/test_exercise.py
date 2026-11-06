import pytest
from exercise import Stack, active_names, first, group_by


class TestStack:
    def test_operations(self):
        s = Stack()
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

    def test_is_generic_with_312_syntax(self):
        assert len(Stack.__type_params__) == 1
        Stack[int]()  # can be parameterized


def test_first():
    assert first([3, 4]) == 3
    assert first(x for x in "abc") == "a"
    assert first([]) is None
    assert first([], default=0) == 0
    assert len(first.__type_params__) == 1


def test_group_by():
    assert group_by(["alice", "bob", "amy"], lambda s: s[0]) == {
        "a": ["alice", "amy"],
        "b": ["bob"],
    }
    assert group_by([1, 2, 3, 4], lambda n: n % 2 == 0) == {False: [1, 3], True: [2, 4]}
    assert len(group_by.__type_params__) == 2


def test_active_names():
    users = [
        {"id": 3, "name": "carol", "active": True},
        {"id": 1, "name": "alice", "active": True},
        {"id": 2, "name": "bob", "active": False},
    ]
    assert active_names(users) == ["alice", "carol"]
