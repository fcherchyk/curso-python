import numpy as np


def resumen_por_columna(m: np.ndarray) -> dict[str, np.ndarray]:
    return {
        "media": np.nanmean(m, axis=0),
        "desvio": np.nanstd(m, axis=0, ddof=1),
        "minimo": np.nanmin(m, axis=0),
        "maximo": np.nanmax(m, axis=0),
    }


def mejor_dia_por_producto(ventas: np.ndarray, dias: np.ndarray) -> list[str]:
    return dias[ventas.argmax(axis=0)].tolist()


def prob_suma_dados(objetivo: int, n: int, semilla: int) -> float:
    rng = np.random.default_rng(semilla)
    sumas = rng.integers(1, 7, size=(n, 2)).sum(axis=1)
    return float((sumas == objetivo).mean())


def intervalo_bootstrap(muestra: np.ndarray, n: int, semilla: int) -> tuple[float, float]:
    rng = np.random.default_rng(semilla)
    medias = rng.choice(muestra, size=(n, len(muestra)), replace=True).mean(axis=1)
    bajo, alto = np.percentile(medias, [2.5, 97.5])
    return float(bajo), float(alto)
