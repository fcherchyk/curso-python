import functools
import warnings
from collections.abc import Callable
from typing import Any

Decorador = Callable[[Callable[..., Any]], Callable[..., Any]]


def repetir(n: int) -> Decorador:
    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
            return [func(*args, **kwargs) for _ in range(n)]

        return wrapper

    return decorador


def reintentar(
    veces: int, excepciones: tuple[type[BaseException], ...] = (Exception,)
) -> Decorador:
    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except excepciones:
                    if intento == veces:
                        raise
            raise AssertionError("inalcanzable")

        return wrapper

    return decorador


def acotar(minimo: float, maximo: float) -> Decorador:
    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            return max(minimo, min(maximo, func(*args, **kwargs)))

        return wrapper

    return decorador


def deprecado(func: Callable[..., Any] | None = None, *, reemplazo: str | None = None) -> Any:
    def decorador(f: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            mensaje = f"{f.__name__} está deprecada"
            if reemplazo:
                mensaje += f"; usá {reemplazo}"
            warnings.warn(mensaje, DeprecationWarning, stacklevel=2)
            return f(*args, **kwargs)

        return wrapper

    if func is not None:  # usado como @deprecado, sin paréntesis
        return decorador(func)
    return decorador
