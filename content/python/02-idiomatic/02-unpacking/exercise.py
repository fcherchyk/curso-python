"""Unpacking.

Solve each function without indexing (`xs[0]`, `xs[-1]`, `xs[1:]`).
"""


def first_and_rest(seq: list[int]) -> tuple[int, list[int]]:
    """Return (first element, list with the rest).

    If the sequence is empty, raise ValueError.

    >>> first_and_rest([1, 2, 3])
    (1, [2, 3])
    """
    raise NotImplementedError("TODO")


def ends(seq: list[int]) -> tuple[int, int]:
    """Return (first, last). With a single element, it's (x, x).

    If the sequence is empty, raise ValueError.

    >>> ends([4, 8, 15, 16])
    (4, 16)
    """
    raise NotImplementedError("TODO")


def sum_points(points: list[tuple[int, int]]) -> tuple[int, int]:
    """Add up a list of (x, y) points component-wise.

    Hint: unpack in the `for`.

    >>> sum_points([(1, 2), (3, 4), (0, -1)])
    (4, 5)
    """
    raise NotImplementedError("TODO")


def merge_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    """Merge dictionaries: the ones on the right overwrite the ones on the left.

    Don't modify `base` or the overrides.

    >>> merge_config({"a": 1, "b": 2}, {"b": 3}, {"c": 4})
    {'a': 1, 'b': 3, 'c': 4}
    """
    raise NotImplementedError("TODO")
