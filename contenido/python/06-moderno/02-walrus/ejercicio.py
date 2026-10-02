"""El operador walrus `:=`. Usalo en cada función."""

import re  # noqa: F401
from collections.abc import Callable
from typing import IO

PRECIO = re.compile(r"\$\s*(\d+(?:\.\d+)?)")


def leer_en_bloques(archivo: IO[str], tamanio: int) -> list[str]:
    """Leé el archivo en bloques de `tamanio` caracteres hasta el final.

    Pista: `while (bloque := archivo.read(tamanio)):`
    """
    raise NotImplementedError("TODO")


def largos_mayores(palabras: list[str], minimo: int) -> list[int]:
    """Largos de las palabras con largo > minimo, calculando len() UNA vez por palabra."""
    raise NotImplementedError("TODO")


def extraer_precios(lineas: list[str]) -> list[float]:
    """Precios (como float) de las líneas que tienen uno con el formato de `PRECIO`
    ("$ 12.50", "$3"). Las demás se ignoran.

    >>> extraer_precios(["café $ 2.5", "sin precio", "pan $3"])
    [2.5, 3.0]
    """
    raise NotImplementedError("TODO")


def primer_ok(intentos: Callable[[], str | None], maximo: int) -> str | None:
    """Llamá a `intentos()` hasta `maximo` veces y devolvé el primer resultado que no
    sea None (o None si ninguno funcionó).
    """
    raise NotImplementedError("TODO")
