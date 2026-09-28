from collections.abc import Callable, Iterable
from typing import TypedDict


class Pila[T]:
    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: list[T] = list(items)

    def apilar(self, item: T) -> None:
        self._items.append(item)

    def desapilar(self) -> T:
        if not self._items:
            raise IndexError("pila vacía")
        return self._items.pop()

    def tope(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Pila({self._items!r})"


def primero[T](xs: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(xs), default)


def agrupar_por[T, K](xs: Iterable[T], clave: Callable[[T], K]) -> dict[K, list[T]]:
    grupos: dict[K, list[T]] = {}
    for x in xs:
        grupos.setdefault(clave(x), []).append(x)
    return grupos


class UsuarioJSON(TypedDict):
    id: int
    nombre: str
    activo: bool


def activos(usuarios: list[UsuarioJSON]) -> list[str]:
    return [u["nombre"] for u in sorted(usuarios, key=lambda u: u["id"]) if u["activo"]]
