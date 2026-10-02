"""Desempaquetado.

Resolvé cada función sin usar índices (`xs[0]`, `xs[-1]`, `xs[1:]`).
"""


def primero_y_resto(seq: list[int]) -> tuple[int, list[int]]:
    """Devolvé (primer elemento, lista con el resto).

    Si la secuencia está vacía, levantá ValueError.

    >>> primero_y_resto([1, 2, 3])
    (1, [2, 3])
    """
    raise NotImplementedError("TODO")


def extremos(seq: list[int]) -> tuple[int, int]:
    """Devolvé (primero, último). Con un solo elemento, es (x, x).

    Si la secuencia está vacía, levantá ValueError.

    >>> extremos([4, 8, 15, 16])
    (4, 16)
    """
    raise NotImplementedError("TODO")


def sumar_puntos(puntos: list[tuple[int, int]]) -> tuple[int, int]:
    """Sumá una lista de puntos (x, y) componente a componente.

    Pista: desempaquetá en el `for`.

    >>> sumar_puntos([(1, 2), (3, 4), (0, -1)])
    (4, 5)
    """
    raise NotImplementedError("TODO")


def fusionar_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    """Fusioná diccionarios: los de la derecha pisan a los de la izquierda.

    No modifiques `base` ni los overrides.

    >>> fusionar_config({"a": 1, "b": 2}, {"b": 3}, {"c": 4})
    {'a': 1, 'b': 3, 'c': 4}
    """
    raise NotImplementedError("TODO")
