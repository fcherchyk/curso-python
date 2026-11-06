# Control Flow

Most of Python's control structures work like they do in any other language. This chapter
focuses on what's **specific to Python**: chained comparisons, the `else` on loops, the
conditional expression and a few patterns that avoid nesting.

## `if` / `elif` / `else`

```python
if temperature < 10:
    state = "cold"
elif temperature < 25:
    state = "mild"
else:
    state = "hot"
```

There's no classic `switch`. To branch on the shape of your data there's `match`, which we
cover in the modern Python module. To map simple values, a dict is often enough:

```python
PRICES = {"small": 100, "medium": 150, "large": 200}
price = PRICES.get(size, 0)
```

### Chained comparisons

```python
if 0 <= index < len(xs): ...      # same as 0 <= index and index < len(xs)
if a == b == c: ...
```

Each intermediate expression is evaluated **only once**. It's more readable and avoids
repeating the variable.

### Logical operators: they return operands, not `bool`

`and` and `or` short-circuit and **return one of the operands**:

```python
0 or "default"         # 'default'
"value" or "default"   # 'value'
[] and "never"         # []
user and user.name     # None if user is None, no AttributeError
```

`not` does always return `True` or `False`.

### Conditional expression (ternary)

```python
label = "even" if n % 2 == 0 else "odd"
```

Use it for simple values. If either branch needs logic, go back to `if`.

## Guard clauses: return early

Instead of nesting conditions, handle the special cases first and return:

```python
# ✗ Pyramid
def process(order):
    if order is not None:
        if order.items:
            if order.paid:
                return ship(order)
    return None

# ✓ Guards
def process(order):
    if order is None or not order.items:
        return None
    if not order.paid:
        return None
    return ship(order)
```

The "happy" path stays unindented and each condition reads on its own.

## `for`: iterates over iterables

```python
for x in [1, 2, 3]: ...
for i in range(5): ...              # 0..4
for i in range(10, 0, -2): ...      # 10, 8, 6, 4, 2
for c in "hello": ...
for line in open("data.txt"): ...
```

`break` exits the loop; `continue` skips to the next iteration.

### `for ... else`: the `else` almost nobody knows

A loop's `else` block runs **if the loop finished without `break`**:

```python
for user in users:
    if user.is_admin:
        print("found an admin:", user)
        break
else:
    print("there are no admins")
```

It's the "search, and act if not found" pattern, without a `found = False` variable. Think
of it as "if there was no break". Since many people find it confusing, keep it for short
searches and, if you use it, add a comment. Sometimes it's clearer to extract a function and
use `return`, or `any()` or `next(...)`.

## `while`

```python
attempts = 0
while attempts < 3:
    if connect():
        break
    attempts += 1
else:
    raise ConnectionError("could not connect")   # while/else exists too
```

Use `while` when you **don't know in advance** how many iterations you'll need: retries,
reading until a sentinel or algorithms that converge. To iterate over collections, always
use `for`.

The walrus operator (`:=`, 3.8+) avoids duplicating the read:

```python
while (line := file.readline()):
    process(line)
```

## `pass`, `...` and empty blocks

Python doesn't allow empty blocks. For a block that has no code yet, you use `pass` (or `...`,
very common in stubs and protocols):

```python
def to_be_implemented():
    ...

class MyError(Exception):
    pass
```

## Scopes: blocks don't create a scope

Unlike C or Java, **`if`, `for` and `while` don't create a new scope**. Variables defined
inside them still exist outside:

```python
for i in range(3):
    last = i
print(i, last)     # 2 2
```

Python has only four scopes: local (function), enclosing (outer functions), global (module)
and built-in, the **LEGB** rule we'll revisit with closures.

## Summary

- Chained comparisons: `0 <= i < n`.
- `and`/`or` return operands: `x or default`.
- Guards with early returns instead of nested `if`s.
- `for/else` and `while/else`: the `else` runs if there was no `break`.
- `while` only when you don't know how many iterations; walrus for "read while there's data".
- Blocks don't create a scope.

## Exercise

Four classic control-flow functions, written idiomatically.

**Further reading:** [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
(official tutorial).
