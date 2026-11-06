# Decorators

A decorator is a function that **takes a function and returns another one**, usually a
"wrapped" version that adds behavior before or after the original. `@property`,
`@dataclass`, `@functools.cache`, FastAPI and Flask routes (`@app.get(...)`) and pytest
fixtures are all built with decorators. If you understand closures, decorators are one more
step.

## `@` is syntactic sugar

```python
@my_decorator
def greet():
    ...
```

is exactly the same as:

```python
def greet():
    ...
greet = my_decorator(greet)
```

The decorator runs **only once**, when the function is defined (usually when the module is
imported). Whatever the decorator returned is what ends up bound to the name `greet`.

## The basic pattern: a wrapper

```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"← {func.__name__} = {result!r}")
        return result
    return wrapper

@log
def add(a, b):
    return a + b

add(2, 3)
# → add(2, 3)
# ← add = 5
```

The parts:

1. `log` receives the original function.
2. It defines `wrapper`, a **closure** with access to `func`.
3. `wrapper` accepts `*args, **kwargs` so it works with **any** signature, and forwards them.
4. It **returns the result** of the original function (forgetting this is a very common bug:
   the decorated function starts returning `None`).
5. `log` returns `wrapper`, which replaces the original.

## `functools.wraps`: don't skip it

Without `@functools.wraps(func)`, the decorated function loses its identity:

```python
add.__name__     # 'wrapper'   ← without wraps
add.__doc__      # None
```

That breaks tracebacks, logs, documentation, `help()`, frameworks that use the function's
name (for example, to register routes) and introspection tools. `wraps` copies `__name__`,
`__doc__`, `__module__`, `__qualname__` and `__dict__`, and adds `__wrapped__`, which points
to the original.

## Stateful decorators

Since the wrapper is a function object, you can hang attributes on it. It's the simplest way
to expose state:

```python
def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    wrapper.calls = 0
    return wrapper
```

Another variant is to keep the state in the closure (a variable of the decorator) and expose
it through a helper function.

## Decorators that don't wrap: registration

Not every decorator returns a wrapper. Some just **register** the function and return it
unchanged. That's how plugin systems and web framework routes work:

```python
COMMANDS = {}

def command(func):
    COMMANDS[func.__name__] = func
    return func             # the same function, unchanged

@command
def help(): ...

COMMANDS["help"]()
```

## Memoization: the classic example

```python
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(100)     # instant
```

This works because inside `fib`, the name `fib` points to the **decorated** version, so the
recursive calls also go through the cache.

In real code, use the stdlib version, which is more complete and well tested:

```python
from functools import cache, lru_cache

@cache                         # unbounded
def fib(n): ...

@lru_cache(maxsize=1024)       # evicts the least recently used
def fetch(id): ...

fetch.cache_info()             # hits, misses, size
fetch.cache_clear()
```

Requirement: the arguments must be **hashable**, because they're the cache key.

## Stacking decorators

```python
@log
@memoize
def f(x): ...
```

is equivalent to `f = log(memoize(f))`: they're applied **bottom to top**, and when called
they run from the outside in. Order matters: in this example every call is logged, including
the ones served from the cache. Reversed, only the calls that actually run `f` would be
logged.

## Stdlib decorators you should recognize

| Decorator                     | What for                                               |
|-------------------------------|--------------------------------------------------------|
| `@functools.cache` / `lru_cache` | memoization                                         |
| `@functools.wraps`            | preserving metadata in your own decorators             |
| `@property`                   | computed attribute (modeling module)                   |
| `@classmethod`, `@staticmethod` | class and static methods                             |
| `@dataclass`                  | generates `__init__`, `__repr__` and `__eq__`          |
| `@contextlib.contextmanager`  | context manager from a generator                       |
| `@functools.singledispatch`   | overloading on the type of the first argument          |
| `@typing.override` (3.12)     | marks a method as overriding the parent class's        |

## Summary

- `@deco` over `def f` is equivalent to `f = deco(f)`, and it runs once, at definition time.
- The pattern: a closure `wrapper(*args, **kwargs)` that calls `func` and **returns its
  result**.
- **Always** use `@functools.wraps(func)`.
- Some decorators only register and return the same function.
- They stack bottom to top.
- For caching, `functools.cache` and `lru_cache`.

## Exercise

Three decorators: one with state in an attribute, your own memoizer and a registration one.

**Further reading:** [PEP 318 — Decorators](https://peps.python.org/pep-0318/),
[functools](https://docs.python.org/3/library/functools.html), *Fluent Python*, ch. 9.
