# Names, Objects and Mutability

If you're coming from another language, the most important thing about Python isn't the syntax
but its **data model**: variables aren't boxes that hold values, they're **names that point to
objects**. Almost every "weird" beginner bug (lists that change on their own, shared defaults,
copies that aren't copies) comes from not having this idea clear.

## Everything is an object, variables are labels

```python
a = [1, 2, 3]
b = a            # b is NOT a copy: it's another name for the SAME object
b.append(4)
print(a)         # [1, 2, 3, 4]
```

Every object has:

- **identity**: `id(obj)`, which never changes during its lifetime;
- **type**: `type(obj)`, which doesn't change either;
- **value**: which may or may not change, depending on whether the type is mutable or immutable.

Assignment with `=` **never copies**: it just makes a name point to an object. The same happens
when you pass arguments to a function: the function receives a reference to the same object
(sometimes called *pass by object reference* or *call by sharing*).

## `==` vs. `is`

```python
a = [1, 2]
b = [1, 2]
a == b      # True:  same VALUE
a is b      # False: different objects
```

- `==` compares values (it calls `__eq__`).
- `is` compares identity (is it the same object?).

Use `is` **only** with singletons: `x is None`, `x is True`/`False` (rare) or your own sentinels.
For everything else, `==`. That `a is b` gives `True` for small ints or short strings is an
implementation detail (CPython reuses those objects); don't rely on it.

## Mutable and immutable

| Immutable                                    | Mutable                           |
|----------------------------------------------|-----------------------------------|
| `int`, `float`, `bool`, `complex`, `Decimal` | `list`                            |
| `str`, `bytes`                               | `dict`                            |
| `tuple`, `frozenset`                         | `set`, `bytearray`                |
| `None`                                       | most of your own classes          |

With an immutable object, any "modification" creates a new object:

```python
s = "hello"
t = s
s += "!"        # creates a new str and rebinds s
print(t)        # "hello"  <- t still points to the original
```

With a mutable object, `+=` modifies **in place**:

```python
xs = [1]
ys = xs
xs += [2]       # list.__iadd__ extends the same object
print(ys)       # [1, 2]
```

> A tuple is immutable, but if it **contains** a mutable object, that object can change:
> `t = ([1], 2); t[0].append(9)` works. The tuple still points to the same list.

## Consequence 1: functions that mutate their arguments

```python
def add_tax(prices):
    for i, p in enumerate(prices):
        prices[i] = p * 1.21      # ✗ modifies the caller's list
    return prices
```

The caller loses their original data without noticing. The Python convention is:

- if the function **mutates**, it returns `None` (like `list.sort()` or `dict.update()`);
- if it **doesn't mutate**, it returns a new object (like `sorted()`).

```python
def with_tax(prices):
    return [p * 1.21 for p in prices]   # ✓ leaves the original alone
```

## Consequence 2: shallow and deep copies

```python
import copy

original = [[1, 2], [3, 4]]

shallow = original.copy()      # also: list(original), original[:]
shallow[0].append(99)
print(original)                # [[1, 2, 99], [3, 4]]  <- it changed!

deep = copy.deepcopy(original)
deep[0].append(100)
print(original)                # unchanged
```

A **shallow** copy creates a new container with the *same* references inside. A **deep** copy
copies everything recursively. For a list of lists, `[row.copy() for row in m]` is enough;
`deepcopy` is the general-purpose hammer (and slower).

## Consequence 3: `[[0] * 3] * 3`

```python
board = [[0] * 3] * 3
board[0][0] = 1
print(board)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```

`* 3` repeats **the reference** to the same inner list. The correct way is
`[[0] * 3 for _ in range(3)]`: the comprehension creates a new list on each iteration.

## Numbers: what's worth remembering

```python
7 / 2       # 3.5   true division, always float
7 // 2      # 3     integer (floor) division
-7 // 2     # -4    rounds toward -infinity, not toward 0!
-7 % 2      # 1     the remainder takes the sign of the divisor
divmod(-7, 2)       # (-4, 1)
2 ** 100    # ints have no size limit
0.1 + 0.2   # 0.30000000000000004  <- binary float (IEEE 754)
```

For money or any exact decimal calculation, use `decimal.Decimal` **built from a string**:

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")    # Decimal('0.3')
Decimal(0.1)                       # Decimal('0.1000000000000000055511151231257827...')  ✗
```

To compare floats, use `math.isclose(a, b)` instead of `==`.

## Truthiness

Any object can be evaluated as a boolean. These are **falsy**: `None`, `False`, `0`, `0.0`,
`""`, `[]`, `{}`, `set()`, `()` and any object whose `__bool__` returns `False` or whose
`__len__` returns 0. Everything else is truthy.

```python
if not items:            # ✓ idiomatic for "empty"
if len(items) == 0:      # ✗ noise

name = user_input or "anonymous"   # default if user_input is falsy
```

Careful: `x or default` also replaces a valid `0` or `""`. If what you mean is
"if it's `None`", say so: `x if x is not None else default`.

## Dynamic but strong typing

Names don't have types; objects do. And Python **doesn't implicitly convert** between
incompatible types:

```python
"3" + 4          # TypeError (in JavaScript it would be "34")
int("3") + 4     # 7
```

*Type hints* (`def f(x: int) -> str`) aren't checked at runtime: they're used by tools like
mypy and by editors. We cover them in the tooling module.

## Summary

- `=` never copies; arguments are passed as references to the same object.
- `is` for `None` and sentinels; `==` for everything else.
- Mutable objects modified "at a distance" are the number one source of bugs: don't mutate
  what you're given unless that's the function's whole point.
- `list.copy()` is shallow; `copy.deepcopy()` is deep.
- `//` and `%` round toward -infinity; for money, use `Decimal("...")`.

## Exercise

Four functions that force you to respect the object model: don't mutate, copy correctly,
add up money without float errors and understand integer division.

**Further reading:** [Data model — Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types),
*Fluent Python* (2nd ed.), ch. 6 ("Object References, Mutability, and Recycling").
