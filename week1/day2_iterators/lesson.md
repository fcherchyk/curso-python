# Day 2: Iterators, generators and itertools

**Goal:** understand the iteration protocol and use lazy pipelines, which is what separates
Python code that scales from code that loads everything into memory.

## 1. Iterable vs. iterator

- **Iterable:** has `__iter__()` and returns a new iterator, for example `list`, `dict`,
  `str`, `range` or a file.
- **Iterator:** has `__next__()` (and an `__iter__` that returns `self`). It is **consumed once**.

```python
it = iter([1, 2])
next(it)  # 1
next(it)  # 2
next(it)  # StopIteration
```

A `for` loop does exactly that: it calls `iter()` and then `next()` until `StopIteration`.

**Trap:** if a function receives an iterator (for example a generator) and walks it twice,
the second pass is empty. If you need to walk it twice, ask for a collection or
materialize it with `list()`.

## 2. Generators

A function with `yield` returns a generator: an iterator that runs the body piece by piece.

```python
def read_large(path):
    with open(path) as f:
        for line in f:  # the file is already a lazy iterator
            yield line.rstrip()


def tree(node):
    yield node
    for child in node.children:
        yield from tree(child)  # delegates to another iterable
```

Generator expressions: `(f(x) for x in xs if cond(x))`. If it is the only argument, you don't
need extra parentheses: `sum(x * x for x in xs)`.

## 3. Lazy pipelines

```python
lines = open("access.log")
records = (parse(l) for l in lines)
errors = (r for r in records if r.status >= 500)
first = list(itertools.islice(errors, 10))  # reads only what's needed
```

Nothing runs until someone asks for items. With this pattern you can process a 50 GB file
in constant memory.

## 4. itertools and friends (the most used ones)

| Function                       | What for                                           |
|--------------------------------|----------------------------------------------------|
| `islice(it, n)`                | slice an iterator (it doesn't support `it[:n]`)    |
| `count()`, `cycle()`, `repeat()` | infinite sequences                               |
| `chain(a, b)` / `chain.from_iterable` | concatenate iterables                       |
| `groupby(it, key)`             | group **consecutive** items (sort first if needed) |
| `pairwise(it)` (3.10)          | `(a, b), (b, c), ...`                              |
| `batched(it, n)` (3.12)        | batches of size n                                  |
| `combinations`, `permutations`, `product` | combinatorics                           |
| `accumulate(it)`               | running sums (or any binary function)              |
| `zip_longest`                  | zip that pads the shorter one                      |

`any()`, `all()`, `sum()`, `min()`, `max()` and `sorted()`, which consume iterables, are useful
too, and so is `collections.deque(maxlen=n)` for windows.

## 5. Walrus in loops (a preview of day 5)

```python
while batch := tuple(islice(it, n)):
    process(batch)
```

## Exercises

```bash
uv run pytest week1/day2_iterators
```

**Extra challenge:** rewrite `in_batches` with `itertools.batched` and `sliding_windows` without
`deque`, using `itertools.tee` + `islice`.

## Further reading

- [itertools docs](https://docs.python.org/3/library/itertools.html). The "Itertools
  Recipes" section is gold.
- *Fluent Python*, ch. 17 ("Iterators, Generators, and Classic Coroutines").
