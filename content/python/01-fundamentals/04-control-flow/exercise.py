"""Control flow."""


def classify_temperature(t: float) -> str:
    """"cold" if t < 10, "mild" if 10 <= t < 25, "hot" if t >= 25.

    >>> classify_temperature(18)
    'mild'
    """
    raise NotImplementedError("TODO")


def is_prime(n: int) -> bool:
    """Is `n` prime? Numbers below 2 are not.

    Try a `for ... else`: look for a divisor up to the square root of n.

    >>> [x for x in range(20) if is_prime(x)]
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    raise NotImplementedError("TODO")


def collatz_steps(n: int) -> int:
    """How many steps it takes to reach 1 by applying:
    if n is even, n // 2; if it's odd, 3 * n + 1.

    If n <= 0, raise ValueError.

    >>> collatz_steps(6)   # 6 3 10 5 16 8 4 2 1
    8
    """
    raise NotImplementedError("TODO")


def fizzbuzz(n: int) -> list[str]:
    """From 1 to n: "Fizz" if it's a multiple of 3, "Buzz" if of 5, "FizzBuzz" if of both,
    and otherwise the number as a string.

    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    """
    raise NotImplementedError("TODO")
