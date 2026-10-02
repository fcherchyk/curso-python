"""Módulos, paquetes e imports."""

import importlib  # noqa: F401
from importlib.metadata import PackageNotFoundError, version  # noqa: F401
from types import ModuleType
from typing import Any


def importar(ruta: str) -> Any:
    """Importá un objeto a partir de un string "paquete.modulo:nombre" o
    "paquete.modulo.nombre" (lo que va después del último `.` o del `:` es el atributo).

    >>> importar("math:sqrt")(16)
    4.0
    >>> importar("os.path.join")("a", "b")
    'a/b'
    """
    raise NotImplementedError("TODO")


def api_publica(modulo: ModuleType) -> list[str]:
    """Nombres públicos de un módulo, ordenados.

    Si el módulo define `__all__`, son esos. Si no, todos los que no empiezan con `_`.
    """
    raise NotImplementedError("TODO")


def version_instalada(paquete: str) -> str | None:
    """Versión instalada del paquete, o None si no está instalado.

    Pista: `importlib.metadata.version`.
    """
    raise NotImplementedError("TODO")


def main(argv: list[str]) -> int:
    """Punto de entrada: imprimí "Hola, NOMBRE!" por cada argumento y devolvé 0.
    Sin argumentos, imprimí "uso: saludar NOMBRE..." y devolvé 2.

    Además, agregá al final del archivo la guarda de `__name__` (ver la lección)
    que llame a `main(sys.argv[1:])` y salga con su resultado.
    """
    raise NotImplementedError("TODO")
