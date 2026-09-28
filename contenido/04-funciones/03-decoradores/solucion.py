import functools
from collections.abc import Callable
from typing import Any


def contar_llamadas(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.llamadas += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.llamadas = 0  # type: ignore[attr-defined]
    return wrapper


def memoizar(func: Callable[..., Any]) -> Callable[..., Any]:
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


MANEJADORES: dict[str, Callable[..., Any]] = {}


def manejador(func: Callable[..., Any]) -> Callable[..., Any]:
    MANEJADORES[func.__name__] = func
    return func


def despachar(evento: str, *args: Any) -> Any:
    try:
        funcion = MANEJADORES[evento]
    except KeyError:
        raise KeyError(f"no hay manejador para el evento {evento!r}") from None
    return funcion(*args)
