"""Control de flujo."""


def clasificar_temperatura(t: float) -> str:
    """"frío" si t < 10, "templado" si 10 <= t < 25, "calor" si t >= 25.

    >>> clasificar_temperatura(18)
    'templado'
    """
    raise NotImplementedError("TODO")


def es_primo(n: int) -> bool:
    """¿`n` es primo? Los menores que 2 no lo son.

    Probá con un `for ... else`: buscá un divisor hasta la raíz de n.

    >>> [x for x in range(20) if es_primo(x)]
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    raise NotImplementedError("TODO")


def pasos_collatz(n: int) -> int:
    """Cuántos pasos hacen falta para llegar a 1 aplicando:
    si n es par, n // 2; si es impar, 3 * n + 1.

    Si n <= 0, levantá ValueError.

    >>> pasos_collatz(6)   # 6 3 10 5 16 8 4 2 1
    8
    """
    raise NotImplementedError("TODO")


def fizzbuzz(n: int) -> list[str]:
    """Del 1 al n: "Fizz" si es múltiplo de 3, "Buzz" si de 5, "FizzBuzz" si de ambos,
    y si no, el número como string.

    >>> fizzbuzz(5)
    ['1', '2', 'Fizz', '4', 'Buzz']
    """
    raise NotImplementedError("TODO")
