import numpy as np


def column_summary(m: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "mean": np.nanmean(m, axis=0),
        "std": np.nanstd(m, axis=0, ddof=1),
        "min": np.nanmin(m, axis=0),
        "max": np.nanmax(m, axis=0),
    }


def best_day_per_product(sales: np.ndarray, days: np.ndarray) -> list[str]:
    return days[sales.argmax(axis=0)].tolist()


def dice_sum_prob(target: int, n: int, seed: int) -> float:
    rng = np.random.default_rng(seed)
    sums = rng.integers(1, 7, size=(n, 2)).sum(axis=1)
    return float((sums == target).mean())


def bootstrap_interval(sample: np.ndarray, n: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    means = rng.choice(sample, size=(n, len(sample)), replace=True).mean(axis=1)
    low, high = np.percentile(means, [2.5, 97.5])
    return float(low), float(high)
