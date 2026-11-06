# Context managers

`with` guarantees that something gets **cleaned up** (closed, released, restored or
committed) no matter what happens inside the block, even if there's an exception or a
`return`. Files, locks, connections, transactions, temporary directories, mocks in tests:
all of them are handled with context managers.

## The problem they solve

```python
f = open("data.txt")
process(f)           # if this fails...
f.close()            # ...this never runs
```

The correct version without `with` needs `try/finally`:

```python
f = open("data.txt")
try:
    process(f)
finally:
    f.close()
```

`with` wraps that pattern:

```python
with open("data.txt") as f:
    process(f)
# here the file is already closed, no matter what
```

## The protocol: `__enter__` and `__exit__`

```python
with expression as name:
    body
```

does, roughly, this:

```python
cm = expression
name = cm.__enter__()
try:
    body
except BaseException as e:
    if not cm.__exit__(type(e), e, e.__traceback__):
        raise                  # __exit__ returned False → the exception continues
else:
    cm.__exit__(None, None, None)
```

- `__enter__` sets up the resource, and whatever it returns goes into the `as` variable. It
  often returns `self`, but not always.
- `__exit__` receives the exception (or three `None`s) and does the cleanup. If it returns
  `True`, **the exception is suppressed**. You almost always want to return `None` or `False`.

## With a class

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.duration = time.perf_counter() - self.start
        # no return → None → doesn't suppress exceptions

with Timer() as t:
    do_something()
print(f"took {t.duration:.3f}s")
```

Writing it as a class makes sense when the object has **other uses** besides the `with`,
such as attributes or methods, or when it's reused.

## With a generator: `@contextmanager`

For most cases, `contextlib.contextmanager` is shorter. Everything before the `yield` is the
`__enter__`, whatever you `yield` goes to the `as`, and everything after it is the
`__exit__`:

```python
from contextlib import contextmanager
import os

@contextmanager
def in_directory(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(previous)         # runs even if the block fails
```

**The `try/finally` around the `yield` is essential.** If the `with` block raises an
exception, it's re-raised **at the `yield` line**. Without `finally`, the cleanup doesn't
run.

### Handling the block's exception

```python
@contextmanager
def transaction(connection):
    connection.begin()
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise                      # re-raise: let the caller know
    else:
        connection.commit()
```

If you **don't** re-raise in the `except`, the exception is suppressed. Sometimes that's
what you want (see `suppress` below), but it has to be a deliberate decision.

## Several at once

```python
with open("input.txt") as src, open("output.txt", "w") as dst:
    dst.write(src.read())

# 3.10+: in parentheses, one per line
with (
    open("a.txt") as a,
    open("b.txt") as b,
):
    ...
```

They're entered left to right and exited in reverse order.

## The `contextlib` toolbox

```python
from contextlib import suppress, ExitStack, closing, redirect_stdout, nullcontext

with suppress(FileNotFoundError):          # ignore one specific exception
    os.remove("temp.txt")

with ExitStack() as stack:                 # a dynamic number of resources
    files = [stack.enter_context(open(p)) for p in paths]

with closing(urlopen(url)) as page:        # objects with .close() but no with protocol
    ...

with redirect_stdout(io.StringIO()) as buf:   # capture prints
    print("hello")

cm = lock if use_lock else nullcontext()   # a "with that does nothing"
```

And in the `async` world there are `async with` and `@asynccontextmanager` (concurrency
module).

## Where you'll see them

- `open()`, `tempfile.TemporaryDirectory()`, `zipfile.ZipFile()`.
- `threading.Lock()`: `with lock:` acquires and releases.
- SQLAlchemy: `with Session(engine) as session, session.begin():`.
- pytest: `with pytest.raises(ValueError):`, `with pytest.warns(...)`, `mock.patch(...)`.
- `decimal.localcontext()`, `warnings.catch_warnings()`.

## Summary

- `with` guarantees cleanup even if there are exceptions or a `return`.
- Protocol: `__enter__` returns what goes to `as`; `__exit__` cleans up and, if it returns
  `True`, suppresses the exception.
- `@contextmanager`: before the `yield` is the setup and after it, the cleanup. **Always**
  with `try/finally` around the `yield`.
- `contextlib`: `suppress`, `ExitStack`, `closing`, `redirect_stdout`, `nullcontext`.

## Exercise

A timer as a class, a directory change that's always restored and a context manager that
captures certain exceptions and hands them over in a list.

**Further reading:** [contextlib](https://docs.python.org/3/library/contextlib.html),
[PEP 343 — The "with" statement](https://peps.python.org/pep-0343/), *Fluent Python*, ch. 18.
