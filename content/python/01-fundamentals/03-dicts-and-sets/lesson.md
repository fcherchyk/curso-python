# Dicts and Sets: The Essentials

Both are implemented with **hash tables**. That gives them O(1) average lookup, insertion and
deletion, and also the restriction that their keys or elements must be **hashable**. This
chapter covers the basics; the advanced patterns (`defaultdict`, `Counter`, merging with `|`)
are in module 02.

## Dicts: key → value mappings

```python
ages = {"alice": 31, "bob": 27}
ages["carol"] = 40             # insert or replace
ages["alice"]                  # 31
ages["zoe"]                    # KeyError
ages.get("zoe")                # None
ages.get("zoe", 0)             # 0
"alice" in ages                # True (searches the KEYS, in O(1))
del ages["bob"]
len(ages)                      # 2
```

Other ways to build them:

```python
dict(alice=31, bob=27)                   # with keywords (valid string keys)
dict([("alice", 31), ("bob", 27)])       # from pairs
dict(zip(names, ages))
{n: len(n) for n in names}               # comprehension
```

### Iterating over them

```python
for name in ages:                        # keys
for age in ages.values():
for name, age in ages.items():
```

`keys()`, `values()` and `items()` return **views**: they aren't copies but windows into the
dict that reflect changes. The `keys()` and `items()` views also support set operations:
`d1.keys() & d2.keys()` gives the keys they have in common.

### Order

Since Python 3.7, dicts **preserve insertion order**. Replacing the value of an existing key
doesn't change its position; deleting it and inserting it again sends it to the end.

## Hashable: what can be a key

An object is hashable if it has a `hash()` that never changes during its lifetime and it can
be compared with `==`. In practice:

- **Yes:** `int`, `float`, `str`, `bytes`, `bool`, `None`, `tuple` (if everything it contains
  is hashable), `frozenset`, your own classes (by default they hash by identity) and
  dataclasses with `frozen=True`.
- **No:** `list`, `dict`, `set`, that is, the mutable containers.

The rule makes sense: if a mutable key changed after being inserted, its hash would no longer
match the slot in the table where it was stored, and it could never be found again.

```python
{[1, 2]: "x"}          # TypeError: unhashable type: 'list'
{(1, 2): "x"}          # ✓
```

## Sets: collections without duplicates

```python
colors = {"red", "green"}
empty = set()                   # {} is an empty dict, not a set!
colors.add("blue")
colors.discard("black")         # doesn't fail if missing (remove would raise KeyError)
"red" in colors                 # O(1)

set([3, 1, 3, 2])               # {1, 2, 3}  removes duplicates
```

The main use case for a set is asking **"is X in here?"** many times. On a list, each `in`
is O(n); on a set, O(1). If you're going to search inside a loop, convert the list to a set
**once** beforehand:

```python
banned = set(banned_list)                         # O(n) just once
clean = [w for w in words if w not in banned]     # each `in` is O(1)
```

### Set algebra

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}

a | b     # {1, 2, 3, 4, 5}   union
a & b     # {3, 4}            intersection
a - b     # {1, 2}            difference (in a and not in b)
a ^ b     # {1, 2, 5}         symmetric difference (in only one)
{1, 2} <= a                   # subset
a.isdisjoint({9})             # no elements in common
```

The equivalent methods (`a.union(some_list)`, `a.intersection(...)`) accept any iterable, not
just sets.

### A set's order is not guaranteed

A set does **not** keep insertion order. If you need "unique items in the order they appear",
the idiomatic trick uses a dict, which does preserve it:

```python
list(dict.fromkeys(["b", "a", "b", "c", "a"]))    # ['b', 'a', 'c']
```

If the final result needs to be deterministic (for example, to compare it in a test), sort
it: `sorted(some_set)`.

### `frozenset`

It's the immutable, hashable version of a set. It can be a dict key or an element of another
set:

```python
seen_groups = {frozenset({"alice", "bob"})}
frozenset({"bob", "alice"}) in seen_groups      # True: order doesn't matter
```

## Choosing the structure

| You need…                                    | Use             |
|----------------------------------------------|-----------------|
| order and duplicates, access by position     | `list`          |
| a fixed record or a composite key            | `tuple`         |
| lookup by key with associated data           | `dict`          |
| fast membership, no duplicates               | `set`           |
| the same but immutable or as a key           | `frozenset`     |
| unique items preserving order                | `dict.fromkeys` |

## Summary

- Dicts and sets are hash tables: `in` costs O(1) and keys must be hashable.
- `d[k]` fails if the key doesn't exist; `d.get(k, default)` doesn't.
- `{}` is a dict; the empty set is `set()`.
- Sets have no order: for unique items in order, use `dict.fromkeys`.
- If you search a list many times, convert it to a set once.

## Exercise

Four functions you can solve with sets and dicts, no nested loops.

**Further reading:** [Mapping types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict),
[Set types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset).
