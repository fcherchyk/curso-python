import pytest

from week1.day1_idiomatic.exercises import (
    build_url,
    first_and_rest,
    flatten,
    group_by_initial,
    indices_of,
    invert_dict,
    merge_config,
    pair_up,
    sort_people,
    square_evens,
    top_words,
)


def test_square_evens():
    assert square_evens([1, 2, 3, 4, 6]) == [4, 16, 36]
    assert square_evens([]) == []


def test_flatten():
    assert flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]


def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_group_by_initial():
    assert group_by_initial(["Alice", "apple", "", "Bob", "boat", "cat"]) == {
        "a": ["Alice", "apple"],
        "b": ["Bob", "boat"],
        "c": ["cat"],
    }


def test_group_returns_plain_dict():
    # A defaultdict "leaks" odd behavior to the caller: return a dict.
    assert type(group_by_initial(["x"])) is dict


def test_first_and_rest():
    assert first_and_rest([1, 2, 3]) == (1, [2, 3])
    assert first_and_rest([7]) == (7, [])
    with pytest.raises(ValueError):
        first_and_rest([])


def test_indices_of():
    assert indices_of(["a", "b", "a", "c", "a"], "a") == [0, 2, 4]
    assert indices_of(["a"], "z") == []


def test_pair_up():
    assert pair_up(["alice", "bob"], [9.5, 7]) == {"alice": 9.5, "bob": 7}
    with pytest.raises(ValueError):
        pair_up(["alice"], [1, 2])


def test_top_words():
    text = "The dog and the cat. THE dog sleeps; the cat does not."
    assert top_words(text, 3) == [("the", 4), ("dog", 2), ("cat", 2)]


def test_sort_people():
    people = [
        {"name": "Zoe", "age": 30},
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
    ]
    assert sort_people(people) == ["Bob", "Zoe", "Alice"]


def test_build_url():
    assert build_url("api.com", "v1", "users", page=2, q="x y") == (
        "https://api.com/v1/users?page=2&q=x+y"
    )
    assert build_url("api.com", https=False) == "http://api.com/"


def test_build_url_https_is_keyword_only():
    # "False" as a positional argument is taken as one more segment, not as https.
    assert build_url("a.com", "b", "c").startswith("https://")


def test_merge_config():
    base = {"debug": False, "port": 80}
    res = merge_config(base, {"port": 8080}, {"debug": True, "host": "x"})
    assert res == {"debug": True, "port": 8080, "host": "x"}
    assert base == {"debug": False, "port": 80}, "base must not be mutated"
