import math


def clasificar_temperatura(t: float) -> str:
    if t < 10:
        return "frío"
    if t < 25:
        return "templado"
    return "calor"


def es_primo(n: int) -> bool:
    if n < 2:
        return False
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            break
    else:  # no hubo break: no encontramos divisores
        return True
    return False


def pasos_collatz(n: int) -> int:
    if n <= 0:
        raise ValueError("n tiene que ser positivo")
    pasos = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        pasos += 1
    return pasos


def fizzbuzz(n: int) -> list[str]:
    res = []
    for i in range(1, n + 1):
        texto = ("Fizz" if i % 3 == 0 else "") + ("Buzz" if i % 5 == 0 else "")
        res.append(texto or str(i))
    return res
