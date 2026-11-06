from collections.abc import Callable


def crear_contador(inicio: int = 0) -> Callable[[], int]:
    actual = inicio - 1

    def siguiente() -> int:
        nonlocal actual
        actual += 1
        return actual

    return siguiente


def multiplicadores(n: int) -> list[Callable[[int], int]]:
    # El default congela el valor de i en cada vuelta (evita el late binding).
    return [lambda x, i=i: x * i for i in range(n)]


def crear_promediador() -> Callable[[float], float]:
    total = 0.0
    cantidad = 0

    def agregar(x: float) -> float:
        nonlocal total, cantidad
        total += x
        cantidad += 1
        return total / cantidad

    return agregar


def crear_limitador(max_llamadas: int) -> Callable[[], bool]:
    restantes = max_llamadas

    def puede() -> bool:
        nonlocal restantes
        if restantes <= 0:
            return False
        restantes -= 1
        return True

    return puede
