from exercise import common, count_chars, has_duplicates, unique_in_order


def test_unique_in_order():
    assert unique_in_order(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]
    assert unique_in_order([]) == []


def test_common():
    assert common([3, 1, 2, 3], [3, 4, 1]) == [1, 3]
    assert common([1, 2], [3]) == []


def test_count_chars():
    assert count_chars("hello all") == {"h": 1, "e": 1, "l": 4, "o": 1, " ": 1, "a": 1}
    assert list(count_chars("ba")) == ["b", "a"], "it must preserve the order"
    assert count_chars("") == {}


def test_has_duplicates():
    assert has_duplicates([1, 2, 3, 1])
    assert not has_duplicates([1, 2, 3])
    assert not has_duplicates([])
