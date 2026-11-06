from exercise import interleave, is_palindrome, last_n, rotate


def test_last_n():
    assert last_n([1, 2, 3, 4], 2) == [3, 4]
    assert last_n([1, 2], 5) == [1, 2]


def test_last_n_zero():
    assert last_n([1, 2, 3], 0) == []


def test_rotate():
    assert rotate([1, 2, 3, 4, 5], 2) == [3, 4, 5, 1, 2]
    assert rotate([1, 2, 3], 3) == [1, 2, 3]
    assert rotate([1, 2, 3], 4) == [2, 3, 1]


def test_rotate_empty():
    assert rotate([], 3) == []


def test_is_palindrome():
    assert is_palindrome("Never odd or even")
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert not is_palindrome("python")
    assert is_palindrome("")


def test_interleave():
    assert interleave([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert interleave([], []) == []
