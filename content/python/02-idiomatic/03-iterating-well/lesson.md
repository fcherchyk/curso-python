# Iterating well: enumerate, zip and friends

Python's `for` is not a `for (i = 0; i < n; i++)`: it walks **elements**, not indices.
Almost all code that "smells like another language" comes from fighting that and rebuilding
indices by hand. This chapter covers the tools that save you from doing so: `enumerate`,
`zip`, `reversed`, `itertools.pairwise`, `any` and `all`.

## The `range(len(...))` anti-pattern

```python
# ✗ C style
for i in range(len(names)):
    print(names[i])

# ✓ Python
for name in names:
    print(name)
```

The indexed version is noisier, invites off-by-one errors and only works with indexable
sequences. The direct `for` works with **any iterable**: files, generators, sets, dict keys
or query results.

## `enumerate`: when you also need the index

```python
for i, name in enumerate(names):
    print(i, name)

for n, line in enumerate(file, start=1):      # number from 1
    print(f"{n:>4} | {line}", end="")
```

`enumerate` returns `(index, element)` pairs that get unpacked in the `for`. The `start`
parameter changes the number it counts from; it doesn't skip elements.

## `zip`: walking several sequences in parallel

```python
names  = ["alice", "bob", "carol"]
grades = [9, 7, 8]

for name, grade in zip(names, grades):
    print(name, grade)

dict(zip(names, grades))         # {'alice': 9, 'bob': 7, 'carol': 8}
```

### The length mismatch problem and `strict=True` (3.10+)

By default, `zip` **stops at the shortest sequence without warning**:

```python
list(zip([1, 2, 3], ["a", "b"]))                 # [(1, 'a'), (2, 'b')]  <- the 3 got lost!
list(zip([1, 2, 3], ["a", "b"], strict=True))    # ValueError
```

This causes silent bugs when two lists "should" have the same length but don't because of an
earlier mistake. **Rule of thumb:** if the sequences must be the same length, use
`strict=True`. If you want to pad the shorter one with a default value, there's
`itertools.zip_longest(a, b, fillvalue=None)`.

### `zip` to "unzip"

`zip(*pairs)` does the inverse operation: it turns a list of pairs into two tuples.

```python
pairs = [("alice", 9), ("bob", 7)]
names, grades = zip(*pairs)      # ('alice', 'bob'), (9, 7)
```

## Consecutive elements: `pairwise` (3.10+)

To compare each element with the next one, you don't need indices:

```python
from itertools import pairwise

temps = [18, 21, 19, 25]
[b - a for a, b in pairwise(temps)]    # [3, -2, 6]

# Before 3.10 (or with lists), the equivalent trick:
[b - a for a, b in zip(temps, temps[1:])]
```

`pairwise` works with any iterable, even generators that can't be sliced with `[1:]`.

## Iterating in reverse and in order

```python
for x in reversed(xs): ...        # without copying the list (xs[::-1] does copy)
for x in sorted(xs): ...          # walks a sorted copy; xs doesn't change
for k in sorted(d): ...           # a dict's keys in order
```

## `any` and `all`: questions about the whole collection

```python
any(n < 0 for n in nums)          # is there any negative?
all(u.active for u in users)      # are they all active?
```

Both **stop as soon as they know the answer**: `any` stops at the first true value and
`all` at the first false one. With a generator expression as the argument, they also don't
build any intermediate list.

Edge cases worth remembering: `any([])` is `False` and `all([])` is `True`. In an empty
collection there's no element that fails.

## Iterating over dicts

```python
for key in d:                     # keys (no need for .keys())
for value in d.values():
for key, value in d.items():
```

One trap: **don't add or remove keys from a dict while you iterate over it**, because
Python raises `RuntimeError: dictionary changed size during iteration`. If you need to,
iterate over a copy (`for k in list(d):`) or build a new dict with a comprehension.

## Summary

| Instead of                                  | Use                                     |
|---------------------------------------------|-----------------------------------------|
| `for i in range(len(xs)): xs[i]`            | `for x in xs`                           |
| keeping a counter by hand                   | `for i, x in enumerate(xs, start=1)`    |
| indices to walk two lists                   | `for a, b in zip(xs, ys, strict=True)`  |
| `xs[i+1] - xs[i]` with indices              | `for a, b in pairwise(xs)`              |
| `xs[::-1]` just to iterate                  | `reversed(xs)`                          |
| a loop with `flag = True` and `break`       | `any(...)` / `all(...)`                 |
| `if len(xs) == 0`                           | `if not xs`                             |

## Exercise

Four functions solved with `enumerate`, `zip` and `pairwise`, without `range(len(...))`.

**Further reading:** [Built-in functions: enumerate, zip](https://docs.python.org/3/library/functions.html#enumerate),
[PEP 618 — zip strict](https://peps.python.org/pep-0618/),
[itertools.pairwise](https://docs.python.org/3/library/itertools.html#itertools.pairwise).
