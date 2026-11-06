from exercise import domains, flatten, invert_dict, squares_of_evens


def test_squares_of_evens():
    assert squares_of_evens([1, 2, 3, 4, 6]) == [4, 16, 36]


def test_squares_of_evens_empty():
    assert squares_of_evens([]) == []
    assert squares_of_evens([1, 3, 5]) == []


def test_flatten():
    assert flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]


def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert_dict({}) == {}


def test_domains():
    emails = ["alice@Gmail.com", "bob@gmail.com", "x@mit.edu", "no-at-sign"]
    assert domains(emails) == {"gmail.com", "mit.edu"}


def test_domains_returns_set():
    assert isinstance(domains(["a@b.c"]), set)
