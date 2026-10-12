import numpy as np


def en_rango(v: np.ndarray, minimo: float, maximo: float) -> np.ndarray:
    return v[(v >= minimo) & (v <= maximo)]


def reemplazar_atipicos(v: np.ndarray, limite: float) -> np.ndarray:
    return np.where(np.abs(v) > limite, 0, v)


def mejores(nombres: np.ndarray, puntajes: np.ndarray, k: int) -> list[str]:
    orden = np.argsort(puntajes)[::-1][:k]  # posiciones de mayor a menor
    return nombres[orden].tolist()


def centrar_columnas(m: np.ndarray) -> np.ndarray:
    return m - m.mean(axis=0)


def proporcion_sobre_promedio_por_fila(m: np.ndarray) -> np.ndarray:
    return (m > m.mean(axis=1, keepdims=True)).mean(axis=1)


def tabla_de_multiplicar(n: int) -> np.ndarray:
    a = np.arange(1, n + 1)
    return a[:, None] * a[None, :]
