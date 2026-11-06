# Dataclasses

In the previous chapter you wrote `__init__`, `__repr__`, `__eq__` and `__hash__` by hand.
`@dataclass` **generates** them from the class annotations. It's the idiomatic way to define
objects that are mostly data: DTOs, records, configurations, domain entities.

## The bare minimum

```python
from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    name: str
    price: float = 0.0           # with a default

p = Product("A1", "Coffee", 3500)
p                                # Product(sku='A1', name='Coffee', price=3500)
p == Product("A1", "Coffee", 3500)   # True: compares field by field
```

It generates `__init__`, `__repr__` and `__eq__`. The **fields** are the **annotated** class
attributes. Attributes without an annotation aren't fields.

Rule: fields with a default go **after** fields without one, just like in any function
signature. Otherwise, `TypeError: non-default argument follows default argument`.

## Mutable defaults: `field(default_factory=...)`

```python
from dataclasses import field

@dataclass
class Cart:
    items: list[str] = []                         # ValueError: mutable default
    items: list[str] = field(default_factory=list)   # ✓ a new list per instance
```

It's the same mutable-default trap as with functions, but `dataclass` **detects it** and
stops you. `default_factory` takes a no-argument function (`list`, `dict`, `set` or
`lambda: {"a": 1}`) that's called for every new instance.

Other `field` options:

```python
id: int = field(default=0, repr=False)         # doesn't show up in the repr
cache: dict = field(default_factory=dict, compare=False)   # doesn't take part in ==
_internal: int = field(init=False, default=0)   # not in the __init__
```

## Decorator options

```python
@dataclass(frozen=True, order=True, slots=True, kw_only=True)
```

| Option          | What it does                                                        |
|-----------------|---------------------------------------------------------------------|
| `frozen=True`   | immutable (assigning raises `FrozenInstanceError`) **and hashable** |
| `order=True`    | generates `<`, `<=`, `>`, `>=` comparing the fields as a tuple, in order |
| `slots=True`    | (3.10) uses `__slots__`: less memory, faster access, no new attributes can be added |
| `kw_only=True`  | (3.10) every field is keyword-only in the `__init__`                |
| `eq=False`      | doesn't generate `__eq__` (equality by identity)                    |

`frozen=True` is a great default for value objects (points, money, versions, coordinates):
they're easier to reason about, can be shared without fear and can be used in sets and as
dict keys.

`order=True` compares the fields **in the order they're declared**. So field order becomes
part of the design:

```python
@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0
    patch: int = 0

sorted([Version(1, 10), Version(1, 2)])     # [Version(1, 2, 0), Version(1, 10, 0)]
```

## Validating: `__post_init__`

The generated `__init__` calls `__post_init__` at the end, if it exists. That's the place to
validate or compute derived fields:

```python
@dataclass
class Range:
    start: int
    end: int

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(f"invalid range: {self.start} > {self.end}")
```

In a `frozen` dataclass, to set a derived field inside `__post_init__` you have to use
`object.__setattr__(self, "field", value)`, because normal assignment is blocked.

## "Modifying" a frozen one: `replace`

```python
from dataclasses import replace

v = Version(1, 2, 3)
v2 = replace(v, patch=4)        # copy with one field changed; v is untouched
```

That's how you work with immutable objects: instead of mutating, you create new versions.

## Utilities

```python
from dataclasses import asdict, astuple, fields

asdict(p)       # {'sku': 'A1', 'name': 'Coffee', 'price': 3500}  (recursive)
astuple(p)      # ('A1', 'Coffee', 3500)
[f.name for f in fields(p)]
```

`asdict` is handy for serializing to JSON: `json.dumps(asdict(p))`.

## Methods and properties still work

A dataclass is a regular class. You can add methods, properties, classmethods and your own
dunders. If you define a method the decorator would also generate (for example,
`__repr__`), **yours is kept**.

```python
@dataclass(frozen=True, order=True)
class Version:
    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def from_str(cls, text: str) -> "Version":
        return cls(*(int(p) for p in text.split(".")))

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
```

## Dataclass, NamedTuple, dict or Pydantic?

| Option             | When                                                                |
|--------------------|---------------------------------------------------------------------|
| `dict`             | loose, temporary data, or JSON that's just passing through          |
| `typing.NamedTuple`| small immutable records you also want to unpack or index            |
| `@dataclass`       | internal objects of your domain: the default choice                 |
| Pydantic `BaseModel` | data coming **from outside** (API JSON, config) that has to be **validated and converted** |

Dataclasses **don't validate types**: `Product("A1", "Coffee", "pricey")` is created without
complaint. Annotations are for tools. If you need real validation when receiving external
data, that's Pydantic, which we cover in the frameworks module.

## Summary

- `@dataclass` generates `__init__`, `__repr__` and `__eq__` from the annotations.
- For mutable defaults, `field(default_factory=list)`.
- `frozen=True` gives immutable, hashable objects; `order=True` compares by fields in order.
- `__post_init__` to validate; `replace` to "modify" a frozen one; `asdict` to serialize.
- No type validation: for external data, Pydantic.

## Exercise

A frozen `Point`, a comparable `Version` and an `Order` with a mutable default, validation
and immutable operations.

**Further reading:** [dataclasses](https://docs.python.org/3/library/dataclasses.html),
[PEP 557](https://peps.python.org/pep-0557/), *Fluent Python*, ch. 5.
