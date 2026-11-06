# Day 4: Data modeling

**Goal:** model a domain with little code using dataclasses, enums, the data model
(dunder methods) and modern typing. This is the foundation of Pydantic, SQLAlchemy 2.0 and FastAPI.

## 1. Dataclasses

```python
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, order=True)
class Product:
    sku: str
    price: float
    tags: list[str] = field(default_factory=list)  # mutable default, always like this

    def __post_init__(self):  # validation
        if self.price < 0:
            raise ValueError("negative price")
```

| Option        | What it does                                                  |
|---------------|---------------------------------------------------------------|
| `frozen=True` | immutable, and also hashable (works in sets and as a key)     |
| `order=True`  | generates `<`, `>`... comparing fields as a tuple             |
| `slots=True`  | (3.10) less memory, fixed attributes                          |
| `kw_only=True`| (3.10) all fields keyword-only                                |

Utilities: `dataclasses.replace(obj, price=10)` to "modify" a frozen one,
`asdict(obj)` and `fields(cls)`.

**Dataclass or Pydantic?** Use a dataclass for internal objects. Pydantic `BaseModel` is for
when you need to **validate external data** (JSON from an API, config): it converts types and
gives detailed errors. It's covered in week 4.

## 2. `@property` and `@classmethod`

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):  # accessed as an attribute: t.fahrenheit
        return self.celsius * 9 / 5 + 32

    @classmethod
    def from_fahrenheit(cls, f):  # alternative constructor
        return cls((f - 32) * 5 / 9)
```

## 3. Enums

```python
from enum import Enum, StrEnum, IntEnum, auto


class Color(StrEnum):  # 3.11+: members are str (they serialize straight to JSON)
    RED = auto()  # value "red"
    GREEN = auto()


Color("red") is Color.RED  # lookup by value
list(Color)  # in definition order
```

## 4. The data model (dunder methods)

By implementing dunders, your objects integrate with the language's syntax:

| You want...                    | Implement                                    |
|--------------------------------|----------------------------------------------|
| `len(x)`, `if x:`              | `__len__` (or `__bool__`)                    |
| `for i in x`                   | `__iter__`                                   |
| `item in x`                    | `__contains__`                               |
| `x[i]`, `x[a:b]`               | `__getitem__`                                |
| `x + y`, `x == y`, `x < y`     | `__add__`, `__eq__`, `__lt__`                |
| `print(x)` vs. debugger        | `__str__` (for humans), `__repr__` (for devs) |
| `with x:`                      | `__enter__` / `__exit__`                     |
| `x()`                          | `__call__`                                   |

## 5. Modern typing

```python
def f(xs: list[int], m: dict[str, float] | None = None) -> tuple[int, ...]: ...


# no longer needed: from typing import List, Dict, Optional, Union

from collections.abc import Iterable, Callable, Iterator, Sequence, Mapping
from typing import Protocol, TypedDict, Literal, Self, Any


class Stack[T]:  # generics, 3.12 syntax
    def push(self, x: T) -> Self: ...


def first[T](xs: Sequence[T]) -> T: ...


type Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None  # 3.12
```

**Protocol** is duck typing checked by the type checker: any class with the right methods
"conforms", without inheriting. It's a better fit than an ABC when you don't control the classes.

Good practice for parameters: accept the most abstract type you can (`Iterable`, `Mapping`) and
return the most concrete one (`list`, `dict`).

Type hints are **not checked at runtime**. For that, run `uv run mypy week1`
(day 6).

## Exercises

```bash
uv run pytest week1/day4_modeling
```

Heads up: if `__post_init__` or `__len__` are left unimplemented, several tests will fail at
once. Start with those.

**Extra challenge:** make `Cart` support `cart[0]` and `cart[1:]` by implementing
`__getitem__`.

## Further reading

- [dataclasses docs](https://docs.python.org/3/library/dataclasses.html)
- *Fluent Python*, ch. 1 (data model), 5 (data classes) and 13 (protocols).
- [mypy typing cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
