import numpy as np


def grid(rows: int, columns: int) -> np.ndarray:
    return np.arange(1, rows * columns + 1, dtype=np.int64).reshape(rows, columns)


def points(start: float, stop: float, count: int) -> np.ndarray:
    return np.linspace(start, stop, count)


def edges(m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return m[:, 0], m[-1, :], np.diag(m)


def normalized_copy(v: np.ndarray) -> np.ndarray:
    # astype creates a new copy: v (and the array it is a view of) stay untouched.
    return v.astype(np.float64) / v.max()


def zero_the_middle(v: np.ndarray) -> None:
    v[1:-1] = 0
