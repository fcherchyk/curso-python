from enum import Flag, IntEnum, StrEnum, auto


class Estado(StrEnum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    TERMINADO = "terminado"

    def siguiente(self) -> "Estado":
        miembros = list(Estado)
        i = miembros.index(self)
        if i == len(miembros) - 1:
            raise ValueError("la tarea ya está terminada")
        return miembros[i + 1]

    @property
    def es_final(self) -> bool:
        return self is Estado.TERMINADO


class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3


def mas_urgentes(tareas: list[tuple[str, Prioridad]]) -> list[str]:
    # sorted es estable: con reverse=True, los empates conservan el orden original.
    return [nombre for nombre, _ in sorted(tareas, key=lambda t: t[1], reverse=True)]


class Permiso(Flag):
    LEER = auto()
    ESCRIBIR = auto()
    BORRAR = auto()
    TODOS = LEER | ESCRIBIR | BORRAR


def puede(permisos: Permiso, requerido: Permiso) -> bool:
    return requerido in permisos
