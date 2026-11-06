"""Arrays and dtypes. Use NumPy functions, no Python loops."""

import numpy as np


def grid(rows: int, columns: int) -> np.ndarray:
    """A `rows` x `columns` matrix with the numbers 1, 2, 3, ... filled row by row, of type int64.

    >>> grid(2, 3)
    array([[1, 2, 3],
           [4, 5, 6]])
    """
    raise NotImplementedError("TODO")


def points(start: float, stop: float, count: int) -> np.ndarray:
    """`count` evenly spaced points between start and stop, both included (float64)."""
    raise NotImplementedError("TODO")


def edges(m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (first column, last row, main diagonal) of a matrix.

    Hint: m[:, 0], m[-1, :] and np.diag.
    """
    raise NotImplementedError("TODO")


def normalized_copy(v: np.ndarray) -> np.ndarray:
    """Return v divided by its maximum, as float64, WITHOUT modifying v
    (even if v is a view of another array).
    """
    raise NotImplementedError("TODO")


def zero_the_middle(v: np.ndarray) -> None:
    """Set the elements of v from index 1 through the second-to-last (inclusive) to 0,
    modifying v IN PLACE (by assigning to a slice).
    """
    raise NotImplementedError("TODO")
