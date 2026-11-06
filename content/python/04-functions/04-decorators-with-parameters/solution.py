import functools
import warnings
from collections.abc import Callable
from typing import Any

Decorator = Callable[[Callable[..., Any]], Callable[..., Any]]


def repeat(n: int) -> Decorator:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> list[Any]:
            return [func(*args, **kwargs) for _ in range(n)]

        return wrapper

    return decorator


def retry(
    times: int, exceptions: tuple[type[BaseException], ...] = (Exception,)
) -> Decorator:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
            raise AssertionError("unreachable")

        return wrapper

    return decorator


def clamp(minimum: float, maximum: float) -> Decorator:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> float:
            return max(minimum, min(maximum, func(*args, **kwargs)))

        return wrapper

    return decorator


def deprecated(func: Callable[..., Any] | None = None, *, replacement: str | None = None) -> Any:
    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            message = f"{f.__name__} is deprecated"
            if replacement:
                message += f"; use {replacement}"
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return f(*args, **kwargs)

        return wrapper

    if func is not None:  # used as @deprecated, without parentheses
        return decorator(func)
    return decorator
