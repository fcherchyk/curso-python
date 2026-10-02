"""Comprehensions.

Completá cada función reemplazando el `raise NotImplementedError`.
Todas se resuelven con una sola comprehension.
"""


def pares_al_cuadrado(nums: list[int]) -> list[int]:
    """Devolvé el cuadrado de cada número par, en el mismo orden.

    >>> pares_al_cuadrado([1, 2, 3, 4])
    [4, 16]
    """
    raise NotImplementedError("TODO")


def aplanar(matriz: list[list[int]]) -> list[int]:
    """Aplaná una lista de listas (un solo nivel).

    Pista: el orden de los `for` es el mismo que con bucles anidados.

    >>> aplanar([[1, 2], [3], []])
    [1, 2, 3]
    """
    raise NotImplementedError("TODO")


def invertir_dict(d: dict[str, int]) -> dict[int, str]:
    """Invertí claves y valores (asumí que los valores son únicos).

    >>> invertir_dict({"a": 1, "b": 2})
    {1: 'a', 2: 'b'}
    """
    raise NotImplementedError("TODO")


def dominios(emails: list[str]) -> set[str]:
    """Devolvé el conjunto de dominios (lo que está después de la `@`), en minúscula.

    Ignorá los strings que no tengan `@`.

    >>> sorted(dominios(["ana@Gmail.com", "beto@gmail.com", "x@uba.ar", "sin-arroba"]))
    ['gmail.com', 'uba.ar']
    """
    raise NotImplementedError("TODO")
