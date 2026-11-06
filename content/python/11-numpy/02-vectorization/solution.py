import numpy as np


def invoice_total(prices: np.ndarray, quantities: np.ndarray, tax: float = 0.21) -> float:
    return round(float((prices * quantities).sum() * (1 + tax)), 2)


def normalize(v: np.ndarray) -> np.ndarray:
    v = v.astype(np.float64)
    spread = v.max() - v.min()
    if spread == 0:
        return np.zeros_like(v)
    return (v - v.min()) / spread


def final_prices(prices: np.ndarray, threshold: float) -> np.ndarray:
    discounted = np.where(prices > threshold, prices * 0.9, prices)
    return np.clip(discounted, 0, 1000).astype(np.float64)


def changes(prices: np.ndarray) -> np.ndarray:
    return prices[1:] / prices[:-1] - 1


def sum_of_squares(v: np.ndarray) -> float:
    return float(np.dot(v, v))
