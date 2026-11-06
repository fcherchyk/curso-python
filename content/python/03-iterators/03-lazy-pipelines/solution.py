import itertools
from collections.abc import Iterable, Iterator


def primeros_cuadrados_pares(numeros: Iterable[int], n: int) -> list[int]:
    cuadrados = (x * x for x in numeros)
    pares = (c for c in cuadrados if c % 2 == 0)
    return list(itertools.islice(pares, n))


def en_lotes(iterable: Iterable[int], n: int) -> Iterator[tuple[int, ...]]:
    it = iter(iterable)
    while lote := tuple(itertools.islice(it, n)):
        yield lote


def parsear_accesos(lineas: Iterable[str]) -> Iterator[tuple[str, int, int]]:
    for linea in lineas:
        try:
            ip, _metodo, _ruta, status, bytes_ = linea.split()
            yield ip, int(status), int(bytes_)
        except ValueError:  # cantidad de campos incorrecta o números inválidos
            continue


def bytes_por_status(lineas: Iterable[str]) -> dict[int, int]:
    totales: dict[int, int] = {}
    for _ip, status, bytes_ in parsear_accesos(lineas):
        totales[status] = totales.get(status, 0) + bytes_
    return dict(sorted(totales.items()))
