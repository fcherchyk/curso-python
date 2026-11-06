"""Máscaras booleanas, fancy indexing y broadcasting. Sin bucles de Python."""

import numpy as np


def en_rango(v: np.ndarray, minimo: float, maximo: float) -> np.ndarray:
    """Elementos de v con minimo <= x <= maximo (en su orden original)."""
    raise NotImplementedError("TODO")


def reemplazar_atipicos(v: np.ndarray, limite: float) -> np.ndarray:
    """Copia de v donde los valores con |x| > limite se reemplazan por 0.
    No modifiques v.
    """
    raise NotImplementedError("TODO")


def mejores(nombres: np.ndarray, puntajes: np.ndarray, k: int) -> list[str]:
    """Los nombres de los k puntajes más altos, del mayor al menor (argsort)."""
    raise NotImplementedError("TODO")


def centrar_columnas(m: np.ndarray) -> np.ndarray:
    """Restá a cada columna su promedio (broadcasting): cada columna queda con media 0."""
    raise NotImplementedError("TODO")


def proporcion_sobre_promedio_por_fila(m: np.ndarray) -> np.ndarray:
    """Para cada fila, la proporción de sus valores que superan el promedio de ESA fila.

    Pista: m.mean(axis=1, keepdims=True).
    """
    raise NotImplementedError("TODO")


def tabla_de_multiplicar(n: int) -> np.ndarray:
    """Matriz n x n con (i+1) * (j+1), sin bucles: columna por fila (broadcasting)."""
    raise NotImplementedError("TODO")
