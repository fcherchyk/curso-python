"""Vectorización. Nada de bucles `for` ni comprehensions: solo operaciones de NumPy."""

import numpy as np


def total_factura(precios: np.ndarray, cantidades: np.ndarray, iva: float = 0.21) -> float:
    """Suma de precio * cantidad, con IVA, redondeada a 2 decimales."""
    raise NotImplementedError("TODO")


def normalizar(v: np.ndarray) -> np.ndarray:
    """Escalá v al rango [0, 1]: (v - mín) / (máx - mín).
    Si todos los valores son iguales, devolvé un array de ceros (float).
    """
    raise NotImplementedError("TODO")


def precios_finales(precios: np.ndarray, umbral: float) -> np.ndarray:
    """10 % de descuento a los precios MAYORES al umbral; después, acotá todo al
    rango [0, 1000] (np.clip). Devolvé floats.
    """
    raise NotImplementedError("TODO")


def variaciones(precios: np.ndarray) -> np.ndarray:
    """Variación relativa de cada precio respecto del anterior (largo n-1).

    >>> variaciones(np.array([100, 110, 99]))
    array([ 0.1, -0.1])
    """
    raise NotImplementedError("TODO")


def suma_de_cuadrados(v: np.ndarray) -> float:
    """Suma de los cuadrados de v. Tiene que ser MUCHO más rápida que un bucle de Python."""
    raise NotImplementedError("TODO")
