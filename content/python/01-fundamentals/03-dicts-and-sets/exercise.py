"""Dicts and sets: the essentials.

Don't use `collections` in this chapter: solve it with plain dicts and sets.
"""


def unique_in_order(xs: list[str]) -> list[str]:
    """Elements without repeats, in the order of their first appearance.

    >>> unique_in_order(["b", "a", "b", "c", "a"])
    ['b', 'a', 'c']
    """
    raise NotImplementedError("TODO")


def common(a: list[int], b: list[int]) -> list[int]:
    """Elements present in both lists, without repeats and sorted in ascending order.

    >>> common([3, 1, 2, 3], [3, 4, 1])
    [1, 3]
    """
    raise NotImplementedError("TODO")


def count_chars(text: str) -> dict[str, int]:
    """How many times each character appears, in order of first appearance.

    Hint: `d.get(c, 0) + 1`.

    >>> count_chars("hello all")
    {'h': 1, 'e': 1, 'l': 4, 'o': 1, ' ': 1, 'a': 1}
    """
    raise NotImplementedError("TODO")


def has_duplicates(xs: list[int]) -> bool:
    """Does any element appear more than once?

    >>> has_duplicates([1, 2, 3, 1])
    True
    """
    raise NotImplementedError("TODO")
