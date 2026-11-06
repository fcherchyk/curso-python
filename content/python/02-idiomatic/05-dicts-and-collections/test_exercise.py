from exercise import can_form, group_by_initial, invert_grouping, top_words


def test_group_by_initial():
    assert group_by_initial(["Alice", "apple", "", "Bob", "boat", "car"]) == {
        "a": ["Alice", "apple"],
        "b": ["Bob", "boat"],
        "c": ["car"],
    }


def test_group_returns_plain_dict():
    assert type(group_by_initial(["x"])) is dict


def test_top_words():
    text = "The dog and the cat. THE dog sleeps; the cat naps."
    assert top_words(text, 3) == [("the", 4), ("dog", 2), ("cat", 2)]


def test_top_words_n_greater_than_total():
    assert top_words("one two", 5) == [("one", 1), ("two", 1)]


def test_invert_grouping():
    assert invert_grouping({"alice": 9, "bob": 7, "carol": 9}) == {
        9: ["alice", "carol"],
        7: ["bob"],
    }
    assert type(invert_grouping({"a": 1})) is dict


def test_can_form():
    assert can_form("tea", "east")
    assert can_form("", "abc")
    assert not can_form("tee", "tea")
    assert not can_form("Tea", "tea")
