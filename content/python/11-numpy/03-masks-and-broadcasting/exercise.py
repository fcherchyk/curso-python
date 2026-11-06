"""Boolean masks, fancy indexing and broadcasting. No Python loops."""

import numpy as np


def in_range(v: np.ndarray, low: float, high: float) -> np.ndarray:
    """Elements of v with low <= x <= high (in their original order)."""
    raise NotImplementedError("TODO")


def replace_outliers(v: np.ndarray, limit: float) -> np.ndarray:
    """Copy of v where values with |x| > limit are replaced by 0.
    Don't modify v.
    """
    raise NotImplementedError("TODO")


def top(names: np.ndarray, scores: np.ndarray, k: int) -> list[str]:
    """The names with the k highest scores, from highest to lowest (argsort)."""
    raise NotImplementedError("TODO")


def center_columns(m: np.ndarray) -> np.ndarray:
    """Subtract from each column its mean (broadcasting): every column ends up with mean 0."""
    raise NotImplementedError("TODO")


def share_above_row_mean(m: np.ndarray) -> np.ndarray:
    """For each row, the share of its values that exceed the mean of THAT row.

    Hint: m.mean(axis=1, keepdims=True).
    """
    raise NotImplementedError("TODO")


def multiplication_table(n: int) -> np.ndarray:
    """n x n matrix with (i+1) * (j+1), no loops: column times row (broadcasting)."""
    raise NotImplementedError("TODO")
