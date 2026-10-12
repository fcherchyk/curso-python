"""Agregaciones, estadística y aleatoriedad reproducible. Sin bucles de Python."""

import numpy as np


def resumen_por_columna(m: np.ndarray) -> dict[str, np.ndarray]:
    """{"media", "desvio", "minimo", "maximo"} de cada columna.
    El desvío es MUESTRAL (ddof=1). Ignorá los nan (funciones nan*).
    """
    raise NotImplementedError("TODO")


def mejor_dia_por_producto(ventas: np.ndarray, dias: np.ndarray) -> list[str]:
    """ventas: filas = días, columnas = productos. Para cada producto, el nombre del día
    en que más vendió (argmax por eje + fancy indexing).
    """
    raise NotImplementedError("TODO")


def prob_suma_dados(objetivo: int, n: int, semilla: int) -> float:
    """Probabilidad estimada por Monte Carlo de que la suma de DOS dados sea `objetivo`.
    Simulá n tiradas de una sola vez con np.random.default_rng(semilla).
    """
    raise NotImplementedError("TODO")


def intervalo_bootstrap(muestra: np.ndarray, n: int, semilla: int) -> tuple[float, float]:
    """Intervalo del 95 % para la MEDIA por bootstrap: n remuestreos con reposición del mismo
    tamaño que la muestra (una matriz n x len(muestra)), media por fila y percentiles 2.5 y 97.5.
    """
    raise NotImplementedError("TODO")
