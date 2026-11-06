# Day 1: Idiomatic Python

**Goal:** get back to writing Python that "reads like Python", not like translated Java or C.
**Time:** about 20 min of reading and 40 min of exercises.

## 1. Comprehensions

```python
squares = [x * x for x in nums if x % 2 == 0]  # list
by_id = {u.id: u for u in users}  # dict
domains = {email.split("@")[1] for email in emails}  # set
total = sum(p.price for p in products)  # generator (no brackets)
flat = [x for row in matrix for x in row]  # nested: same order as the for loops
```

Rule of thumb: if the comprehension needs more than one `if` or two `for`s, use a regular loop
or a helper function.

## 2. Unpacking

```python
a, b = b, a  # swap
first, *rest = [1, 2, 3]  # first=1, rest=[2, 3]
*init, last = "abc"  # init=['a', 'b'], last='c'
for i, (x, y) in enumerate(points):
    ...
merged = {**defaults, **config}  # or better in 3.9+: defaults | config
call(*args, **kwargs)
```

## 3. Iterating well

| Instead of                                   | Use                                          |
|----------------------------------------------|----------------------------------------------|
| `for i in range(len(xs)): xs[i]`              | `for x in xs` / `for i, x in enumerate(xs)`  |
| indices to walk two lists                    | `zip(a, b, strict=True)` (3.10+)             |
| `if len(xs) == 0`                            | `if not xs`                                  |
| `d.has_key(k)` / `k in d.keys()`             | `k in d`                                     |
| `try: d[k] except KeyError: d[k] = []`       | `d.setdefault(k, [])` or `defaultdict(list)` |
| counting by hand with a dict                 | `Counter(xs)`, `.most_common(n)`             |

`zip(strict=True)` raises `ValueError` if the lengths don't match. Without `strict`, the leftover
items are silently dropped, a classic source of bugs.

## 4. Sorting

```python
sorted(people, key=lambda p: p.age)  # asc
sorted(people, key=lambda p: (-p.age, p.name))  # age desc, name asc
sorted(words, key=str.lower)
max(products, key=lambda p: p.price)
from operator import attrgetter, itemgetter

sorted(rows, key=itemgetter("country", "city"))
```

Python's sort is **stable**, so you can chain sorts by several keys
(from the least to the most important).

## 5. Function signatures

```python
def f(pos_only, /, normal, *args, kw_only, **kwargs): ...
```

- Everything before `/` is **positional-only** (3.8+).
- Everything after `*` or `*args` is **keyword-only**. This is useful for boolean flags:
  `connect(host, timeout=5, retry=True)` reads much better than `connect(host, 5, True)`.
- **Classic trap:** mutable defaults are evaluated only once.

```python
def bad(x, acc=[]):          # the same list is shared across calls
def good(x, acc=None):
    acc = [] if acc is None else acc
```

## 6. Dicts

- They keep insertion order (guaranteed since 3.7).
- `d | other` returns a new one and `d |= other` updates in place (3.9+).
- `d.get(k, default)`, `d.setdefault(k, [])`, `d.pop(k, None)`.

## 7. Strings

```python
f"{name!r} is {age} years old"  # !r uses repr
f"{price:,.2f}"  # 1,234.50
f"{x=}"  # debug: prints "x=42" (3.8+)
"-".join(parts)  # never concatenate in a loop
s.removeprefix("http://")  # 3.9+
```

## Exercises

Open `exercises.py`, implement each function and run:

```bash
uv run pytest week1/day1_idiomatic          # the whole day
uv run pytest week1/day1_idiomatic -x       # stop at the first failure
uv run pytest week1/day1_idiomatic -k url   # only tests matching "url"
```

**Extra challenge:** no solution longer than 3 lines, except `build_url`.

## Further reading

- [Python Tutorial: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- *Fluent Python* (2nd ed.), ch. 2 and 3.
- *Effective Python* (3rd ed.), items on comprehensions and keyword-only arguments.
