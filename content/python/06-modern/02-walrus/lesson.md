# The walrus operator `:=`

The `:=` operator (3.8), nicknamed *walrus* because of its shape, **assigns and returns** the
value inside an expression. Its goal isn't to save a line but to **remove duplication**: to
avoid computing the same thing twice or repeating a read before and inside a loop.

## How it differs from `=`

`=` is a **statement**: you can't use it inside an `if`, a `while` or a comprehension. `:=` is
an **expression**: it produces a value and, along the way, stores it in a name.

```python
if (n := len(data)) > 10:
    print(f"too much data: {n}")
```

Without walrus you'd have to compute `len(data)` twice or add a line before the `if`.

## Case 1: read until there's nothing left

The classic "read, check, process, read again" pattern:

```python
# Without walrus: the read is duplicated
chunk = file.read(4096)
while chunk:
    process(chunk)
    chunk = file.read(4096)

# With walrus: a single read
while chunk := file.read(4096):
    process(chunk)
```

It works with any source that returns something falsy when it's done: `readline()`,
`queue.get()` with a sentinel, `socket.recv()` or `tuple(islice(it, n))` for batches.

## Case 2: regex

```python
import re

if m := re.match(r"(\d{4})-(\d{2})", text):
    year, month = m.groups()
```

`re.match` returns a `Match` or `None`. With walrus, the check and the use stay together.

Chained with `elif`:

```python
if m := DATE_PATTERN.match(line):
    ...
elif m := TIME_PATTERN.match(line):
    ...
```

## Case 3: comprehensions that filter on a computed value

```python
# Without walrus: parse() is called TWICE per element
results = [parse(x) for x in data if parse(x) is not None]

# With walrus: just once
results = [r for x in data if (r := parse(x)) is not None]
```

This matters when the function is expensive or has side effects.

## Case 4: `any()` and "which one was it?"

```python
if any((length := len(line)) > 80 for line in lines):
    print(f"there's a line with {length} characters")
```

Since `any` stops at the first true value, the variable keeps the value that triggered it. A
name assigned inside a comprehension or generator is available **outside** it (unlike the
`for` variable), precisely to allow this pattern.

## Rules and parentheses

- As a standalone statement, `x := 5` is a syntax error (use `=`). In arguments and
  comparisons you usually need parentheses: `if (n := len(xs)) > 10`.
- Without parentheses, `if n := len(xs) > 10` assigns the **boolean** `len(xs) > 10` to `n`.
  It's a classic bug.
- You can't use it to assign attributes or indexes: `self.x := 1` isn't valid.

## When **not** to use it

```python
# ✗ Adds nothing: it's a disguised =
print(total := compute())

# ✗ Several assignments on one line: hard to read
if (a := f()) and (b := g(a)) and (c := h(b)): ...
```

Rule of thumb: use it if it **removes** duplication or a line that only existed to set up an
`if` or a `while`. If you have to stop and think to read it, write it in two lines.

## Summary

- `:=` assigns and returns the value inside an expression.
- Typical cases: `while x := read()`, `if m := re.match(...)` and filtering on a computed
  value in a comprehension.
- Parentheses: `if (n := len(xs)) > 10`. Without them, `n` gets the boolean.
- Use it to remove duplication, not to make code more compact.

## Exercise

Read in chunks, filter while computing just once, extract data with a regex and write a retry
loop, all with walrus.

**Further reading:** [PEP 572 — Assignment Expressions](https://peps.python.org/pep-0572/).
