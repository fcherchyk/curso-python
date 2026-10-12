"""Arrays y dtypes. Usá funciones de NumPy, sin bucles de Python."""

import numpy as np


def tablero(filas: int, columnas: int) -> np.ndarray:
    """Matriz de `filas` x `columnas` con los números 1, 2, 3, ... por filas, de tipo int64.

    >>> tablero(2, 3)
    array([[1, 2, 3],
           [4, 5, 6]])
    """
    raise NotImplementedError("TODO")


def puntos(inicio: float, fin: float, cantidad: int) -> np.ndarray:
    """`cantidad` puntos equiespaciados entre inicio y fin, ambos incluidos (float64)."""
    raise NotImplementedError("TODO")


def bordes(m: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Devolvé (primera columna, última fila, diagonal principal) de una matriz.

    Pista: m[:, 0], m[-1, :] y np.diag.
    """
    raise NotImplementedError("TODO")


def normalizar_copia(v: np.ndarray) -> np.ndarray:
    """Devolvé v dividido por su máximo, como float64, SIN modificar v
    (aunque v sea una vista de otro array).
    """
    raise NotImplementedError("TODO")


def poner_en_cero_el_medio(v: np.ndarray) -> None:
    """Poné en 0 los elementos de v desde el índice 1 hasta el anteúltimo (inclusive),
    modificando v EN EL LUGAR (asignando a un slice).
    """
    raise NotImplementedError("TODO")
