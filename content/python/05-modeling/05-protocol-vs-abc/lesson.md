# Interfaces: Protocol vs. ABC

Python has no `interface` keyword. It has **duck typing** ("if it walks like a duck and
quacks like a duck, it's a duck") and two tools to formalize it: **abstract base classes**
(ABCs), which require inheritance, and **Protocols**, which describe a shape without requiring
anything. Knowing which one to use in each case is part of designing Pythonic APIs.

## Duck typing: the starting point

```python
def total_area(shapes):
    return sum(s.area() for s in shapes)
```

This function doesn't care **what** each shape is, but **what it can do**: have an `area()`
method. Any object that has it will do. It's flexible, but the "interface" only lives in
your head. If someone passes an object without `area`, they find out at runtime.

## ABC: nominal interface, with inheritance

```python
from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        """Sends a message. Returns True if it went through."""

    def send_to_all(self, recipients: list[str], message: str) -> int:
        # concrete method that uses the abstract one ("template method" pattern)
        return sum(self.send(r, message) for r in recipients)

class EmailNotifier(Notifier):
    def send(self, recipient, message):
        ...
        return True
```

What an ABC gives you:

- **The base can't be instantiated**: `Notifier()` raises `TypeError`.
- **An incomplete subclass can't be instantiated**: if `EmailNotifier` doesn't implement
  `send`, it fails when creating the instance (not later, when calling the method).
- It can bring shared **concrete methods**, like `send_to_all`.
- `isinstance(x, Notifier)` works.

The cost is that you have to **inherit**. It doesn't work for classes you don't control (from
another library).

## Protocol: structural interface, no inheritance

```python
from typing import Protocol

class HasArea(Protocol):
    def area(self) -> float: ...

class Circle:                      # doesn't inherit from HasArea
    def __init__(self, r): self.r = r
    def area(self) -> float: return math.pi * self.r ** 2

def total_area(shapes: Iterable[HasArea]) -> float:
    return sum(s.area() for s in shapes)
```

A `Protocol` describes **the shape** an object must have. Any class that has those methods,
with those signatures, **conforms automatically**, without inheriting or registering. It's
duck typing, but **checked by the type checker** (mypy or pyright): if you pass something
without `area()`, it flags it before running.

By default, a Protocol **doesn't exist at runtime**: `isinstance(x, HasArea)` raises
`TypeError`. If you need to check it at runtime, decorate it with `@runtime_checkable`:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

isinstance(open("x.txt"), Closeable)    # True
```

Careful: `runtime_checkable` only checks that the methods **exist**, not their signatures or types.

## Which one to choose?

| Situation                                                      | Use          |
|----------------------------------------------------------------|--------------|
| Typing a parameter: "I need something with `.read()`"          | **Protocol** |
| Implementations are third-party or you don't control them      | **Protocol** |
| You want to share code across implementations (template method) | **ABC**     |
| You want an incomplete implementation to fail on instantiation | **ABC**      |
| It's your own hierarchy with a clear "is a" relationship       | **ABC**      |

In modern practice, **Protocol is the default choice for typing dependencies**: it makes code
easy to test (any *fake* with the methods will do) and doesn't couple implementers to your
class hierarchy.

## The stdlib ABCs: `collections.abc`

The stdlib defines ABCs for the language's protocols, and you should use them in type
annotations:

```python
from collections.abc import Iterable, Iterator, Sequence, Mapping, Callable

def process(items: Iterable[str]) -> list[str]: ...      # accepts list, set, generator…
def lookup(table: Mapping[str, int], k: str) -> int: ...   # accepts dict and more
```

They're smart "mixins": if you inherit from `collections.abc.Sequence` and implement
`__getitem__` and `__len__`, you get `__contains__`, `__iter__`, `__reversed__`, `index` and
`count` for free.

A useful principle: **accept the most abstract type** (`Iterable`, `Mapping`) and **return the
most concrete one** (`list`, `dict`).

## Summary

- Duck typing: what matters is what the object can do, not what it is.
- ABC: mandatory inheritance, fails on instantiation if something is missing, and lets you
  share code.
- Protocol: structural shape without inheritance, checked by the type checker; at runtime,
  only with `@runtime_checkable`.
- For typing dependencies, Protocol by default.
- In annotations, `collections.abc` (`Iterable`, `Mapping`…).

## Exercise

A Protocol for shapes, an ABC with a template method and a `runtime_checkable` Protocol for
closing resources.

**Further reading:** [PEP 544 — Protocols](https://peps.python.org/pep-0544/),
[abc](https://docs.python.org/3/library/abc.html), *Fluent Python*, ch. 13.
