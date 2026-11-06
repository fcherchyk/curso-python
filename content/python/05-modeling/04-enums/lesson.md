# Enums

An **enum** is a closed set of named values: order statuses, log levels, HTTP methods, days
of the week. Using them instead of loose ("magic") strings or numbers makes the code
self-documenting, makes typos fail immediately and lets the editor autocomplete.

## The problem with magic strings

```python
if order.status == "shipped": ...
if order.status == "shiped": ...        # typo: never True and nobody notices
```

With an enum:

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

if order.status is Status.SHIPPED: ...
if order.status is Status.SHIPED: ...     # immediate AttributeError
```

## The basics

```python
Status.SHIPPED              # <Status.SHIPPED: 'shipped'>
Status.SHIPPED.name         # 'SHIPPED'
Status.SHIPPED.value        # 'shipped'
Status("shipped")           # lookup by VALUE → Status.SHIPPED
Status["SHIPPED"]           # lookup by NAME
Status("lost")              # ValueError
list(Status)                # the members, in definition order
len(Status)                 # 3
Status.SHIPPED in Status    # True
```

Members are **singletons**: compare them with `is` (though `==` works too).

## `auto()`: when the value doesn't matter

```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()       # 1
    GREEN = auto()     # 2
```

## `StrEnum` and `IntEnum`: enums that are also str or int

A plain `Enum` is **not** equal to its value: `Status.SHIPPED == "shipped"` is `False`. That's
annoying at the edges of your program (JSON, the database, URL parameters). `StrEnum`
(3.11+) and `IntEnum` make the members **be** strings or integers:

```python
from enum import StrEnum, IntEnum, auto

class Method(StrEnum):
    GET = auto()          # with StrEnum, auto() gives the lowercase name: "get"
    POST = auto()

Method.GET == "get"       # True
f"{Method.GET}"           # 'get'
json.dumps({"m": Method.GET})   # '{"m": "get"}'  ← serializes directly

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

Priority.HIGH > Priority.LOW        # True: compared as ints
sorted([Priority.HIGH, Priority.LOW])
```

Rule of thumb: **`StrEnum` for almost anything that goes to JSON or the database**; `IntEnum`
when numeric order makes sense (priorities, levels); plain `Enum` when you don't want it
mixing with strings.

FastAPI, Pydantic and SQLAlchemy understand enums: they validate that the incoming value is
one of the members and document it in OpenAPI.

## Enums are classes: they can have methods

```python
class Status(StrEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

    @property
    def is_final(self) -> bool:
        return self is Status.DELIVERED

    def next(self) -> "Status":
        members = list(Status)
        i = members.index(self)
        if i == len(members) - 1:
            raise ValueError("already in the final status")
        return members[i + 1]
```

That way the "state machine" logic lives next to the states.

## `Flag`: combinations

For permissions or combinable options, `Flag` lets you work with bits:

```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()        # 1
    WRITE = auto()       # 2
    DELETE = auto()      # 4
    ALL = READ | WRITE | DELETE

p = Permission.READ | Permission.WRITE
Permission.WRITE in p       # True
Permission.DELETE in p      # False
p & Permission.DELETE       # Permission(0): empty, falsy
```

## Enums and `match`

Enums go very well with `match` (module 06). Be careful to use the full dotted name:

```python
match status:
    case Status.PENDING:       # ✓ compares with the member
        ...
    case PENDING:              # ✗ captures any value into a variable named PENDING!
        ...
```

## Summary

- Enums instead of magic strings or numbers: early errors and self-documenting code.
- `.name`, `.value`, `Class(value)`, `Class["NAME"]`, `list(Class)`.
- `StrEnum` for values that go to JSON or the database; `IntEnum` if numeric order
  matters.
- Enums can have methods and properties.
- `Flag` for combinations of options.

## Exercise

A `StrEnum` with a state machine, an `IntEnum` to sort by priority and a permissions `Flag`.

**Further reading:** [enum](https://docs.python.org/3/library/enum.html),
[Enum HOWTO](https://docs.python.org/3/howto/enum.html).
