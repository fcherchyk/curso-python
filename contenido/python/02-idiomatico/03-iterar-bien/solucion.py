from itertools import pairwise


def indices_de(seq: list[str], valor: str) -> list[int]:
    return [i for i, x in enumerate(seq) if x == valor]


def emparejar(nombres: list[str], notas: list[float]) -> dict[str, float]:
    return dict(zip(nombres, notas, strict=True))


def diferencias(nums: list[int]) -> list[int]:
    return [b - a for a, b in pairwise(nums)]


def numerar_lineas(lineas: list[str], inicio: int = 1) -> list[str]:
    return [f"{n:>3} | {linea}" for n, linea in enumerate(lineas, start=inicio)]
