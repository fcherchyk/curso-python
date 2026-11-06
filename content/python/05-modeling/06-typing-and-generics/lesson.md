# Modern typing and generics

*Type hints* don't change how Python runs, but they change how code is **written** and
**maintained**: the editor autocompletes, mypy or pyright find bugs before you run anything,
and a function's signature documents what it expects and what it returns. FastAPI, Pydantic
and SQLAlchemy 2.0 use types to generate validation, schemas and queries. This chapter is a
cheat sheet for the modern syntax (3.10 to 3.12).

## The basics, modern version

```python
def find(ids: list[int], cache: dict[str, float] | None = None) -> tuple[int, ...]:
    ...
```

You **no longer** need to import `List`, `Dict`, `Optional` or `Union` from `typing`:

| Before (≤ 3.8)                  | Now                      |
|---------------------------------|--------------------------|
| `List[int]`, `Dict[str, int]`   | `list[int]`, `dict[str, int]` (3.9) |
| `Optional[str]`                 | `str \| None` (3.10)      |
| `Union[int, str]`               | `int \| str` (3.10)       |
| `Tuple[int, ...]`               | `tuple[int, ...]`        |

Others you'll use often:

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Any, Literal, TypedDict, Self, Final, ClassVar

Callable[[int, str], bool]       # function (int, str) -> bool
Callable[..., Any]               # any function
Literal["r", "w", "a"]           # only those exact values
Final                            # constant: don't reassign
```

`Any` turns checking off: use it as a last resort. For "any object I'm not going to touch",
`object` is safer.

## `TypedDict`: typing dicts with a known shape

When you work with JSON or dicts that have fixed keys:

```python
from typing import TypedDict, NotRequired

class UserJSON(TypedDict):
    id: int
    name: str
    email: NotRequired[str]

def greet(u: UserJSON) -> str:
    return f"hello {u['name']}"         # mypy knows 'name' is a str
```

At runtime it's still a plain `dict`: it only exists for the type checker.

## Type aliases: `type` (3.12)

```python
type Json = dict[str, Json] | list[Json] | str | int | float | bool | None
type Matrix = list[list[float]]

def load(text: str) -> Json: ...
```

Aliases give names to long types and allow recursion (as in `Json`).

## Generics: functions and classes parameterized by type

A generic is a "type with a hole". `list[int]` and `list[str]` are the same class with a
different parameter. Since 3.12 there's a direct syntax for writing your own:

```python
def first[T](xs: Iterable[T], default: T | None = None) -> T | None:
    return next(iter(xs), default)

first([1, 2])            # mypy infers: int | None
first(["a"])             # str | None
```

`[T]` declares a **type variable**: the function works with any `T`, but the input type
and the output type are **tied together**.

```python
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

s = Stack[int]()
s.push(1)
s.push("x")              # mypy: error, expected int
```

You can add **bounds**:

```python
def maximum[T: (int, float)](xs: list[T]) -> T: ...     # T is int or float
def sort[T: Comparable](xs: list[T]) -> list[T]: ...    # T satisfies a Protocol
```

> Before 3.12 you wrote `T = TypeVar("T")` and `class Stack(Generic[T])`. You'll see it in
> a lot of existing code; it means the same thing.

## `Self`: methods that return their own class

```python
from typing import Self

class Query:
    def filter(self, cond: str) -> Self:     # works in subclasses too
        ...
        return self
```

## Types aren't checked at runtime

```python
def double(x: int) -> int:
    return x * 2

double("ab")     # 'abab': Python doesn't complain
```

To get value from types you have to **run a type checker**: `mypy`, `pyright` (the one
VS Code uses) or `ty`. We set it up in the tooling module. If you also need to validate
data **at runtime** (external input), that's Pydantic.

Types remain available for introspection, which is what frameworks use:

```python
double.__annotations__       # {'x': <class 'int'>, 'return': <class 'int'>}
Stack.__type_params__        # (T,)
```

## Practical tips

- Type the **signatures** (parameters and return): that's 90% of the value. Local
  variables are inferred.
- Accept abstract types (`Iterable`, `Mapping`) and return concrete ones (`list`, `dict`).
- If something can be `None`, let the type say so (`str | None`), and mypy will force you to
  handle it.
- Avoid `Any`; if a library has no types, isolate it behind a typed function.

## Summary

- `list[int]`, `dict[str, X]`, `X | None`: no `typing` imports.
- `Callable`, `Iterable` and `Mapping` come from `collections.abc`; `Literal`, `TypedDict`, `Self`
  and `Any`, from `typing`.
- `type Alias = ...` to name types (3.12).
- Generics with `def f[T](...)` and `class C[T]:` (3.12), with optional bounds.
- Types don't check themselves: you need mypy or pyright.

## Exercise

A generic stack and two generic functions with the 3.12 syntax, plus a `TypedDict` for
JSON-like data.

**Further reading:** [typing](https://docs.python.org/3/library/typing.html),
[PEP 695 — Type Parameter Syntax](https://peps.python.org/pep-0695/),
[mypy cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).
