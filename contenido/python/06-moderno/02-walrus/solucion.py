import re
from collections.abc import Callable
from typing import IO

PRECIO = re.compile(r"\$\s*(\d+(?:\.\d+)?)")


def leer_en_bloques(archivo: IO[str], tamanio: int) -> list[str]:
    bloques = []
    while bloque := archivo.read(tamanio):
        bloques.append(bloque)
    return bloques


def largos_mayores(palabras: list[str], minimo: int) -> list[int]:
    return [n for p in palabras if (n := len(p)) > minimo]


def extraer_precios(lineas: list[str]) -> list[float]:
    return [float(m[1]) for linea in lineas if (m := PRECIO.search(linea))]


def primer_ok(intentos: Callable[[], str | None], maximo: int) -> str | None:
    for _ in range(maximo):
        if (resultado := intentos()) is not None:
            return resultado
    return None
