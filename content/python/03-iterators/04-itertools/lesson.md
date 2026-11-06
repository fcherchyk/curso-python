# itertools: the building blocks

`itertools` is a stdlib module with building blocks for iterators: they're
implemented in C, they're lazy and they combine with each other. Many loops with helper
variables, indexes and `if`s boil down to one or two `itertools` functions. This chapter
covers the most used ones, grouped by what they're for.

## Cutting and skipping

```python
from itertools import islice, takewhile, dropwhile

islice(it, 5)              # the first 5
islice(it, 2, 8, 2)        # like [2:8:2], but lazy
takewhile(lambda x: x < 10, nums)   # while it holds; stops at the first one that fails
dropwhile(lambda l: l.startswith("#"), lines)   # skips the comment header
```

`takewhile` and `dropwhile` only look at **the prefix**: once the condition changes, they
don't evaluate it again. They're not a `filter`.

## Infinite iterators

```python
from itertools import count, cycle, repeat

count(10, 5)               # 10, 15, 20, ...
cycle(["red", "green"])    # red, green, red, green, ...
repeat("x", 3)             # x, x, x   (without the 3 it's infinite)

for i, parity in zip(count(1), cycle(["odd", "even"])): ...
```

Always combine them with something that stops them: `islice`, `zip` with a finite iterable, `takewhile` or
a `break`.

## Joining

```python
from itertools import chain

chain([1, 2], (3,), range(4, 6))          # 1, 2, 3, 4, 5
chain.from_iterable(list_of_lists)        # flattens one level, lazily
```

`chain.from_iterable` is the lazy version of `[x for sub in xs for x in sub]`.

## Grouping: `groupby`

`groupby(iterable, key)` groups **consecutive** elements that share the same key:

```python
from itertools import groupby

for letter, group in groupby("aaabccaa"):
    print(letter, list(group))
# a ['a', 'a', 'a']
# b ['b']
# c ['c', 'c']
# a ['a', 'a']        ← 'a' again! it only groups CONSECUTIVE ones
```

To group "everything with the same key", **sort by that key first**, or use
a `defaultdict(list)`:

```python
sales.sort(key=lambda s: s.month)
for month, month_sales in groupby(sales, key=lambda s: s.month):
    print(month, sum(s.amount for s in month_sales))
```

Another trap: each `group` is an iterator that shares the underlying iterator. If you move on to
the next group, the previous one is left empty. If you need it later, convert it to a list.

## Windows and pairs

```python
from itertools import pairwise, batched     # pairwise 3.10+, batched 3.12+

list(pairwise([1, 2, 3, 4]))      # [(1, 2), (2, 3), (3, 4)]
list(batched(range(7), 3))        # [(0, 1, 2), (3, 4, 5), (6,)]
```

There's no built-in function for sliding windows of size `n`. The recipe uses
`collections.deque(maxlen=n)`, which drops the oldest element when you add a new one:

```python
from collections import deque

def windows(it, n):
    window = deque(maxlen=n)
    for x in it:
        window.append(x)
        if len(window) == n:
            yield tuple(window)
```

## Accumulating

```python
from itertools import accumulate
import operator

list(accumulate([1, 2, 3, 4]))                   # [1, 3, 6, 10]   running sums
list(accumulate([3, 1, 4, 1, 5], max))           # [3, 3, 4, 4, 5] max so far
list(accumulate([1, 2, 3], operator.mul))        # [1, 2, 6]
list(accumulate([100, -30, 50], initial=1000))   # [1000, 1100, 1070, 1120]
```

## Combinatorics

```python
from itertools import product, permutations, combinations, combinations_with_replacement

list(product("ab", [1, 2]))       # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]  nested loops
list(product([0, 1], repeat=3))   # all 8 combinations of 3 bits
list(permutations("abc", 2))      # 6: order matters
list(combinations("abc", 2))      # 3: [('a','b'), ('a','c'), ('b','c')]
```

`product` replaces nested `for` loops. Watch the size: permutations grow
factorially. They're lazy, but iterating over all of them may never finish in practice.

## Other useful ones

| Function                      | What it's for                                    |
|-------------------------------|--------------------------------------------------|
| `zip_longest(a, b, fillvalue=)`| zip that pads the shorter one                   |
| `starmap(f, pairs)`           | `f(*pair)` for each pair                         |
| `compress(data, mask)`        | filters according to a list of booleans          |
| `tee(it, n)`                  | duplicates an iterator (keeps in memory what one has read and the other hasn't) |
| `filterfalse(pred, it)`       | the opposite of `filter`                         |

The official docs have an **"Itertools Recipes"** section with dozens of functions
built from these pieces (`unique_everseen`, `sliding_window`, `roundrobin`…). The
`more-itertools` package also ships them ready-made.

## Summary

- Cutting: `islice`, `takewhile`, `dropwhile`. Joining: `chain`. Infinite: `count`, `cycle`, `repeat`.
- `groupby` only groups **consecutive** elements: sort first.
- `pairwise`, `batched` and the windows recipe with `deque(maxlen=n)`.
- `accumulate` for running totals; `product`, `permutations` and `combinations` for
  combinatorics.
- Everything is lazy: combine it with something that stops it.

## Exercise

Four functions you can solve with one or two `itertools` pieces.

**Further reading:** [itertools](https://docs.python.org/3/library/itertools.html),
especially the recipes section.
