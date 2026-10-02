"""Listas, tuplas y slicing.

Resolvé cada función con slicing, sin bucles.
"""


def ultimos(xs: list[int], n: int) -> list[int]:
    """Los últimos `n` elementos (o todos, si hay menos). Con n=0, lista vacía.

    >>> ultimos([1, 2, 3, 4], 2)
    [3, 4]
    """
    raise NotImplementedError("TODO")


def rotar(xs: list[int], k: int) -> list[int]:
    """Rotá la lista `k` posiciones a la izquierda. `k` puede ser mayor que el largo.

    >>> rotar([1, 2, 3, 4, 5], 2)
    [3, 4, 5, 1, 2]
    >>> rotar([1, 2, 3], 4)
    [2, 3, 1]
    """
    raise NotImplementedError("TODO")


def es_palindromo(texto: str) -> bool:
    """¿Se lee igual al derecho y al revés? Ignorá mayúsculas y todo lo que no sea
    letra o número.

    >>> es_palindromo("Anita lava la tina")
    True
    """
    raise NotImplementedError("TODO")


def intercalar(a: list[int], b: list[int]) -> list[int]:
    """Intercalá dos listas del mismo largo: a0, b0, a1, b1, ...

    Pista: se puede asignar a un slice con paso: `res[::2] = a`.

    >>> intercalar([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    raise NotImplementedError("TODO")
