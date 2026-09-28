from collections.abc import Callable
from typing import Any


def validar_usuario(datos: dict[str, Any]) -> None:
    errores: list[Exception] = []
    nombre = datos.get("nombre")
    if not isinstance(nombre, str) or not nombre:
        errores.append(ValueError("nombre"))
    edad = datos.get("edad")
    if not isinstance(edad, int):
        errores.append(TypeError("edad"))
    elif edad < 0:
        errores.append(ValueError("edad"))
    if "@" not in str(datos.get("email", "")):
        errores.append(ValueError("email"))
    if errores:
        raise ExceptionGroup("usuario inválido", errores)


def clasificar_errores(datos: dict[str, Any]) -> dict[str, list[str]]:
    resultado: dict[str, list[str]] = {"valor": [], "tipo": []}
    try:
        validar_usuario(datos)
    except* ValueError as grupo:
        resultado["valor"] = [str(e) for e in grupo.exceptions]
    except* TypeError as grupo:
        resultado["tipo"] = [str(e) for e in grupo.exceptions]
    return resultado


def ejecutar_todas(tareas: list[Callable[[], Any]]) -> list[Any]:
    resultados: list[Any] = []
    errores: list[Exception] = []
    for i, tarea in enumerate(tareas):
        try:
            resultados.append(tarea())
        except Exception as e:
            e.add_note(f"tarea {i}")
            errores.append(e)
    if errores:
        raise ExceptionGroup("fallaron tareas", errores)
    return resultados
