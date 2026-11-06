# Generators

A **generator** is a function that, instead of computing everything and returning it,
**produces values one at a time**, whenever someone asks for them. It's the simplest way to write an
iterator: no classes with `__next__`, just `yield`.

## `yield` turns a function into a generator

```python
def countdown(n):
    print("starting")
    while n > 0:
        yield n
        n -= 1
    print("done")

g = countdown(3)    # prints nothing! it only creates the generator
next(g)             # prints "starting", returns 3
next(g)             # 2
next(g)             # 1
next(g)             # prints "done" and raises StopIteration
```

Things to notice:

1. Calling the function **doesn't run the body**: it returns a generator object.
2. Each `next()` runs until the next `yield`, hands over that value and **pauses**,
   keeping its local variables and position.
3. When the function ends (or hits `return`), the generator raises `StopIteration`.

That's why generators are **lazy**: they don't compute anything nobody asked for.

## Why it matters: memory and composition

```python
def squares_list(n):
    return [i * i for i in range(n)]      # builds n elements in memory

def squares_gen(n):
    for i in range(n):
        yield i * i                        # one element at a time

sum(squares_list(10**8))   # ~4 GB of RAM
sum(squares_gen(10**8))    # constant memory
```

A generator can also be **infinite**, because it only produces what gets consumed:

```python
def naturals():
    n = 0
    while True:
        yield n
        n += 1

from itertools import islice
list(islice(naturals(), 5))   # [0, 1, 2, 3, 4]
```

## Generator expressions

For simple cases, comprehension syntax with parentheses creates a generator without
writing a function:

```python
squares = (i * i for i in range(10))
total = sum(len(line) for line in file)       # no extra parentheses when it's the only argument
```

Rule of thumb: if it fits on one readable line, use a generator expression; if it needs
state, several steps or `try`, write a function with `yield`.

## `yield from`: delegating to another iterable

`yield from iterable` yields every element of `iterable`, one by one. It's ideal for
**recursion**:

```python
def walk(node):
    yield node.value
    for child in node.children:
        yield from walk(child)
```

Without `yield from`, you'd have to write `for x in walk(child): yield x`.

## Stateful generators

A generator is a very natural way to express algorithms that "remember" something from
one step to the next:

```python
def running_averages(values):
    total = 0
    for i, v in enumerate(values, start=1):
        total += v
        yield total / i

list(running_averages([10, 20, 30]))   # [10.0, 15.0, 20.0]
```

## Cleanup: `try/finally` and `with` inside a generator

If the generator opens a resource, use `with` inside it. When the generator finishes, or when
it's destroyed before finishing (for example, when a `for` loop exits with `break`), Python calls
`gen.close()` and the resource is released:

```python
def lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")
```

## Advanced features (so you can recognize them)

- `return value` inside a generator ends the iteration; the value travels in
  `StopIteration.value` and is what `yield from` returns.
- `gen.send(x)` sends a value into the generator (the `yield` receives it as its result). It's the
  historical basis of coroutines; today, for concurrency, you use `async`/`await`.
- `gen.throw(exc)` and `gen.close()` inject an exception or close it.

You won't need them often, but they show up in libraries and in interviews.

## When **not** to use a generator

- If you'll iterate over the result several times, or need `len()`, indexing or slicing:
  return a list.
- If the collection is small and you'll use all of it: a list is easier to debug.
- If the function has side effects that must happen **right away**: remember that the body
  doesn't run until someone iterates. A generator nobody consumes does nothing.

## Summary

- `yield` pauses the function and hands over a value; the body only runs when you iterate.
- Generators use constant memory and can be infinite.
- `(expr for x in xs)` for one-liners; `def` with `yield` for stateful logic.
- `yield from` delegates, ideal for recursion.
- They are iterators: they're consumed only once.

## Exercise

Four generators: an infinite one, a line filter, a recursive flatten with `yield from`
and a `range` for decimals.

**Further reading:** [PEP 255 — Simple Generators](https://peps.python.org/pep-0255/),
[PEP 380 — yield from](https://peps.python.org/pep-0380/), *Fluent Python*, ch. 17.
