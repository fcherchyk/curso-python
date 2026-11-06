import numpy as np


def total_factura(precios: np.ndarray, cantidades: np.ndarray, iva: float = 0.21) -> float:
    return round(float((precios * cantidades).sum() * (1 + iva)), 2)


def normalizar(v: np.ndarray) -> np.ndarray:
    v = v.astype(np.float64)
    rango = v.max() - v.min()
    if rango == 0:
        return np.zeros_like(v)
    return (v - v.min()) / rango


def precios_finales(precios: np.ndarray, umbral: float) -> np.ndarray:
    con_descuento = np.where(precios > umbral, precios * 0.9, precios)
    return np.clip(con_descuento, 0, 1000).astype(np.float64)


def variaciones(precios: np.ndarray) -> np.ndarray:
    return precios[1:] / precios[:-1] - 1


def suma_de_cuadrados(v: np.ndarray) -> float:
    return float(np.dot(v, v))
