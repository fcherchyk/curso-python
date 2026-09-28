import math
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Protocol, runtime_checkable


class TieneArea(Protocol):
    def area(self) -> float: ...


class Circulo:
    def __init__(self, radio: float) -> None:
        self.radio = radio

    def area(self) -> float:
        return math.pi * self.radio**2


def area_total(figuras: Iterable[TieneArea]) -> float:
    return sum(f.area() for f in figuras)


class Notificador(ABC):
    @abstractmethod
    def enviar(self, destino: str, mensaje: str) -> bool: ...

    def enviar_a_todos(self, destinos: Iterable[str], mensaje: str) -> int:
        return sum(self.enviar(d, mensaje) for d in destinos)


class NotificadorMemoria(Notificador):
    def __init__(self) -> None:
        self.enviados: list[tuple[str, str]] = []

    def enviar(self, destino: str, mensaje: str) -> bool:
        if not destino:
            return False
        self.enviados.append((destino, mensaje))
        return True


@runtime_checkable
class Cerrable(Protocol):
    def close(self) -> None: ...


def cerrar_todos(objetos: Iterable[object]) -> int:
    cerrados = 0
    for obj in objetos:
        if isinstance(obj, Cerrable):
            obj.close()
            cerrados += 1
    return cerrados
