# Functions and Signatures

Python signatures are very expressive: parameters with defaults, positional or by name,
variadic, positional-only and keyword-only. Used well, they make calls read on their own and
catch usage errors right away. Used badly, they produce the language's most famous bug: the
mutable default.

## Anatomy

```python
def connect(host: str, port: int = 5432, *, timeout: float = 5.0) -> Connection:
    """Open a connection. (docstring: the first line summarizes)"""
    ...
```

- `host` is required.
- `port` has a default.
- Everything after `*` is **keyword-only**.
- Annotations (`: str`, `-> Connection`) are documentation that tools can verify, but they
  aren't checked at runtime.
- A function without an explicit `return` returns `None`.

## Positional and by name

When calling, any "normal" parameter can be passed by position or by name:

```python
connect("db.local", 5433)
connect(host="db.local", port=5433)
connect("db.local", port=5433)
connect(port=5433, host="db.local")     # by name, order doesn't matter
```

Rule: positional arguments come first. `connect(host="x", 5433)` is a syntax error.

## Keyword-only: after `*`

```python
def export(data, *, format="csv", compress=False): ...

export(rows, format="json", compress=True)   # ✓
export(rows, "json", True)                   # TypeError
```

Forcing the name is very useful for **boolean flags and options**: `export(rows, "json", True)`
says nothing, while `compress=True` does. It also lets you reorder or add options without
breaking callers.

## Positional-only: before `/` (3.8+)

```python
def distance(a, b, /): ...

distance(p1, p2)        # ✓
distance(a=p1, b=p2)    # TypeError
```

It's useful when the parameter name adds nothing or you want to be able to change it without
breaking the API. Many built-in functions work this way: `len(obj, /)`.

The full form:

```python
def f(pos_only, /, normal, *, kw_only): ...
```

## Variadics: `*args` and `**kwargs`

```python
def average(*numbers):           # numbers is a TUPLE
    return sum(numbers) / len(numbers)

average(1, 2, 3)

def tag(text, **attrs):          # attrs is a DICT
    extras = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<span {extras}>{text}</span>"

tag("hello", id="x", klass="y")
```

The names `args` and `kwargs` are just a convention; what matters is the asterisks. Both
together, `def f(*args, **kwargs)`, accept anything, which is useful in decorators and
wrappers that forward arguments to another function.

And the other way around, when **calling**, `*` and `**` unpack (you saw this with unpacking):

```python
nums = [1, 2, 3]
average(*nums)
options = {"format": "json"}
export(rows, **options)
```

## The mutable default trap

**Defaults are evaluated only once**, when the function is defined, not on every call:

```python
def append_to(item, items=[]):     # ✗ the same list for every call
    items.append(item)
    return items

append_to(1)   # [1]
append_to(2)   # [1, 2]   ← surprise!
```

The idiomatic fix is to use `None` as a sentinel:

```python
def append_to(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

The same applies to `dict`, `set`, objects, and even `datetime.now()`: the default
`created=datetime.now()` is frozen at the moment the module was imported.

> If `None` is a valid value for your parameter, use your own sentinel:
> `_MISSING = object()` and `def f(x=_MISSING): if x is _MISSING: ...`.

## Returning multiple values

A function returns **one** object; for "several", return a tuple and unpack it:

```python
def min_max(xs):
    return min(xs), max(xs)

lowest, highest = min_max(data)
```

## Docstrings

The first line summarizes the function in the imperative mood; then, if needed, come the
details. Doctests (`>>> ...`) serve as both an example and a test:

```python
def area(base: float, height: float) -> float:
    """Area of a triangle.

    >>> area(4, 3)
    6.0
    """
    return base * height / 2
```

`help(area)` and editors show this text.

## Summary

- After `*`, keyword-only: ideal for flags and options.
- Before `/`, positional-only: when the name doesn't matter.
- `*args` is a tuple; `**kwargs` is a dict.
- **Never** use a mutable object as a default: use `None` and create it inside.
- Without `return`, the function returns `None`.

## Exercise

Four functions to practice signatures: mutable defaults, variadics, positional-only and
keyword-only parameters, and `**kwargs`.

**Further reading:** [Defining functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions),
[PEP 570 (positional-only)](https://peps.python.org/pep-0570/), [PEP 3102 (keyword-only)](https://peps.python.org/pep-3102/).
