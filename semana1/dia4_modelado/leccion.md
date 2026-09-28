# Día 4: Modelado de datos

**Objetivo:** modelar dominio con poco código usando dataclasses, enums, el modelo de datos
(dunder methods) y tipado moderno. Es la base de Pydantic, SQLAlchemy 2.0 y FastAPI.

## 1. Dataclasses

```python
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, order=True)
class Producto:
    sku: str
    precio: float
    tags: list[str] = field(default_factory=list)  # default mutable, siempre así

    def __post_init__(self):  # validación
        if self.precio < 0:
            raise ValueError("precio negativo")
```

| Opción        | Qué hace                                                      |
|---------------|---------------------------------------------------------------|
| `frozen=True` | inmutable, y además hasheable (sirve en sets y como clave)    |
| `order=True`  | genera `<`, `>`... comparando campos como tupla               |
| `slots=True`  | (3.10) menos memoria, atributos fijos                         |
| `kw_only=True`| (3.10) todos los campos keyword-only                          |

Utilidades: `dataclasses.replace(obj, precio=10)` para "modificar" un frozen,
`asdict(obj)` y `fields(cls)`.

**¿Dataclass o Pydantic?** Usá dataclass para objetos internos. Pydantic `BaseModel` sirve
cuando hay que **validar datos externos** (JSON de una API, config): convierte tipos y da
errores detallados. Se ve en la semana 4.

## 2. `@property` y `@classmethod`

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):  # se accede como atributo: t.fahrenheit
        return self.celsius * 9 / 5 + 32

    @classmethod
    def desde_fahrenheit(cls, f):  # constructor alternativo
        return cls((f - 32) * 5 / 9)
```

## 3. Enums

```python
from enum import Enum, StrEnum, IntEnum, auto


class Color(StrEnum):  # 3.11+: los miembros son str (se serializan a JSON directo)
    ROJO = auto()  # valor "rojo"
    VERDE = auto()


Color("rojo") is Color.ROJO  # lookup por valor
list(Color)  # en orden de definición
```

## 4. Modelo de datos (dunder methods)

Implementando dunders tus objetos se integran con la sintaxis del lenguaje:

| Querés...                      | Implementá                                   |
|--------------------------------|----------------------------------------------|
| `len(x)`, `if x:`              | `__len__` (o `__bool__`)                     |
| `for i in x`                   | `__iter__`                                   |
| `item in x`                    | `__contains__`                               |
| `x[i]`, `x[a:b]`               | `__getitem__`                                |
| `x + y`, `x == y`, `x < y`     | `__add__`, `__eq__`, `__lt__`                |
| `print(x)` vs. debugger        | `__str__` (para humanos), `__repr__` (para devs) |
| `with x:`                      | `__enter__` / `__exit__`                     |
| `x()`                          | `__call__`                                   |

## 5. Tipado moderno

```python
def f(xs: list[int], m: dict[str, float] | None = None) -> tuple[int, ...]: ...


# ya no hace falta: from typing import List, Dict, Optional, Union

from collections.abc import Iterable, Callable, Iterator, Sequence, Mapping
from typing import Protocol, TypedDict, Literal, Self, Any


class Pila[T]:  # genéricos, sintaxis 3.12
    def push(self, x: T) -> Self: ...


def primero[T](xs: Sequence[T]) -> T: ...


type Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None  # 3.12
```

**Protocol** es duck typing verificado por el type checker: cualquier clase con los métodos
correctos "cumple", sin heredar. Conviene más que una ABC cuando no controlás las clases.

Buena práctica en parámetros: aceptá lo más abstracto que puedas (`Iterable`, `Mapping`) y
devolvé lo más concreto (`list`, `dict`).

Los type hints **no se verifican en runtime**. Para eso corré `uv run mypy semana1`
(día 6).

## Ejercicios

```bash
uv run pytest semana1/dia4_modelado
```

Ojo: si `__post_init__` o `__len__` quedan sin implementar, van a fallar varios tests a la
vez. Empezá por esos.

**Reto extra:** que `Carrito` soporte `carrito[0]` y `carrito[1:]` implementando
`__getitem__`.

## Para profundizar

- [Doc de dataclasses](https://docs.python.org/3/library/dataclasses.html)
- *Fluent Python*, cap. 1 (modelo de datos), 5 (data classes) y 13 (protocolos).
- [Typing cheat sheet de mypy](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
