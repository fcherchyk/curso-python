# Classes and the data model

Python classes are simple: no `private`, no method overloading, no mandatory interfaces.
What makes them powerful is the **data model**: a set of special methods (the *dunder
methods*, for *double underscore*) that let your objects plug into the language's syntax:
`len()`, `for`, `in`, `+`, `==`, `print`, `with`…

## The basics, quickly

```python
class Account:
    fee = 0.01                           # CLASS attribute (shared)

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner               # INSTANCE attributes
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

a = Account("Alice")
a.deposit(100)            # same as Account.deposit(a, 100)
```

- `self` is explicit: it's the instance the method is called on.
- `__init__` **initializes**; it doesn't construct (that's `__new__`, which you almost never touch).
- Class attributes are shared across instances. Watch out for **mutables** there: a list
  defined on the class is shared by **all** instances.

### Privacy by convention

```python
self.balance      # public
self._internal    # "private" by convention: don't touch it from outside
self.__secret     # name mangling: renamed to _Account__secret (avoids clashes in inheritance)
```

There's no real privacy, and that's fine: *"we are all consenting adults"*. Use `_name` to
signal internals.

## `__repr__` and `__str__`

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x!r}, {self.y!r})"     # for devs: unambiguous

    def __str__(self):
        return f"({self.x}, {self.y})"               # for humans
```

- `repr(obj)` is used in the REPL, the debugger, logs and inside containers (`print([p])`
  shows the `repr` of each element). Ideally it's an expression that recreates the object.
- `str(obj)` is used by `print` and f-strings. If you don't define it, it falls back to `__repr__`.

**Always implement `__repr__`.** The default, `<Point object at 0x10a3…>`, doesn't help
when debugging.

## Equality and hashing

By default, `==` compares **identity**: two distinct objects are never equal. To compare
by value:

```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented            # not False! lets Python try the other side
    return (self.x, self.y) == (other.x, other.y)

def __hash__(self):
    return hash((self.x, self.y))
```

Two rules:

1. If two objects are `==`, they must have the same `hash`. That's why, **when you define
   `__eq__`, Python sets `__hash__ = None`** and the objects can no longer go in sets or be
   used as keys. If you want them hashable, define `__hash__` from the same fields.
2. Only hash objects whose value **doesn't change**. If you mutate an object that's inside a
   set, the set breaks.

Returning `NotImplemented` (a special constant, not the exception) tells Python "I don't know
how to compare with that". Python then tries the other operand's method and, if neither can,
falls back to identity (for `==`) or raises `TypeError` (for `<` and friends).

## Operators

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):              # v + w
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):                  # v * 3
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                     # 3 * v  (the "r" is the right operand)

    def __abs__(self):                     # abs(v)
        return math.hypot(self.x, self.y)

    def __bool__(self):                    # if v:
        return bool(abs(self))
```

For `3 * v`, Python first tries `int.__mul__(3, v)`, which returns `NotImplemented`, and
then `v.__rmul__(3)`. That's why it matters to return `NotImplemented` instead of raising
an exception.

Operators should return a **new** object. The *in-place* ones (`__iadd__` for `+=`) may
mutate, but only on mutable types.

## Behaving like a collection

| You want…                 | Implement                           |
|---------------------------|-------------------------------------|
| `len(x)`                  | `__len__`                           |
| `if x:` (empty = false)   | `__len__` or `__bool__`             |
| `for i in x`              | `__iter__`                          |
| `item in x`               | `__contains__` (otherwise uses `__iter__`) |
| `x[i]`, `x[a:b]`          | `__getitem__`                       |
| `x[i] = v`, `del x[i]`    | `__setitem__`, `__delitem__`        |
| `reversed(x)`             | `__reversed__` (or `__len__` + `__getitem__`) |

Delegating to an internal collection is almost always enough:

```python
class Deck:
    def __init__(self, cards):
        self._cards = list(cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, i):              # enables x[0], slicing, and even for e in
        return self._cards[i]
```

With those two methods, `random.choice(deck)`, `deck[:3]`, `for c in deck`, `c in deck` and
`reversed(deck)` just work.

## Inheritance: just enough

```python
class PremiumAccount(Account):
    fee = 0.0

    def __init__(self, owner, balance=0, limit=1000):
        super().__init__(owner, balance)   # always super(), not Account.__init__(self, ...)
        self.limit = limit
```

Prefer **composition** (an object that *has* another) over inheritance (an object that *is*
another), unless there's a real "is a" relationship. Deep hierarchies are hard to follow.

## Summary

- `self` is explicit, `__init__` initializes, `_name` is private by convention.
- Always `__repr__`; `__str__` if you need a human-friendly version.
- `__eq__` disables hashing: if you need a hash, define it from the same fields.
- Operators return `NotImplemented` for types they don't handle; `__rmul__` and
  friends cover the right operand.
- `__len__` + `__getitem__` (or `__iter__`) make your class behave like a collection.
- In the upcoming dataclasses chapter you'll see how to **generate** most of this.

## Exercise

A `Vector` with operators, equality and hashing, and a `Cart` that behaves like a collection.

**Further reading:** [Data model](https://docs.python.org/3/reference/datamodel.html),
*Fluent Python* (2nd ed.), ch. 1 and 16.
