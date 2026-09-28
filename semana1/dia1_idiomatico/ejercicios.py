"""Día 1 — Python idiomático.

Completá cada función reemplazando el `raise NotImplementedError`.
Leé primero `leccion.md` y corré los tests con:

    uv run pytest semana1/dia1_idiomatico
"""

import re
from collections import Counter, defaultdict
from urllib.parse import urlencode


def pares_al_cuadrado(nums: list[int]) -> list[int]:
    """Devolvé el cuadrado de cada número par, en el mismo orden.

    Pista: una sola list comprehension con `if`.

    >>> pares_al_cuadrado([1, 2, 3, 4])
    [4, 16]
    """
    return [(x*x) for x  in nums if x % 2 == 0]


def aplanar(matriz: list[list[int]]) -> list[int]:
    """Aplaná una lista de listas (un solo nivel).

    Pista: comprehension anidada; el orden de los `for` es el mismo que
    escribirías con bucles anidados.

    >>> aplanar([[1, 2], [3], []])
    [1, 2, 3]
    """
    return [x for fila in matriz for x in fila]

def invertir_dict(d: dict[str, int]) -> dict[int, str]:
    """Invertí claves y valores (asumí valores únicos).

    Pista: dict comprehension + `.items()`.

    >>> invertir_dict({"a": 1, "b": 2})
    {1: 'a', 2: 'b'}
    """
    return {v:k for k,v in d.items()}


def agrupar_por_inicial(palabras: list[str]) -> dict[str, list[str]]:
    """Agrupá palabras por su primera letra en minúscula, respetando el orden.

    Ignorá strings vacíos.

    Pista: `collections.defaultdict(list)` o `dict.setdefault`.

    >>> agrupar_por_inicial(["Ana", "auto", "Beto"])
    {'a': ['Ana', 'auto'], 'b': ['Beto']}
    """
    return {letra.lower(): [p for p in palabras if p and p[0].lower() == letra.lower()] for letra in set(p[0] for p in palabras if p)}


def primero_y_resto(seq: list[int]) -> tuple[int, list[int]]:
    """Devolvé (primer elemento, lista con el resto).

    Si la secuencia está vacía, levantá ValueError.

    Pista: desempaquetado extendido `a, *b = ...`.
    """
    return seq[0], seq[1:] if seq else ValueError("La secuencia está vacía")


def indices_de(seq: list[str], valor: str) -> list[int]:
    """Índices donde aparece `valor`.

    Pista: `enumerate`, nunca `range(len(...))`.

    >>> indices_de(["a", "b", "a"], "a")
    [0, 2]
    """
    raise NotImplementedError("TODO")


def emparejar(nombres: list[str], notas: list[float]) -> dict[str, float]:
    """Armá un dict nombre -> nota.

    Si las listas tienen distinto largo, tiene que levantar ValueError.

    Pista: `zip(..., strict=True)` (3.10+) ya hace eso por vos.
    """
    raise NotImplementedError("TODO")


def top_palabras(texto: str, n: int) -> list[tuple[str, int]]:
    """Las `n` palabras más frecuentes (en minúscula) con su cantidad.

    Una "palabra" es una secuencia de caracteres `\\w`. Ante empates, gana la
    que apareció primero en el texto.

    Pista: `re.findall` + `collections.Counter.most_common`.

    >>> top_palabras("Hola hola chau", 1)
    [('hola', 2)]
    """
    raise NotImplementedError("TODO")


def ordenar_personas(personas: list[dict[str, str | int]]) -> list[str]:
    """Devolvé los nombres ordenados por edad descendente y, a igual edad,
    por nombre ascendente.

    Cada persona es `{"nombre": str, "edad": int}`.

    Pista: `sorted(..., key=lambda p: (...))` con una tupla como clave.
    """
    raise NotImplementedError("TODO")


def construir_url(host: str, *segmentos: str, https: bool = True, **query: str | int) -> str:
    """Construí una URL.

    - `segmentos` son partes del path (posicionales variables).
    - `https` es keyword-only (ya está en la firma: va después de `*segmentos`).
    - `query` son parámetros del querystring, en el orden recibido.

    >>> construir_url("api.com", "v1", "users", page=2)
    'https://api.com/v1/users?page=2'
    >>> construir_url("api.com", https=False)
    'http://api.com/'

    Pista: `urllib.parse.urlencode`.
    """
    raise NotImplementedError("TODO")


def fusionar_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    """Fusioná diccionarios: los de la derecha pisan a los de la izquierda.

    No modifiques `base`.

    Pista: el operador `|` de dicts (3.9+).
    """
    raise NotImplementedError("TODO")
