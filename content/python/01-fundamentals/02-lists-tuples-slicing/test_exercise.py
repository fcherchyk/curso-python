from exercise import es_palindromo, intercalar, rotar, ultimos


def test_ultimos():
    assert ultimos([1, 2, 3, 4], 2) == [3, 4]
    assert ultimos([1, 2], 5) == [1, 2]


def test_ultimos_cero():
    assert ultimos([1, 2, 3], 0) == []


def test_rotar():
    assert rotar([1, 2, 3, 4, 5], 2) == [3, 4, 5, 1, 2]
    assert rotar([1, 2, 3], 3) == [1, 2, 3]
    assert rotar([1, 2, 3], 4) == [2, 3, 1]


def test_rotar_vacia():
    assert rotar([], 3) == []


def test_es_palindromo():
    assert es_palindromo("Anita lava la tina")
    assert es_palindromo("A man, a plan, a canal: Panama")
    assert not es_palindromo("python")
    assert es_palindromo("")


def test_intercalar():
    assert intercalar([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert intercalar([], []) == []
