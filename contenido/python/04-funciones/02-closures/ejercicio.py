"""Closures y scopes."""

from collections.abc import Callable


def crear_contador(inicio: int = 0) -> Callable[[], int]:
    """Devolvé una función que, cada vez que se llama, devuelve el siguiente entero
    empezando en `inicio`. Cada contador es independiente.

    Pista: closure + `nonlocal`.

    >>> c = crear_contador(5)
    >>> c(), c()
    (5, 6)
    """
    raise NotImplementedError("TODO")


def multiplicadores(n: int) -> list[Callable[[int], int]]:
    """Lista de `n` funciones: la i-ésima multiplica su argumento por i.

    ¡Cuidado con el late binding!

    >>> [f(10) for f in multiplicadores(3)]
    [0, 10, 20]
    """
    raise NotImplementedError("TODO")


def crear_promediador() -> Callable[[float], float]:
    """Devolvé una función que acumula valores y devuelve el promedio de todos los
    que recibió hasta el momento.

    >>> p = crear_promediador()
    >>> p(10), p(20), p(60)
    (10.0, 15.0, 30.0)
    """
    raise NotImplementedError("TODO")


def crear_limitador(max_llamadas: int) -> Callable[[], bool]:
    """Devolvé una función que devuelve True las primeras `max_llamadas` veces que se
    la llama, y False después (como un rate limiter simple).

    >>> puede = crear_limitador(2)
    >>> puede(), puede(), puede()
    (True, True, False)
    """
    raise NotImplementedError("TODO")
