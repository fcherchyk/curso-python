# Dicts, defaultdict and Counter

The dict is Python's central data structure: objects, modules, namespaces and kwargs are all
implemented with dicts. Using it well, together with its variants from `collections`, removes
a lot of repetitive code: hand-rolled counters, `if key not in d` and `try/except KeyError`.

## The basics worth keeping fresh

- Dicts **keep insertion order** (guaranteed since 3.7).
- Keys must be **hashable**: `str`, `int`, `tuple` of hashables and `frozenset` work;
  `list`, `dict` and `set` don't.
- Lookup, insertion and deletion cost O(1) on average.
- `k in d` checks **keys** (no need for `.keys()`).

## Reading without crashing: `get`, `setdefault` and `pop`

```python
prices = {"bread": 1200}

prices["milk"]                   # KeyError
prices.get("milk")               # None
prices.get("milk", 0)            # 0

prices.pop("bread")              # 1200, and removes it
prices.pop("bread", None)        # None; without a default, raises KeyError
```

`setdefault(k, default)` returns the value of `k` and, if it doesn't exist, first inserts it
with `default`. It lets you group without an `if`:

```python
groups = {}
for word in words:
    groups.setdefault(word[0], []).append(word)
```

There's a catch: the `default` is **always** built, even if the key already exists. In the
example, an empty list is created on every iteration and almost always thrown away. For
grouping, `defaultdict` is cleaner.

## `defaultdict`: automatic default values

```python
from collections import defaultdict

groups = defaultdict(list)          # takes a FACTORY (list, int, set…), not a value
for word in words:
    groups[word[0]].append(word)

counts = defaultdict(int)           # int() == 0
for char in text:
    counts[char] += 1
```

When you access a missing key with `[]`, `defaultdict` calls the factory, stores the result
and returns it to you.

### Watch out for side effects

```python
d = defaultdict(list)
if d["x"]:          # this CREATES the key "x" with []!
    ...
"x" in d            # True
```

Reading with `[]` inserts the key. To check without modifying, use `in` or `.get()`. For the
same reason, **don't return a `defaultdict` from a public API**: whoever receives it may
create keys without noticing. Convert it first with `dict(groups)`.

## `Counter`: counting things

```python
from collections import Counter

c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

c["a"]             # 5
c["z"]             # 0  <- doesn't raise KeyError or insert the key
c.most_common(2)   # [('a', 5), ('b', 2)]
c.total()          # 11 (3.10+)
```

`most_common` sorts by count and, **on ties, keeps the order in which each element first
appeared**. That solves a "top N" without sorting by hand.

`Counter` also has multiset arithmetic:

```python
stock = Counter(apple=3, pear=1)
order = Counter(apple=2, pear=2)

stock - order       # Counter({'apple': 1})  <- drops counts <= 0
order - stock       # Counter({'pear': 1})   <- what's missing
stock + order       # adds counts
stock & order       # minimum of each
stock | order       # maximum of each
```

An empty (falsy) `order - stock` means "the stock is enough". It's a very handy trick for
anagram and availability problems.

## Building and inverting dicts

```python
dict(zip(keys, values))                     # from two lists
dict.fromkeys(["a", "b"], 0)                # {'a': 0, 'b': 0}
{v: k for k, v in d.items()}                # invert if the values are unique

# If values repeat, invert by grouping:
inverse = defaultdict(list)
for k, v in d.items():
    inverse[v].append(k)
```

> `dict.fromkeys(keys, [])` is a trap: **all** the keys share the same list. Use a
> comprehension: `{k: [] for k in keys}`.

## Merging and updating

```python
a | b          # new dict (3.9+); b overwrites a
a |= b         # updates a in place (like a.update(b))
{**a, **b}     # equivalent to a | b, before 3.9
```

## Other `collections` types worth knowing

| Type           | What for                                                              |
|----------------|-----------------------------------------------------------------------|
| `deque`        | queue with O(1) append/pop at both ends (covered in the algorithms module) |
| `ChainMap`     | look up several dicts in layers (e.g. config → env → defaults) without copying them |
| `OrderedDict`  | nearly obsolete: has `move_to_end`, and its equality takes order into account |
| `namedtuple`   | tuple with field names; `typing.NamedTuple` is usually preferred today |

## Summary

| You want to…                           | Use                                    |
|----------------------------------------|----------------------------------------|
| read with a default                    | `d.get(k, default)`                    |
| group                                  | `defaultdict(list)`, then `dict()`     |
| count                                  | `Counter(iterable)`                    |
| get the top N by frequency             | `Counter(...).most_common(n)`          |
| check whether the stock is enough      | `not (order - stock)`                  |
| remove without failing                 | `d.pop(k, None)`                       |

## Exercise

Four functions: grouping, counting words, inverting by grouping and an availability problem
using `Counter` arithmetic.

**Further reading:** [collections — Container datatypes](https://docs.python.org/3/library/collections.html),
*Fluent Python* (2nd ed.), ch. 3.
