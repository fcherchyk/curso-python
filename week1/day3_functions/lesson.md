# Day 3: Functions, closures, decorators and context managers

**Goal:** master the tools that almost every framework is built on. FastAPI and Flask
routes, pytest fixtures and `@property` are decorators; database sessions and
transactions are context managers.

## 1. Functions are objects

```python
ops = {"+": operator.add, "*": operator.mul}
ops["+"](2, 3)  # 5
sorted(xs, key=len)  # pass functions as arguments
from functools import partial

int_base2 = partial(int, base=2)  # fix arguments
```

## 2. Closures and `nonlocal`

An inner function "remembers" the variables of the scope where it was defined.

```python
def multiplier(k):
    def f(x):
        return x * k  # k is captured

    return f


def accumulator():
    total = 0

    def add(x):
        nonlocal total  # without this, `total += x` raises UnboundLocalError
        total += x
        return total

    return add
```

**Trap:** closures capture variables, not values.
`[lambda: i for i in range(3)]` returns functions that all return `2`. The fix is
`lambda i=i: i`.

## 3. Decorators

`@deco` above `def f` is sugar for `f = deco(f)`.

```python
import functools


def log(func):
    @functools.wraps(func)  # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
```

A **decorator with parameters** is a function that returns a decorator, so there are three
levels:

```python
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(n)]

        return wrapper

    return decorator


@repeat(3)
def hello(): ...
```

Standard library decorators you need to know: `@functools.cache` /
`@lru_cache(maxsize=...)`, `@property`, `@staticmethod`, `@classmethod`,
`@dataclass`, `@contextmanager` and `@functools.singledispatch`.

## 4. Context managers

They guarantee cleanup (closing, releasing, restoring) even when there are exceptions.

**With a class:**

```python
class Connection:
    def __enter__(self):
        self.open()
        return self  # this is what ends up in `as`

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False  # True = suppress the exception (almost never)
```

**With a generator (more common):**

```python
from contextlib import contextmanager


@contextmanager
def transaction(db):
    db.begin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
```

More from contextlib: `suppress(FileNotFoundError)`, `ExitStack` for a dynamic number of
resources, `closing()`, `redirect_stdout()` and `asynccontextmanager`.

Since 3.10 you can group several context managers in parentheses:

```python
with (
    open("a") as a,
    open("b") as b,
):
    ...
```

## Exercises

```bash
uv run pytest week1/day3_functions
```

**Extra challenge:** add an optional `maxsize` parameter to `memoize` (a decorator that works
with and without parentheses: `@memoize` and `@memoize(maxsize=100)`).

## Further reading

- *Fluent Python*, ch. 7 and 9 (functions and decorators/closures) and ch. 18 (`with`).
- [contextlib docs](https://docs.python.org/3/library/contextlib.html).
