from collections.abc import Iterable, Iterator
from itertools import count


def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def lineas_utiles(lineas: Iterable[str]) -> Iterator[str]:
    for linea in lineas:
        linea = linea.strip()
        if linea and not linea.startswith("#"):
            yield linea


def aplanar_profundo(anidado: Iterable[object]) -> Iterator[object]:
    for x in anidado:
        if isinstance(x, (list, tuple)):
            yield from aplanar_profundo(x)
        else:
            yield x


def rango_decimal(inicio: float, fin: float, paso: float) -> Iterator[float]:
    # Como es un generador, esta validación corre recién en el primer next().
    if paso <= 0:
        raise ValueError("paso tiene que ser positivo")
    for i in count():
        valor = round(inicio + i * paso, 10)
        if valor >= fin:
            return
        yield valor
