def primero_y_resto(seq: list[int]) -> tuple[int, list[int]]:
    if not seq:
        raise ValueError("secuencia vacía")
    primero, *resto = seq
    return primero, resto


def extremos(seq: list[int]) -> tuple[int, int]:
    if not seq:
        raise ValueError("secuencia vacía")
    # Con un solo elemento, los dos patrones toman ese mismo valor.
    primero, *_ = seq
    *_, ultimo = seq
    return primero, ultimo


def sumar_puntos(puntos: list[tuple[int, int]]) -> tuple[int, int]:
    sx = sy = 0
    for x, y in puntos:
        sx += x
        sy += y
    return sx, sy


def fusionar_config(base: dict[str, object], *overrides: dict[str, object]) -> dict[str, object]:
    resultado = dict(base)
    for o in overrides:
        resultado |= o
    return resultado
