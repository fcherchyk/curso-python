"""Lists, tuples and slicing.

Solve each function with slicing, no loops.
"""


def last_n(xs: list[int], n: int) -> list[int]:
    """The last `n` elements (or all of them, if there are fewer). With n=0, an empty list.

    >>> last_n([1, 2, 3, 4], 2)
    [3, 4]
    """
    raise NotImplementedError("TODO")


def rotate(xs: list[int], k: int) -> list[int]:
    """Rotate the list `k` positions to the left. `k` may be larger than the length.

    >>> rotate([1, 2, 3, 4, 5], 2)
    [3, 4, 5, 1, 2]
    >>> rotate([1, 2, 3], 4)
    [2, 3, 1]
    """
    raise NotImplementedError("TODO")


def is_palindrome(text: str) -> bool:
    """Does it read the same forwards and backwards? Ignore case and anything that
    isn't a letter or a digit.

    >>> is_palindrome("Never odd or even")
    True
    """
    raise NotImplementedError("TODO")


def interleave(a: list[int], b: list[int]) -> list[int]:
    """Interleave two lists of the same length: a0, b0, a1, b1, ...

    Hint: you can assign to a slice with a step: `res[::2] = a`.

    >>> interleave([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    raise NotImplementedError("TODO")
