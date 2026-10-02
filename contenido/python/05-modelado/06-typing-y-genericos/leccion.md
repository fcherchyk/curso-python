# Tipado moderno y genéricos

Los *type hints* no cambian cómo corre Python, pero cambian cómo se **escribe** y cómo se
**mantiene**: el editor autocompleta, mypy o pyright encuentran bugs antes de ejecutar y la
firma de una función documenta qué espera y qué devuelve. FastAPI, Pydantic y SQLAlchemy 2.0
usan los tipos para generar validación, esquemas y consultas. Este capítulo es la chuleta de
la sintaxis moderna (3.10 a 3.12).

## Lo básico, en su versión moderna

```python
def buscar(ids: list[int], cache: dict[str, float] | None = None) -> tuple[int, ...]:
    ...
```

Ya **no** hace falta importar `List`, `Dict`, `Optional` ni `Union` de `typing`:

| Antes (≤ 3.8)                   | Ahora                    |
|---------------------------------|--------------------------|
| `List[int]`, `Dict[str, int]`   | `list[int]`, `dict[str, int]` (3.9) |
| `Optional[str]`                 | `str \| None` (3.10)      |
| `Union[int, str]`               | `int \| str` (3.10)       |
| `Tuple[int, ...]`               | `tuple[int, ...]`        |

Otros que vas a usar seguido:

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal, TypedDict, Self, Final, ClassVar

Callable[[int, str], bool]       # función (int, str) -> bool
Callable[..., Any]               # cualquier función
Literal["r", "w", "a"]           # solo esos valores exactos
Final                            # constante: no reasignar
```

`Any` desactiva el chequeo: usalo como último recurso. Para "un objeto cualquiera que no voy
a tocar", `object` es más seguro.

## `TypedDict`: tipar dicts con forma conocida

Cuando trabajás con JSON o con dicts que tienen claves fijas:

```python
from typing import TypedDict, NotRequired

class UsuarioJSON(TypedDict):
    id: int
    nombre: str
    email: NotRequired[str]

def saludar(u: UsuarioJSON) -> str:
    return f"hola {u['nombre']}"        # mypy sabe que 'nombre' es str
```

En runtime sigue siendo un `dict` común: solo existe para el type checker.

## Alias de tipos: `type` (3.12)

```python
type Json = dict[str, Json] | list[Json] | str | int | float | bool | None
type Matriz = list[list[float]]

def cargar(texto: str) -> Json: ...
```

Los alias dan nombre a tipos largos y permiten recursión (como en `Json`).

## Genéricos: funciones y clases parametrizadas por tipo

Un genérico es un "tipo con un hueco". `list[int]` y `list[str]` son la misma clase con
distinto parámetro. Desde 3.12 hay una sintaxis directa para escribir los tuyos:

```python
def primero[T](xs: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(xs), default)

primero([1, 2])          # mypy infiere: int | None
primero(["a"])           # str | None
```

`[T]` declara una **variable de tipo**: la función funciona con cualquier `T`, pero el tipo
de entrada y el de salida quedan **ligados**.

```python
class Pila[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def apilar(self, item: T) -> None:
        self._items.append(item)

    def desapilar(self) -> T:
        return self._items.pop()

p = Pila[int]()
p.apilar(1)
p.apilar("x")            # mypy: error, se esperaba int
```

Se pueden poner **cotas**:

```python
def maximo[T: (int, float)](xs: list[T]) -> T: ...      # T es int o float
def ordenar[T: Comparable](xs: list[T]) -> list[T]: ... # T cumple un Protocol
```

> Antes de 3.12 se escribía `T = TypeVar("T")` y `class Pila(Generic[T])`. Lo vas a ver en
> mucho código existente; significa lo mismo.

## `Self`: métodos que devuelven la propia clase

```python
from typing import Self

class Consulta:
    def filtrar(self, cond: str) -> Self:    # sirve también en subclases
        ...
        return self
```

## Los tipos no se verifican al ejecutar

```python
def doble(x: int) -> int:
    return x * 2

doble("ab")      # 'abab': Python no se queja
```

Para aprovechar los tipos hay que **correr un type checker**: `mypy`, `pyright` (el que usa
VS Code) o `ty`. Lo configuramos en el módulo de herramientas. Si además necesitás validar
datos **en runtime** (entradas externas), eso es Pydantic.

Los tipos quedan disponibles para introspección, que es lo que usan los frameworks:

```python
doble.__annotations__        # {'x': <class 'int'>, 'return': <class 'int'>}
Pila.__type_params__         # (T,)
```

## Consejos prácticos

- Tipá las **firmas** (parámetros y retorno): ahí está el 90 % del valor. Las variables
  locales se infieren solas.
- Aceptá tipos abstractos (`Iterable`, `Mapping`) y devolvé concretos (`list`, `dict`).
- Si algo puede ser `None`, que lo diga el tipo (`str | None`), y mypy te obliga a manejarlo.
- Evitá `Any`; si una librería no tiene tipos, aislala detrás de una función tipada.

## Resumen

- `list[int]`, `dict[str, X]`, `X | None`: sin imports de `typing`.
- `Callable`, `Iterable` y `Mapping` vienen de `collections.abc`; `Literal`, `TypedDict`, `Self`
  y `Any`, de `typing`.
- `type Alias = ...` para nombrar tipos (3.12).
- Genéricos con `def f[T](...)` y `class C[T]:` (3.12), con cotas opcionales.
- Los tipos no se verifican solos: hace falta mypy o pyright.

## Ejercicio

Una pila genérica y dos funciones genéricas con la sintaxis de 3.12, más un `TypedDict` para
datos tipo JSON.

**Para profundizar:** [typing](https://docs.python.org/3/library/typing.html),
[PEP 695 — Type Parameter Syntax](https://peps.python.org/pep-0695/),
[mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
