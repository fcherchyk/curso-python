import importlib
import sys
from importlib.metadata import PackageNotFoundError, version
from types import ModuleType
from typing import Any


def importar(ruta: str) -> Any:
    separador = ":" if ":" in ruta else "."
    nombre_modulo, _, atributo = ruta.rpartition(separador)
    return getattr(importlib.import_module(nombre_modulo), atributo)


def api_publica(modulo: ModuleType) -> list[str]:
    nombres = getattr(modulo, "__all__", None)
    if nombres is None:
        nombres = [n for n in vars(modulo) if not n.startswith("_")]
    return sorted(nombres)


def version_instalada(paquete: str) -> str | None:
    try:
        return version(paquete)
    except PackageNotFoundError:
        return None


def main(argv: list[str]) -> int:
    if not argv:
        print("uso: saludar NOMBRE...")
        return 2
    for nombre in argv:
        print(f"Hola, {nombre}!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
