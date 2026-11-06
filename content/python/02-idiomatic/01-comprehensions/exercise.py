"""Comprehensions.

Complete each function by replacing the `raise NotImplementedError`.
Each one can be solved with a single comprehension.
"""


def squares_of_evens(nums: list[int]) -> list[int]:
    """Return the square of each even number, in the same order.

    >>> squares_of_evens([1, 2, 3, 4])
    [4, 16]
    """
    raise NotImplementedError("TODO")


def flatten(matrix: list[list[int]]) -> list[int]:
    """Flatten a list of lists (one level only).

    Hint: the `for` clauses go in the same order as nested loops.

    >>> flatten([[1, 2], [3], []])
    [1, 2, 3]
    """
    raise NotImplementedError("TODO")


def invert_dict(d: dict[str, int]) -> dict[int, str]:
    """Swap keys and values (assume the values are unique).

    >>> invert_dict({"a": 1, "b": 2})
    {1: 'a', 2: 'b'}
    """
    raise NotImplementedError("TODO")


def domains(emails: list[str]) -> set[str]:
    """Return the set of domains (whatever comes after the `@`), lowercased.

    Ignore strings that have no `@`.

    >>> sorted(domains(["alice@Gmail.com", "bob@gmail.com", "x@mit.edu", "no-at-sign"]))
    ['gmail.com', 'mit.edu']
    """
    raise NotImplementedError("TODO")
