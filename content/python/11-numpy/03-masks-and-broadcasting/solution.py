import numpy as np


def in_range(v: np.ndarray, low: float, high: float) -> np.ndarray:
    return v[(v >= low) & (v <= high)]


def replace_outliers(v: np.ndarray, limit: float) -> np.ndarray:
    return np.where(np.abs(v) > limit, 0, v)


def top(names: np.ndarray, scores: np.ndarray, k: int) -> list[str]:
    order = np.argsort(scores)[::-1][:k]  # positions from highest to lowest
    return names[order].tolist()


def center_columns(m: np.ndarray) -> np.ndarray:
    return m - m.mean(axis=0)


def share_above_row_mean(m: np.ndarray) -> np.ndarray:
    return (m > m.mean(axis=1, keepdims=True)).mean(axis=1)


def multiplication_table(n: int) -> np.ndarray:
    a = np.arange(1, n + 1)
    return a[:, None] * a[None, :]
