import math


def classify_temperature(t: float) -> str:
    if t < 10:
        return "cold"
    if t < 25:
        return "mild"
    return "hot"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            break
    else:  # no break: we found no divisors
        return True
    return False


def collatz_steps(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def fizzbuzz(n: int) -> list[str]:
    res = []
    for i in range(1, n + 1):
        text = ("Fizz" if i % 3 == 0 else "") + ("Buzz" if i % 5 == 0 else "")
        res.append(text or str(i))
    return res
