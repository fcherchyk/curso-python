# Comprehensions

A *comprehension* builds a new collection from an iterable in a single expression. It's
the idiomatic way to do "map + filter" in Python. Used well, it replaces four- or five-line
loops with one line that reads almost like the mathematical definition of a set.

## The idea: from loop to expression

This is the pattern comprehensions replace:

```python
result = []
for x in nums:
    if x % 2 == 0:
        result.append(x * x)
```

The comprehension version reads in the same order: *what* gets produced, *where* it comes
from and *under what condition*:

```python
result = [x * x for x in nums if x % 2 == 0]
#         ^^^^^ ^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^
#         expr  iteration      filter (optional)
```

Besides being shorter, it has three concrete advantages:

1. **Explicit intent.** A `for` with `append` could be doing anything, so you have to read
   all of it. A comprehension always builds a collection, and that's obvious up front.
2. **No intermediate state.** There's no empty list that gets filled up later: the result
   either exists in full or doesn't exist at all.
3. **It's faster.** It runs specialized bytecode and avoids looking up `result.append` on
   every iteration. This usually isn't the deciding factor, but it helps.

## The four flavors

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

squares  = [x * x for x in nums]                  # list
unique   = {x for x in nums}                      # set  -> {1, 2, 3, 4, 5, 6, 9}
by_name  = {u.name: u for u in users}             # dict
total    = sum(x * x for x in nums)               # generator expression
```

- **List** `[...]`: the general case. Keeps order and allows duplicates.
- **Set** `{...}`: removes duplicates. Good for questions like "which domains show up?".
- **Dict** `{k: v ...}`: builds indexes and mappings. If a key repeats, **the last one wins**.
- **Generator expression** `(...)`: builds nothing in memory. It produces values one at a
  time when someone asks for them. If it's the only argument to a function, you can drop the
  extra parentheses: `sum(x for x in xs)`, `any(...)`, `max(...)`, `"".join(...)`.

> There's no "tuple comprehension". `(x for x in xs)` is a generator; if you need a tuple,
> use `tuple(x for x in xs)`.

## Filtering vs. transforming conditionally

An `if` can go in two places, and they do different things:

```python
# Filter: the if goes AT THE END. It drops elements.
[x for x in nums if x > 2]              # [3, 4, 5, 9, 6]

# Conditional expression: the if/else goes AT THE START. It transforms every element.
["even" if x % 2 == 0 else "odd" for x in nums]
```

The filter takes no `else`; the conditional expression always needs one. You can combine
both, but by then it's worth asking whether a loop would read better.

## Nested comprehensions

The `for` clauses are written **in the same order you'd nest them** as loops:

```python
matrix = [[1, 2, 3], [4, 5, 6]]

# for row in matrix:
#     for x in row:
#         ...
flat = [x for row in matrix for x in row]         # [1, 2, 3, 4, 5, 6]

# A comprehension INSIDE another one builds nested structures:
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4], [2, 5], [3, 6]]
```

The first form (two `for` clauses in a row) **flattens**. The second (a comprehension as the
expression of another) **nests**. They're easy to mix up: when in doubt, write out the loops
on paper.

## Dict comprehensions: common patterns

```python
prices = {"bread": 1200, "milk": 1500, "coffee": 9800}

# Invert a dict (only if the values are unique and hashable)
by_price = {v: k for k, v in prices.items()}

# Filter a dict
expensive = {k: v for k, v in prices.items() if v > 1400}

# Transform values
with_tax = {k: round(v * 1.21) for k, v in prices.items()}

# Index by id from a list of objects
by_id = {p.id: p for p in products}
```

To build a dict from **pairs** you already have, you don't need a comprehension:
`dict(zip(keys, values))` is more direct.

## Variable scope

Since Python 3, a comprehension's variable is **local** to the comprehension and doesn't
"leak" outside:

```python
x = "outside"
squares = [x * x for x in range(3)]
print(x)   # "outside"
```

A regular `for` loop, on the other hand, leaves the variable defined with its last value.
One more point in favor of comprehensions.

## When NOT to use them

- **For side effects.** `[print(x) for x in xs]` creates a list of `None` that gets thrown
  away. If what you want is to *do* something, use a `for`.
- **When the logic doesn't fit on one readable line.** As a rule of thumb, more than one `if`
  or more than two `for` clauses is a sign you want a loop or a named helper function.
- **When you need to stop early.** A comprehension goes through everything. For "the first
  element that satisfies X", use `next((x for x in xs if cond(x)), None)`.
- **With huge data you'll go through only once.** That's where a generator expression pays
  off: `sum(len(l) for l in file)` doesn't load the whole file into memory.

## Common pitfalls

```python
# 1. Nested for clauses in the wrong order -> NameError or a wrong result
[x for x in row for row in matrix]        # ✗ `row` doesn't exist yet

# 2. Forgetting that a set loses order
{x for x in [3, 1, 2]}                    # iteration order is not guaranteed

# 3. Repeated keys in dict comprehensions: the last one overwrites
{len(p): p for p in ["ab", "cd"]}         # {2: 'cd'}

# 4. Consuming a generator expression twice
gen = (x * 2 for x in range(3))
list(gen)   # [0, 2, 4]
list(gen)   # []  <- already exhausted
```

## Summary

| You want to…                         | Use                                   |
|--------------------------------------|---------------------------------------|
| transform and/or filter a list       | `[f(x) for x in xs if cond(x)]`       |
| get unique values                    | `{f(x) for x in xs}`                  |
| build an index or mapping            | `{k(x): v(x) for x in xs}`            |
| aggregate (sum, max, all/any)        | `sum(f(x) for x in xs)`               |
| flatten one level                    | `[y for x in xs for y in x]`          |
| find the first match                 | `next((x for x in xs if c(x)), None)` |

## Exercise

In the **Code** tab you'll implement four functions, each with a single comprehension:
filter and transform, flatten, invert a dict and extract unique values.

**Further reading:** [Python Tutorial — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions),
*Fluent Python* (2nd ed.), ch. 2.
