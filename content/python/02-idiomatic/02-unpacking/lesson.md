# Unpacking

*Unpacking* means assigning the elements of an iterable to several names in one go. It looks
like a syntax detail, but it shows up everywhere: in assignments, in `for` loops, in function
calls and when combining collections. Once you master it, almost all the stray `x[0]`, `x[1]`
and `x[-1]` that make code hard to read disappear.

## Multiple assignment

```python
x, y = 3, 4                  # the right side is a tuple (parentheses are optional)
user, domain = "alice@mit.edu".split("@")
a, b = b, a                  # swap without a temporary variable
```

It works with **any iterable**: lists, tuples, strings, generators, the result of
`dict.items()`, etc. The only rule is that the number of names must match the number of
elements:

```python
a, b = [1, 2, 3]   # ValueError: too many values to unpack (expected 2)
a, b, c = [1, 2]   # ValueError: not enough values to unpack (expected 3, got 2)
```

That error works in your favor: if a function "should" return two things and one day returns
three, you find out right away instead of carrying a wrong value around.

### How does the swap work?

`a, b = b, a` first evaluates the whole right side and builds the tuple `(b, a)` with the
**old** values. Only then does it assign. That's why no temporary variable is needed.

## Extended unpacking: `*rest`

A starred name "takes" everything left over, always as a **list**:

```python
first, *rest = [1, 2, 3, 4]         # first=1, rest=[2, 3, 4]
*init, last = "abc"                 # init=['a', 'b'], last='c'
head, *middle, tail = range(5)      # 0, [1, 2, 3], 4
first, *rest = [7]                  # first=7, rest=[]
```

- There can be only **one** starred name per assignment.
- If nothing is left over, the rest is an empty list (it doesn't fail).
- If there aren't enough elements for the **unstarred** names, it does fail: `a, *b = []`
  raises `ValueError`.

To discard values, the convention is `_`:

```python
_, domain = email.split("@")
first, *_, last = line.split(",")
```

## In `for` loops

Each element the iterable produces is unpacked into the names in the `for`. It's what you
do without thinking with `dict.items()`:

```python
for key, value in config.items():
    ...

points = [(0, 0), (3, 4), (1, 1)]
for x, y in points:
    print(x + y)

# Nested structures: the parentheses follow the shape of the data
for i, (x, y) in enumerate(points):
    ...
```

Compare it with the alternative:

```python
for p in points:
    print(p[0] + p[1])     # what was p[0] again?
```

## Unpacking in function calls: `*` and `**`

In a **call**, `*` expands an iterable into positional arguments and `**` expands a dict
into keyword arguments:

```python
def connect(host, port, timeout=5): ...

args = ("db.local", 5432)
options = {"timeout": 10}
connect(*args, **options)       # == connect("db.local", 5432, timeout=10)

print(*["a", "b", "c"], sep="-")  # a-b-c
```

It's the same asterisk as in the **definition** `def f(*args, **kwargs)`, but in reverse: in
the definition it *collects* arguments and in the call it *expands* them.

## Combining collections with `*` and `**`

Inside list, tuple, set and dict literals, the asterisks "spill" the contents:

```python
a = [1, 2]
b = (3, 4)
everything = [*a, *b, 5]       # [1, 2, 3, 4, 5]
unique = {*a, *b}              # {1, 2, 3, 4}

defaults = {"debug": False, "port": 80}
config   = {"port": 8080}
final = {**defaults, **config, "host": "x"}
# {'debug': False, 'port': 8080, 'host': 'x'}  <- the right side overwrites the left
```

### The `|` operator for dicts (3.9+)

To merge dicts, `|` usually reads better than `{**a, **b}`:

```python
final = defaults | config          # new dict, modifies neither
defaults |= config                 # updates defaults in place (like .update)
```

Both forms create a **new** dict and don't mutate the originals, except `|=`, which does
modify the left one. Keep that difference in mind when you received the dict as a
parameter: modifying it is a side effect the caller doesn't expect.

## Unpacking what a function returns

Returning a tuple and unpacking it is the idiomatic way to return several values:

```python
def min_max(xs: list[int]) -> tuple[int, int]:
    return min(xs), max(xs)

lowest, highest = min_max([3, 1, 4])
quotient, remainder = divmod(17, 5)
```

If there are more than three values or they have meaning of their own, use a `NamedTuple`:
you can still unpack it like a tuple, and each field also gets a name (`r.quotient`). We'll
cover it in the modeling module.

## Common pitfalls

```python
# 1. Assuming *rest is a tuple: it's always a LIST
_, *rest = (1, 2, 3)
type(rest)                    # list

# 2. Forgetting the comma in a one-element tuple
(x,) = [42]                   # x = 42
x, = [42]                     # same thing, more cryptic

# 3. Mutating the dict you were given when merging
def apply(base, extra):
    base.update(extra)        # ✗ modifies the caller's dict
    return base

def apply(base, extra):
    return base | extra       # ✓ returns a new one
```

## Summary

| You want to…                          | Use                          |
|---------------------------------------|------------------------------|
| split the first from the rest         | `first, *rest = xs`          |
| keep only the ends                    | `first, *_, last = xs`       |
| swap values                           | `a, b = b, a`                |
| iterate over pairs                    | `for k, v in d.items()`      |
| pass a list as arguments              | `f(*items)`                  |
| pass a dict as keyword arguments      | `f(**options)`               |
| concatenate iterables                 | `[*a, *b]`                   |
| merge dicts without mutating          | `a | b` or `{**a, **b}`      |

## Exercise

You'll implement four functions that are solved with unpacking and no indexing.

**Further reading:** [PEP 3132 — Extended Iterable Unpacking](https://peps.python.org/pep-3132/),
[PEP 448 — Additional Unpacking Generalizations](https://peps.python.org/pep-0448/),
[PEP 584 — Add Union Operators To dict](https://peps.python.org/pep-0584/).
