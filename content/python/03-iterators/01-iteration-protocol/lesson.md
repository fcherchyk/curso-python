# The iteration protocol

Every Python `for` loop relies on two methods: `__iter__` and `__next__`. Knowing them explains
why a generator "runs dry" after the first pass, why a list can be iterated any number of
times, and how to make your own classes work with `for`, `list()`, `sum()`, `in` and
unpacking.

## Iterable vs. iterator

These are two different roles, and it pays to keep them apart:

- An **iterable** is something you *can iterate over*: it implements `__iter__()`, which returns
  a **new iterator**. Examples: `list`, `tuple`, `str`, `dict`, `set`, `range` or a file.
- An **iterator** is what *keeps track* of the iteration: it implements `__next__()`, which
  returns the next element or raises `StopIteration` when there are none left. Its
  `__iter__()` also returns `self`.

```python
nums = [10, 20]          # iterable
it = iter(nums)          # calls nums.__iter__() → a list_iterator
next(it)                 # 10
next(it)                 # 20
next(it)                 # StopIteration
next(it, "end")          # 'end'  ← next with a default doesn't raise
```

## What a `for` loop really does

```python
for x in collection:
    body(x)
```

is equivalent to:

```python
it = iter(collection)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    body(x)
```

That's the whole protocol. Any object that follows `__iter__`/`__next__` works in a
`for` loop, in comprehensions, in `list(...)`, `sum(...)`, `zip(...)`, `in` and in
unpacking `a, b = obj`.

## The difference that matters: iterators get consumed

An **iterable** hands you a new iterator every time you ask for one, so it can be
iterated many times. An **iterator** returns itself, so it can be iterated **only
once**:

```python
nums = [1, 2, 3]
list(nums), list(nums)        # ([1, 2, 3], [1, 2, 3])

it = iter(nums)
list(it), list(it)            # ([1, 2, 3], [])   ← the second one is empty

gen = (x * 2 for x in nums)   # generators are iterators
sum(gen), sum(gen)            # (12, 0)
```

This is a very common bug: a function that takes "something iterable" and iterates over it
twice (say, to compute the total and then each percentage) works with lists and fails
**silently** with generators. If you need two passes, materialize up front with
`data = list(data)`, or ask for a `Sequence` in the type annotation.

## Implementing your own iterable

The simplest and most robust approach is to make `__iter__` a **generator** (a function with
`yield`, next chapter). Every call to `iter()` creates a new one:

```python
class Playlist:
    def __init__(self, songs: list[str]) -> None:
        self._songs = songs

    def __iter__(self):
        for s in self._songs:
            yield s
        # or simply: return iter(self._songs)

p = Playlist(["a", "b"])
list(p), list(p)        # (['a', 'b'], ['a', 'b'])  ✓ can be iterated many times
```

## Implementing an iterator by hand

To understand the protocol (or when you need explicit state), you can write the full
iterator class:

```python
class Count:
    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self              # an iterator is its own iterable

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value
```

In practice you almost never need this: generators do the same with less code.
But when you see `__next__` in a library, you'll know what's going on.

## "Easy" iterables: `__getitem__` and `__len__`

For historical compatibility, if a class has no `__iter__` but does have `__getitem__` taking
indexes 0, 1, 2… until an `IndexError`, Python can iterate over it too. Today you should
implement `__iter__` explicitly: it's clearer and works with any data source.

## `iter()` with a sentinel

`iter(function, sentinel)` creates an iterator that calls `function()` until it returns the
sentinel. It's very handy for reading in chunks:

```python
from functools import partial

with open("big.bin", "rb") as f:
    for chunk in iter(partial(f.read, 4096), b""):
        process(chunk)
```

## Tools that consume iterables

`list`, `tuple`, `set`, `dict`, `sum`, `min`, `max`, `any`, `all`, `sorted`, `"".join`,
`enumerate`, `zip`, `map`, `filter`, `reversed` (this last one needs a sequence or
`__reversed__`) and all of `itertools`. If your class implements `__iter__`, it works with all of them.

## Summary

- Iterable: `__iter__` returns a **new** iterator. Iterator: `__next__` plus an
  `__iter__` that returns `self`.
- Iterators (generators included) are consumed only once.
- If you need to iterate twice, materialize with `list()`.
- For your own classes, implement `__iter__` as a generator.
- `next(it, default)` avoids the `StopIteration`.

## Exercise

An iterable class that can be iterated many times, a hand-written iterator and two
functions that use `next()` and `iter()`.

**Further reading:** [Iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types),
*Fluent Python* (2nd ed.), ch. 17.
