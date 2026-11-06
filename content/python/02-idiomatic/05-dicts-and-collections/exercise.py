"""Dicts, defaultdict y Counter."""

import re  # noqa: F401
from collections import Counter, defaultdict  # noqa: F401


def agrupar_por_inicial(palabras: list[str]) -> dict[str, list[str]]:
    """Agrupá palabras por su primera letra en minúscula, respetando el orden.

    Ignorá los strings vacíos. Devolvé un `dict` común (no un defaultdict).

    >>> agrupar_por_inicial(["Ana", "auto", "Beto"])
    {'a': ['Ana', 'auto'], 'b': ['Beto']}
    """
    raise NotImplementedError("TODO")


def top_palabras(texto: str, n: int) -> list[tuple[str, int]]:
    """Las `n` palabras más frecuentes (en minúscula) con su cantidad.

    Una "palabra" es una secuencia de caracteres `\\w`. Ante empates, gana la
    que apareció primero en el texto.

    Pista: `re.findall` + `Counter.most_common`.

    >>> top_palabras("Hola hola chau", 1)
    [('hola', 2)]
    """
    raise NotImplementedError("TODO")


def invertir_agrupando(d: dict[str, int]) -> dict[int, list[str]]:
    """Invertí el dict: cada valor pasa a ser clave, con la lista de claves originales.

    >>> invertir_agrupando({"ana": 9, "beto": 7, "caro": 9})
    {9: ['ana', 'caro'], 7: ['beto']}
    """
    raise NotImplementedError("TODO")


def puede_formar(palabra: str, letras: str) -> bool:
    """¿Se puede escribir `palabra` usando cada letra de `letras` como máximo una vez?

    Distinguí mayúsculas de minúsculas tal cual vienen.

    Pista: resta de `Counter`.

    >>> puede_formar("sol", "losa")
    True
    >>> puede_formar("oso", "sol")
    False
    """
    raise NotImplementedError("TODO")
