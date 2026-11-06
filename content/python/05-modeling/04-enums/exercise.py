"""Enums."""

from enum import Enum, Flag, IntEnum, StrEnum, auto  # noqa: F401


class Estado(Enum):  # ← cambiá la base a StrEnum
    """Estados de una tarea. Los miembros tienen que ser strings:
    `Estado.PENDIENTE == "pendiente"`.

    - `siguiente()`: PENDIENTE → EN_CURSO → TERMINADO; desde TERMINADO, ValueError.
    - `es_final` (property): True solo para TERMINADO.
    """

    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    TERMINADO = "terminado"

    def siguiente(self) -> "Estado":
        raise NotImplementedError("TODO")


class Prioridad(Enum):  # ← cambiá la base para que se ordenen como enteros
    BAJA = 1
    MEDIA = 2
    ALTA = 3


def mas_urgentes(tareas: list[tuple[str, Prioridad]]) -> list[str]:
    """Nombres de las tareas ordenadas de mayor a menor prioridad (estable ante empates).

    >>> mas_urgentes([("a", Prioridad.BAJA), ("b", Prioridad.ALTA)])
    ['b', 'a']
    """
    raise NotImplementedError("TODO")


class Permiso(Enum):  # ← cambiá la base a Flag
    """Permisos combinables: LEER, ESCRIBIR, BORRAR (con auto()) y TODOS (los tres)."""

    LEER = 1


def puede(permisos: Permiso, requerido: Permiso) -> bool:
    """¿`permisos` incluye TODO lo de `requerido`?

    >>> puede(Permiso.LEER | Permiso.ESCRIBIR, Permiso.LEER)
    True
    """
    raise NotImplementedError("TODO")
