"""ExceptionGroup, except* y notas."""

from collections.abc import Callable
from typing import Any


def validar_usuario(datos: dict[str, Any]) -> None:
    """Validá TODOS los campos y reportá todos los errores juntos.

    - "nombre": str no vacío     -> si no, ValueError("nombre")
    - "edad": int                -> si no es int, TypeError("edad")
    - "edad" >= 0                -> si es negativa, ValueError("edad")
    - "email": contiene "@"      -> si no, ValueError("email")

    Si hay errores, levantá `ExceptionGroup("usuario inválido", errores)`.
    Los campos faltantes cuentan como inválidos.
    """
    raise NotImplementedError("TODO")


def clasificar_errores(datos: dict[str, Any]) -> dict[str, list[str]]:
    """Llamá a `validar_usuario` y clasificá los errores con `except*`.

    Devolvé {"valor": [...mensajes de ValueError], "tipo": [...de TypeError]}.
    Si no hay errores, las dos listas quedan vacías.
    """
    raise NotImplementedError("TODO")


def ejecutar_todas(tareas: list[Callable[[], Any]]) -> list[Any]:
    """Ejecutá todas las tareas (aunque alguna falle) y devolvé sus resultados en orden.

    Si alguna levantó una excepción (Exception), al final levantá
    `ExceptionGroup("fallaron tareas", [...])` con esas excepciones, cada una con la
    nota "tarea N" (N empezando en 0).
    """
    raise NotImplementedError("TODO")
