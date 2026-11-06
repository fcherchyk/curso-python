# Lists, Tuples and Slicing

Lists and tuples are the two general-purpose sequences. Their syntax is very similar, but
they play different roles. In this chapter we review when to use each one, the operations
worth keeping at hand (and what they cost), and *slicing*, which works the same on lists,
tuples, strings and `range`.

## List vs. tuple: it's not just "mutable vs. immutable"

```python
prices = [1200, 1500, 980]           # list: HOMOGENEOUS collection of variable length
point  = (3.5, -1.2)                 # tuple: HETEROGENEOUS record of fixed length
person = ("Alice", 31, "Chicago")    # each position has a meaning
```

- Use a **list** when you have "many of the same thing" and you'll add, remove or sort.
- Use a **tuple** when each position means something different, like a row, a key-value
  pair or a point. Being immutable is a benefit: it can be used as a dict key or a set
  element, and nobody can change it on you.

```python
distances = {("NYC", "Boston"): 215}      # tuple as a key: ✓
distances = {["NYC", "Boston"]: 215}      # TypeError: unhashable type: 'list'
```

Tuple syntax details:

```python
t = 1, 2          # the parentheses are optional; the comma is what creates the tuple
one = (42,)       # single-element tuple: the comma is required
(42)              # this is just the int 42
empty = ()
```

## List operations and their cost

| Operation                      | Cost      | Note                                       |
|--------------------------------|-----------|--------------------------------------------|
| `xs[i]`, `xs[i] = v`           | O(1)      |                                            |
| `xs.append(x)`                 | O(1)*     | amortized                                  |
| `xs.pop()`                     | O(1)      | removes from the end                       |
| `xs.pop(0)`, `xs.insert(0, x)` | **O(n)**  | shifts every element: use `deque`          |
| `x in xs`                      | **O(n)**  | linear search: use a `set`                 |
| `xs.extend(ys)` / `xs += ys`   | O(len ys) |                                            |
| `xs.sort()`                    | O(n log n)|                                            |
| `len(xs)`                      | O(1)      |                                            |

Python lists are **dynamic arrays**, not linked lists. Working at the end is cheap; at the
front it's expensive. If you need a queue, `collections.deque` has `appendleft` and
`popleft` in O(1).

```python
xs = [3, 1, 2]
xs.append(4)          # [3, 1, 2, 4]
xs.extend([5, 6])     # adds each element (append would add the whole list)
xs.insert(1, 9)       # inserts at position 1
xs.remove(9)          # removes the FIRST occurrence of the value (ValueError if missing)
xs.pop()              # removes and returns the last one
xs.index(2)           # position of the first occurrence
xs.count(1)
del xs[0]             # delete by index
```

## Negative indexing

```python
xs = ["a", "b", "c", "d"]
xs[-1]    # 'd'  last
xs[-2]    # 'c'  second to last
```

`xs[-k]` is equivalent to `xs[len(xs) - k]`.

## Slicing: `[start:stop:step]`

A slice returns a **new** sequence of the same type. `start` is inclusive and `stop`
exclusive, just like `range`:

```python
xs = [0, 1, 2, 3, 4, 5]

xs[1:4]     # [1, 2, 3]
xs[:3]      # [0, 1, 2]       the first 3
xs[3:]      # [3, 4, 5]       from 3 to the end
xs[-2:]     # [4, 5]          the last 2
xs[:-2]     # [0, 1, 2, 3]    all but the last 2
xs[::2]     # [0, 2, 4]       every other one
xs[::-1]    # [5, 4, 3, 2, 1, 0]  reversed
xs[:]       # shallow copy
```

One nice property is that slicing **never raises `IndexError`**: out-of-range bounds are
clamped.

```python
xs[10:20]   # []
xs[:100]    # the whole list
```

A good way to think about indices is that they mark the **edges between elements**, not the
elements themselves:

```
 +---+---+---+---+
 | a | b | c | d |
 +---+---+---+---+
 0   1   2   3   4
-4  -3  -2  -1
```

So `xs[1:3]` is the elements between edge 1 and edge 3: `b, c`. And `xs[:k] + xs[k:]`
always rebuilds the full list.

### The `xs[-n:]` trap with `n = 0`

```python
n = 0
xs[-n:]     # the whole list! because -0 == 0 and xs[0:] is everything
```

If `n` can be 0, write it as `xs[len(xs) - n:]`.

### Assigning to a slice (lists only)

```python
xs = [0, 1, 2, 3, 4]
xs[1:3] = ["a", "b", "c"]   # replaces (the length can change): [0, 'a', 'b', 'c', 3, 4]
xs[:] = []                  # empties the list IN PLACE (other names see the change)
del xs[::2]                 # deletes every other element
```

## Sequence operators

```python
[1, 2] + [3]         # [1, 2, 3]   concatenates (creates a new one)
[0] * 3              # [0, 0, 0]   repeats (careful repeating lists, see previous chapter)
(1, 2) < (1, 3)      # True        lexicographic comparison
3 in (1, 2, 3)       # True
min(xs), max(xs), sum(xs), len(xs)
```

## `range`: a lazy sequence

`range(start, stop, step)` doesn't create a list: it computes values on demand. `range(10**12)`
takes up the same space as `range(10)`. It supports `len`, `in` (O(1) for integers), indexing
and slicing.

## Summary

- List for homogeneous collections that change; tuple for fixed-length records (and as a
  dict key).
- Working at the end of a list is O(1); at the front, O(n) (that's what `deque` is for).
- `x in some_list` is O(n): if you search a lot, use a `set`.
- Slicing: `[start:stop:step]`, exclusive stop, never fails on range and returns a copy.
- `xs[::-1]` reverses; `xs[:]` copies; `xs[-n:]` breaks with `n = 0`.

## Exercise

Four functions you can solve with slicing, no loops.

**Further reading:** [Sequence types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range),
[TimeComplexity (Python wiki)](https://wiki.python.org/moin/TimeComplexity).
