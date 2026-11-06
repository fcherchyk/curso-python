import numpy as np


def tablero(filas: int, columnas: int) -> np.ndarray:
    return np.arange(1, filas * columnas + 1, dtype=np.int64).reshape(filas, columnas)


def puntos(inicio: float, fin: float, cantidad: int) -> np.ndarray:
    return np.linspace(inicio, fin, cantidad)


def bordes(m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return m[:, 0], m[-1, :], np.diag(m)


def normalizar_copia(v: np.ndarray) -> np.ndarray:
    # astype crea una copia nueva: v (y el array del que es vista) no se tocan.
    return v.astype(np.float64) / v.max()


def poner_en_cero_el_medio(v: np.ndarray) -> None:
    v[1:-1] = 0
