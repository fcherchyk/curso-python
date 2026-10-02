"""Interfaces: Protocol vs. ABC."""

import math  # noqa: F401
from abc import ABC, abstractmethod  # noqa: F401
from collections.abc import Iterable
from typing import Protocol, runtime_checkable  # noqa: F401


class TieneArea(Protocol):
    def area(self) -> float: ...


class Circulo:
    def __init__(self, radio: float) -> None:
        self.radio = radio

    def area(self) -> float:
        raise NotImplementedError("TODO")


def area_total(figuras: Iterable[TieneArea]) -> float:
    """Suma de las áreas de cualquier cosa con un método `area()`, sin herencia."""
    raise NotImplementedError("TODO")


class Notificador:  # ← convertila en una ABC con `enviar` abstracto
    """Base abstracta de notificadores.

    - `enviar(destino, mensaje) -> bool`: ABSTRACTO.
    - `enviar_a_todos(destinos, mensaje) -> int`: concreto; cuántos envíos salieron bien.
    """

    def enviar(self, destino: str, mensaje: str) -> bool:
        raise NotImplementedError("TODO")

    def enviar_a_todos(self, destinos: Iterable[str], mensaje: str) -> int:
        raise NotImplementedError("TODO")


class NotificadorMemoria(Notificador):
    """Implementación para tests: guarda (destino, mensaje) en `self.enviados`.
    Falla (devuelve False, sin guardar) si el destino está vacío.
    """

    def __init__(self) -> None:
        self.enviados: list[tuple[str, str]] = []


class Cerrable(Protocol):  # ← hacelo verificable en runtime
    def close(self) -> None: ...


def cerrar_todos(objetos: Iterable[object]) -> int:
    """Llamá a `close()` en los objetos que cumplan `Cerrable` (ignorá el resto) y
    devolvé cuántos cerraste.
    """
    raise NotImplementedError("TODO")
