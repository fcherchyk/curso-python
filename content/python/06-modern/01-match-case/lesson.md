# Pattern matching: `match` / `case`

`match` (3.10) **is not a `switch`**. It's *structural pattern matching*: it compares a value
against **patterns** that describe its shape and, in the same step, **destructures** it and
captures its parts in variables. It shines when you process commands, events, JSON, syntax
trees or messages that come in different shapes.

## Anatomy

```python
match subject:
    case pattern_1:
        ...
    case pattern_2 if condition:    # optional guard
        ...
    case _:                         # wildcard: everything else
        ...
```

`case` clauses are tried **in order** and **only the first** one that matches runs (there's no
*fall-through* and no `break`). If none matches and there's no `case _`, nothing happens.

## Kinds of patterns

### Literals and alternatives

```python
match status:
    case 200 | 201 | 204:
        return "ok"
    case 404:
        return "not found"
    case 500 | 502 | 503:
        return "server error"
```

### Captures

A **bare name** captures the value, whatever it is:

```python
match point:
    case (0, 0):
        return "origin"
    case (x, 0):                  # captures x; requires y == 0
        return f"on the X axis at {x}"
    case (x, y):
        return f"({x}, {y})"
```

### ⚠️ The trap: a bare name **captures**, it doesn't compare

```python
RED = "red"
match color:
    case RED:             # ✗ does NOT compare with "red"! captures anything into RED
        ...
```

To compare against constants, use a **dotted name** (`Color.RED`, `config.DEBUG_MODE`) or a
literal. Python knows a dotted name is a value, not a capture.

### Sequences

```python
match command.split():
    case []:
        return "empty"
    case ["exit" | "quit"]:
        return "bye"
    case ["go", direction]:                     # exactly 2 elements
        return f"going {direction}"
    case ["take", *items] if items:             # 1 or more: *rest like in unpacking
        return f"you took {', '.join(items)}"
    case ["take", first, *_]:                   # _ discards
        ...
```

Sequence patterns match lists and tuples, but **not** strings (a `str` isn't destructured
character by character, by design).

### Capturing with `as`

```python
case ["go", ("north" | "south" | "east" | "west") as direction]:
    ...
```

### Mappings (dicts)

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        return f"click at ({x}, {y})"
    case {"type": "key", "key": "enter"}:
        return "confirm"
    case {"type": "key", "key": key}:
        return f"key {key}"
```

**Extra keys are ignored**: `{"type": "click", "x": 1, "y": 2, "button": "left"}` matches the
first case. That's exactly what you want with JSON, where new fields can always show up.
To capture the rest, use `**rest`.

### Classes (with type checking)

```python
match shape:
    case Circle(radius=0):
        return "degenerate"
    case Circle(radius=r):
        return f"circle of radius {r}"
    case Rectangle(width=a, height=b) if a == b:
        return f"square of side {a}"
    case Rectangle(width=a, height=b):
        return f"rectangle {a} x {b}"
```

`Circle(radius=r)` means: "it's an instance of `Circle` and its `radius` attribute goes into
`r`". Dataclasses also allow the positional form, `Circle(r)`, because they generate
`__match_args__`.

With built-in types, `int(x)` or `str(s)` **checks the type and captures**:

```python
case {"x": int(x), "y": int(y)}:     # only if x and y are ints
```

## Guards

An `if` after the pattern adds a condition. If the pattern matches but the guard is false,
matching continues with the next `case`:

```python
case {"type": "scroll", "delta": d} if d < 0:
    return "down"
case {"type": "scroll", "delta": d} if d > 0:
    return "up"
```

## `match` or `if/elif`?

- **`match`** when you branch on the **shape** of the data (which keys are there, how many
  elements, what class it is) and want to extract parts.
- **`if/elif`** for simple boolean conditions or ranges (`if age < 18`). A `match` with only
  literals doesn't add much over a dispatch dict either.

## Summary

- `match` compares **shape** and **destructures** in one step; the first matching `case` wins.
- Literals, `|`, captures, sequences with `*rest`, mappings (extra keys ignored), classes with
  attributes, and `int(x)` to check the type.
- **A bare name captures.** For constants, use a dotted name.
- `case _` as the wildcard; `if` as a guard; `as` to capture a sub-pattern.

## Exercise

A command interpreter, a JSON-like event processor and a shape describer, all with `match`.

**Further reading:** [PEP 636 — pattern matching tutorial](https://peps.python.org/pep-0636/)
(the best resource for learning it).
