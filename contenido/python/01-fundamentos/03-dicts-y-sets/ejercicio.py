"""Dicts y sets: lo esencial.

No uses `collections` en este capítulo: resolvelo con dicts y sets comunes.
"""


def unicos_en_orden(xs: list[str]) -> list[str]:
    """Elementos sin repetir, en el orden de su primera aparición.

    >>> unicos_en_orden(["b", "a", "b", "c", "a"])
    ['b', 'a', 'c']
    """
    raise NotImplementedError("TODO")


def comunes(a: list[int], b: list[int]) -> list[int]:
    """Elementos que están en las dos listas, sin repetir y ordenados de menor a mayor.

    >>> comunes([3, 1, 2, 3], [3, 4, 1])
    [1, 3]
    """
    raise NotImplementedError("TODO")


def contar_caracteres(texto: str) -> dict[str, int]:
    """Cuántas veces aparece cada carácter, en orden de primera aparición.

    Pista: `d.get(c, 0) + 1`.

    >>> contar_caracteres("hola ola")
    {'h': 1, 'o': 2, 'l': 2, 'a': 2, ' ': 1}
    """
    raise NotImplementedError("TODO")


def hay_duplicados(xs: list[int]) -> bool:
    """¿Algún elemento aparece más de una vez?

    >>> hay_duplicados([1, 2, 3, 1])
    True
    """
    raise NotImplementedError("TODO")
