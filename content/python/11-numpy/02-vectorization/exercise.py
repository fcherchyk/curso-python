"""Vectorization. No `for` loops or comprehensions: NumPy operations only."""

import numpy as np


def invoice_total(prices: np.ndarray, quantities: np.ndarray, tax: float = 0.21) -> float:
    """Sum of price * quantity, with tax, rounded to 2 decimals."""
    raise NotImplementedError("TODO")


def normalize(v: np.ndarray) -> np.ndarray:
    """Scale v to the range [0, 1]: (v - min) / (max - min).
    If all the values are equal, return an array of zeros (float).
    """
    raise NotImplementedError("TODO")


def final_prices(prices: np.ndarray, threshold: float) -> np.ndarray:
    """Apply a 10% discount to prices GREATER than the threshold; then clamp everything to the
    range [0, 1000] (np.clip). Return floats.
    """
    raise NotImplementedError("TODO")


def changes(prices: np.ndarray) -> np.ndarray:
    """Relative change of each price with respect to the previous one (length n-1).

    >>> changes(np.array([100, 110, 99]))
    array([ 0.1, -0.1])
    """
    raise NotImplementedError("TODO")


def sum_of_squares(v: np.ndarray) -> float:
    """Sum of the squares of v. It must be MUCH faster than a Python loop."""
    raise NotImplementedError("TODO")
