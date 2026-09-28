def pares_al_cuadrado(nums: list[int]) -> list[int]:
    return [n * n for n in nums if n % 2 == 0]


def aplanar(matriz: list[list[int]]) -> list[int]:
    return [x for fila in matriz for x in fila]


def invertir_dict(d: dict[str, int]) -> dict[int, str]:
    return {v: k for k, v in d.items()}


def dominios(emails: list[str]) -> set[str]:
    # partition no falla si no hay "@": devuelve el separador vacío.
    return {e.partition("@")[2].lower() for e in emails if "@" in e}
