"""uv y pyproject.toml: leer la configuración de un proyecto."""

import re  # noqa: F401
import tomllib  # noqa: F401


def nombre_de_paquete(especificador: str) -> str:
    """Nombre del paquete de un especificador de dependencia, sin extras ni versiones,
    en minúscula.

    >>> nombre_de_paquete("httpx[http2]>=0.27")
    'httpx'
    >>> nombre_de_paquete("Pydantic >=2,<3")
    'pydantic'

    Pista: el nombre son letras, números, `-`, `_` y `.` desde el principio.
    """
    raise NotImplementedError("TODO")


def dependencias(texto_pyproject: str) -> list[str]:
    """Nombres de las dependencias de ejecución (`[project] dependencies`), ordenados.
    Sin la sección, lista vacía.
    """
    raise NotImplementedError("TODO")


def grupos(texto_pyproject: str) -> dict[str, list[str]]:
    """Cada grupo de `[dependency-groups]` con los nombres de sus paquetes (en el orden
    en que aparecen).
    """
    raise NotImplementedError("TODO")


def python_minimo(texto_pyproject: str) -> tuple[int, int] | None:
    """Versión mínima de Python de `requires-python` (solo se usa la forma ">=X.Y"),
    como tupla. None si no está declarada.

    >>> python_minimo('[project]\\nrequires-python = ">=3.12"')
    (3, 12)
    """
    raise NotImplementedError("TODO")
