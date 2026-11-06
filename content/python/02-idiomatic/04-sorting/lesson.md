# Sorting: sorted, key and comparisons

In Python you almost never write a comparison function. You sort by saying **which value**
to compare each element by, using the `key` parameter. That one idea covers everything from
"by age" to "by country ascending and date descending".

## `sorted` vs. `list.sort`

```python
nums = [3, 1, 2]

ordered = sorted(nums)    # returns a NEW list; nums doesn't change
nums.sort()               # sorts IN PLACE and returns None
```

- `sorted(iterable)` accepts **any iterable** (sets, dict keys, generators) and always
  returns a list.
- `items.sort()` only exists on lists, doesn't copy and returns `None`.

A classic mistake is `nums = nums.sort()`, which leaves `nums` as `None`. The stdlib
convention is that methods that mutate an object return `None`, precisely so they aren't
confused with the ones that return a new value.

Both accept the same parameters: `key` and `reverse`.

## `key`: sorting by a projection

`key` takes a function that is applied **once per element**. Sorting follows the value it
returns:

```python
words = ["banana", "Fig", "cherry", "éclair"]

sorted(words)                        # ['Fig', 'banana', 'cherry', 'éclair']  (by Unicode code point)
sorted(words, key=str.lower)         # ['banana', 'cherry', 'Fig', 'éclair']
sorted(words, key=len)               # ['Fig', 'banana', 'cherry', 'éclair']

people = [{"name": "Zoe", "age": 30}, {"name": "Alice", "age": 25}]
sorted(people, key=lambda p: p["age"])
```

> To sort text "like a dictionary" (with `é` next to `e`) you need `locale.strxfrm` or a
> library like PyICU. `str.lower` isn't enough for accented letters.

## Several keys: tuples

Tuples are compared **element by element**: first the first one and, if they tie, the
second, and so on. That lets you sort by several criteria by returning a tuple from `key`:

```python
# By age and, for equal ages, by name
sorted(people, key=lambda p: (p["age"], p["name"]))
```

### Mixing ascending and descending

`reverse=True` reverses **everything**. If you need one criterion descending and another
ascending, you have two options:

**1. Negate the numeric key.** This is the most direct when the descending key is a number:

```python
# Age descending, name ascending
sorted(people, key=lambda p: (-p["age"], p["name"]))
```

**2. Sort in several passes, taking advantage of stability.** Python's sort is **stable**:
if two elements tie on the key, they keep the relative order they came in with. So you can
sort first by the *least* important criterion and then by the *most* important one:

```python
res = sorted(people, key=lambda p: p["name"])                # secondary criterion
res = sorted(res, key=lambda p: p["age"], reverse=True)      # primary criterion
```

This second approach also works for keys that can't be negated, like strings.

## `operator.itemgetter` and `attrgetter`

For the typical "sort by a field" cases, the `operator` module has ready-made functions that
are also a bit faster than a lambda:

```python
from operator import attrgetter, itemgetter

sorted(rows, key=itemgetter("country"))            # == lambda r: r["country"]
sorted(rows, key=itemgetter("country", "city"))    # returns a tuple: several keys
sorted(tuples, key=itemgetter(1))                  # by the second element
sorted(users, key=attrgetter("last_name", "first_name"))
```

## `min`, `max` and `heapq` take `key` too

You don't need to sort everything to find an extreme:

```python
max(products, key=lambda p: p["price"])            # the most expensive: O(n)
min(words, key=len)                                # the shortest
max([], default=None)                              # avoids ValueError on empty input

import heapq
heapq.nlargest(3, products, key=lambda p: p["price"])     # top 3 without sorting everything
```

Sorting costs O(n log n). If you only want the maximum, `max` is O(n), and for "the k
largest" with a small k, `heapq.nlargest` is more efficient.

## Sorting dicts

A dict has no method to sort itself, but you can build a new one in whatever order you want,
because dicts keep insertion order:

```python
stock = {"pear": 3, "apple": 10, "grape": 7}

dict(sorted(stock.items()))                           # by key
dict(sorted(stock.items(), key=itemgetter(1)))        # by value
sorted(stock, key=stock.get, reverse=True)            # keys by value desc: ['apple', 'grape', 'pear']
```

## Common pitfalls

- `items = items.sort()` leaves the list as `None`.
- Mixing incomparable types: `sorted([1, "2"])` raises `TypeError` in Python 3.
- `None` in the data: `sorted([3, None])` fails. One fix is
  `key=lambda x: (x is None, x or 0)` to send the `None` values to the end.
- Sorting strings that hold numbers: `sorted(["10", "9"])` gives `['10', '9']`. If they're
  numbers, convert them in the key: `key=int`.

## Summary

| You want…                                | Use                                           |
|------------------------------------------|-----------------------------------------------|
| a sorted copy                            | `sorted(xs)`                                  |
| to sort in place                         | `xs.sort()`                                   |
| to sort by one field                     | `key=itemgetter("field")` / `attrgetter`      |
| to sort by several fields                | `key=lambda x: (x.a, x.b)`                    |
| one criterion desc and another asc       | negate the numeric one, or two stable passes  |
| only the maximum or minimum              | `max(xs, key=...)`, `min(...)`                |
| the k largest                            | `heapq.nlargest(k, xs, key=...)`              |

## Exercise

Four sorting functions: with compound keys, `max` with `key`, and `itemgetter`.

**Further reading:** [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html) (in the
official documentation, highly recommended).
