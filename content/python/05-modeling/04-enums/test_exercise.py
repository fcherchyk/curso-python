import json

import pytest
from exercise import Permission, Priority, Status, can, most_urgent


def test_status_is_string():
    assert Status.PENDING == "pending"
    assert Status("in_progress") is Status.IN_PROGRESS
    assert json.dumps({"s": Status.DONE}) == '{"s": "done"}'


def test_status_next():
    assert Status.PENDING.next() is Status.IN_PROGRESS
    assert Status.IN_PROGRESS.next() is Status.DONE
    with pytest.raises(ValueError):
        Status.DONE.next()


def test_status_is_final():
    assert Status.DONE.is_final
    assert not Status.PENDING.is_final


def test_priority_sortable():
    assert Priority.HIGH > Priority.LOW
    assert Priority.MEDIUM == 2


def test_most_urgent():
    tasks = [
        ("a", Priority.LOW),
        ("b", Priority.HIGH),
        ("c", Priority.MEDIUM),
        ("d", Priority.HIGH),
    ]
    assert most_urgent(tasks) == ["b", "d", "c", "a"]


def test_permissions():
    rw = Permission.READ | Permission.WRITE
    assert can(rw, Permission.READ)
    assert can(rw, Permission.READ | Permission.WRITE)
    assert not can(rw, Permission.DELETE)
    assert not can(rw, Permission.ALL)
    assert can(Permission.ALL, Permission.DELETE)
