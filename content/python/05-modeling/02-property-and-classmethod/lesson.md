# property, classmethod and staticmethod

Three decorators that change how a method is accessed. `@property` lets you start with plain
public attributes and add logic later **without breaking anyone**. `@classmethod` is the
idiomatic way to write alternative constructors. `@staticmethod` is for functions that live
in the class for organization.

## The problem: getters and setters

In Java it's common to write `getBalance()` and `setBalance()` "just in case". Not in Python:

```python
class Product:
    def __init__(self, price):
        self.price = price             # plain public attribute

p = Product(100)
p.price = 120
```

If tomorrow you need to check that the price isn't negative, you don't have to change the
API to `set_price()`: you turn the attribute into a **property** and all the code doing
`p.price = x` keeps working.

## `@property`: computed or controlled attributes

```python
class Product:
    def __init__(self, price: float) -> None:
        self.price = price             # goes through the setter too!

    @property
    def price(self) -> float:          # getter: accessed as p.price
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"negative price: {value}")
        self._price = value

    @property
    def price_with_tax(self) -> float:   # getter only: read-only
        return round(self._price * 1.21, 2)
```

```python
p = Product(100)
p.price_with_tax          # 121.0  (no parentheses)
p.price = -5              # ValueError
p.price_with_tax = 1      # AttributeError: property has no setter
```

Important details:

- The real value is stored in another attribute (`_price`). If the getter did
  `return self.price`, it would call itself in infinite recursion.
- Assigning in `__init__` with `self.price = …` makes the **validation run at construction
  time too**.
- A property without a setter is **read-only**.
- There's also `@price.deleter`, but it's rarely used.

### When to use a property

- **Derived values** that are cheap to compute: `full_name`, `total`, `is_adult`.
- **Validation or normalization** on assignment.
- **Compatibility**: turning an attribute into a computed one without changing the API.

When **not** to:

- If the computation is expensive or has side effects (I/O, network): whoever reads `obj.x`
  expects it to be instant. Use a method with a verb name (`compute_x()`) or
  `functools.cached_property`, which computes it the first time and stores the result.

## `@classmethod`: alternative constructors

A classmethod receives **the class** (`cls`) instead of the instance. Its main use is
offering other ways to create objects:

```python
from datetime import date

class Person:
    def __init__(self, name: str, birth_date: date) -> None:
        self.name = name
        self.birth_date = birth_date

    @classmethod
    def from_dict(cls, data: dict) -> "Person":
        return cls(data["name"], date.fromisoformat(data["birth_date"]))

    @classmethod
    def from_csv(cls, line: str) -> "Person":
        name, iso_date = line.split(",")
        return cls(name.strip(), date.fromisoformat(iso_date.strip()))
```

Why `cls(...)` and not `Person(...)`? Because if someone subclasses it (`class Employee(Person)`),
`Employee.from_dict(...)` will create an `Employee`. The stdlib uses this pattern
everywhere: `dict.fromkeys`, `datetime.fromisoformat`, `int.from_bytes`, `Path.cwd()`.

The naming convention is `from_…`.

## `@staticmethod`: a function in the class namespace

```python
class Email:
    @staticmethod
    def normalize(text: str) -> str:
        return text.strip().lower()
```

It receives neither `self` nor `cls`: it's a plain function that lives inside the class
because it's related to it. Often a module-level function is just as good, or better.
If the method needs the class, it's a `classmethod`; if it needs the instance, it's a
regular method.

| Decorator       | First parameter  | Typical use                           |
|-----------------|------------------|---------------------------------------|
| (none)          | `self`           | instance behavior                     |
| `@classmethod`  | `cls`            | alternative constructors, factories   |
| `@staticmethod` | —                | utilities related to the class        |
| `@property`     | `self`           | computed or validated attribute       |

## How it works under the hood (a glimpse)

`property`, `classmethod` and `staticmethod` are **descriptors**: objects with `__get__` (and
`__set__`) that Python consults when you access an attribute on the class. Descriptors are
how methods (the automatic `self`), properties and Django and SQLAlchemy fields are
implemented. You won't write them often, but it's worth knowing they exist.

## Summary

- Start with public attributes; turn them into `@property` when you need logic.
- Store the real value in `_attribute` and assign through the property in `__init__` so it's
  always validated.
- Without a setter, the property is read-only.
- `@classmethod` + `cls(...)` for alternative constructors (`from_…`).
- `@staticmethod` for stateless utilities; a module-level function is usually enough.

## Exercise

A `Temperature` with validated, convertible properties, and a `User` with a normalized
email, a read-only id and an alternative constructor.

**Further reading:** [property](https://docs.python.org/3/library/functions.html#property),
[Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html), *Fluent Python*, ch. 22.
