"""Nombres, objetos y mutabilidad."""

from decimal import Decimal  # noqa: F401


def agregar_sin_mutar(xs: list[int], x: int) -> list[int]:
    """Devolvé una lista NUEVA con `x` agregado al final. No modifiques `xs`.

    >>> agregar_sin_mutar([1, 2], 3)
    [1, 2, 3]
    """
    raise NotImplementedError("TODO")


def copiar_matriz(m: list[list[int]]) -> list[list[int]]:
    """Copiá una matriz de forma que modificar la copia NO afecte al original
    (ni las filas ni sus elementos).

    >>> copiar_matriz([[1, 2], [3]])
    [[1, 2], [3]]
    """
    raise NotImplementedError("TODO")


def sumar_precios(precios: list[str]) -> Decimal:
    """Sumá precios que vienen como strings, sin errores de redondeo de float.

    >>> sumar_precios(["0.10", "0.20"])
    Decimal('0.30')
    """
    raise NotImplementedError("TODO")


def repartir(total: int, personas: int) -> tuple[int, int]:
    """Devolvé (cuánto le toca a cada uno, cuánto sobra) con división entera.

    El resultado tiene que cumplir `cada * personas + sobra == total`.

    >>> repartir(17, 5)
    (3, 2)
    """
    raise NotImplementedError("TODO")
