"""Iterating well.

No `range(len(...))` allowed: use enumerate, zip and pairwise.
"""


def indices_of(seq: list[str], value: str) -> list[int]:
    """Indices where `value` appears.

    >>> indices_of(["a", "b", "a"], "a")
    [0, 2]
    """
    raise NotImplementedError("TODO")


def pair_up(names: list[str], grades: list[float]) -> dict[str, float]:
    """Build a name -> grade dict.

    If the lists have different lengths, it must raise ValueError.

    >>> pair_up(["alice", "bob"], [9.5, 7])
    {'alice': 9.5, 'bob': 7}
    """
    raise NotImplementedError("TODO")


def differences(nums: list[int]) -> list[int]:
    """Difference between each element and the previous one.

    >>> differences([18, 21, 19, 25])
    [3, -2, 6]
    >>> differences([5])
    []
    """
    raise NotImplementedError("TODO")


def number_lines(lines: list[str], start: int = 1) -> list[str]:
    """Prefix each line with its number, right-aligned in 3 characters, and ` | `.

    >>> number_lines(["hello", "bye"])
    ['  1 | hello', '  2 | bye']
    >>> number_lines(["x"], start=10)
    [' 10 | x']
    """
    raise NotImplementedError("TODO")
