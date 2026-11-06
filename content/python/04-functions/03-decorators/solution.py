import functools
from collections.abc import Callable
from typing import Any


def count_calls(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.calls += 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper


def memoize(func: Callable[..., Any]) -> Callable[..., Any]:
    cache: dict[tuple[Any, ...], Any] = {}

    @functools.wraps(func)
    def wrapper(*args: Any) -> Any:
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # type: ignore[attr-defined]
    return wrapper


HANDLERS: dict[str, Callable[..., Any]] = {}


def handler(func: Callable[..., Any]) -> Callable[..., Any]:
    HANDLERS[func.__name__] = func
    return func


def dispatch(event: str, *args: Any) -> Any:
    try:
        function = HANDLERS[event]
    except KeyError:
        raise KeyError(f"no handler for event {event!r}") from None
    return function(*args)
