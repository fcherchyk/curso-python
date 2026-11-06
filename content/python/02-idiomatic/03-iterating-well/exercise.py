"""Iterar bien.

Prohibido `range(len(...))`: usá enumerate, zip y pairwise.
"""


def indices_de(seq: list[str], valor: str) -> list[int]:
    """Índices donde aparece `valor`.

    >>> indices_de(["a", "b", "a"], "a")
    [0, 2]
    """
    raise NotImplementedError("TODO")


def emparejar(nombres: list[str], notas: list[float]) -> dict[str, float]:
    """Armá un dict nombre -> nota.

    Si las listas tienen distinto largo, tiene que levantar ValueError.

    >>> emparejar(["ana", "beto"], [9.5, 7])
    {'ana': 9.5, 'beto': 7}
    """
    raise NotImplementedError("TODO")


def diferencias(nums: list[int]) -> list[int]:
    """Diferencia entre cada elemento y el anterior.

    >>> diferencias([18, 21, 19, 25])
    [3, -2, 6]
    >>> diferencias([5])
    []
    """
    raise NotImplementedError("TODO")


def numerar_lineas(lineas: list[str], inicio: int = 1) -> list[str]:
    """Anteponé a cada línea su número, alineado a la derecha en 3 caracteres, y ` | `.

    >>> numerar_lineas(["hola", "chau"])
    ['  1 | hola', '  2 | chau']
    >>> numerar_lineas(["x"], inicio=10)
    [' 10 | x']
    """
    raise NotImplementedError("TODO")
