from decimal import Decimal


def agregar_sin_mutar(xs: list[int], x: int) -> list[int]:
    return [*xs, x]  # o xs + [x]


def copiar_matriz(m: list[list[int]]) -> list[list[int]]:
    # Alcanza con copiar cada fila: los int son inmutables.
    return [fila.copy() for fila in m]


def sumar_precios(precios: list[str]) -> Decimal:
    return sum((Decimal(p) for p in precios), Decimal(0))


def repartir(total: int, personas: int) -> tuple[int, int]:
    return divmod(total, personas)
