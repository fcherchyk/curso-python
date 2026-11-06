from collections.abc import Callable


def make_counter(start: int = 0) -> Callable[[], int]:
    current = start - 1

    def next_value() -> int:
        nonlocal current
        current += 1
        return current

    return next_value


def multipliers(n: int) -> list[Callable[[int], int]]:
    # The default freezes the value of i on each iteration (avoids late binding).
    return [lambda x, i=i: x * i for i in range(n)]


def make_averager() -> Callable[[float], float]:
    total = 0.0
    count = 0

    def add(x: float) -> float:
        nonlocal total, count
        total += x
        count += 1
        return total / count

    return add


def make_limiter(max_calls: int) -> Callable[[], bool]:
    remaining = max_calls

    def allowed() -> bool:
        nonlocal remaining
        if remaining <= 0:
            return False
        remaining -= 1
        return True

    return allowed
