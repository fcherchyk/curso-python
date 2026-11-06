# Exceptions

In Python, exceptions aren't something "exceptional" to be avoided at all costs: they're the
**normal** mechanism for signaling errors, and also for things like the end of an iterator
(`StopIteration`). The idiomatic style is **EAFP**: *"Easier to Ask Forgiveness than
Permission"*, that is, try the operation and handle the error, instead of checking first
whether you can.

## `try` / `except` / `else` / `finally`

```python
try:
    file = open(path, encoding="utf-8")
except FileNotFoundError:
    print("doesn't exist")
except (PermissionError, IsADirectoryError) as e:
    print(f"can't read it: {e}")
else:
    # runs ONLY if the try raised nothing
    with file:
        process(file)
finally:
    # ALWAYS runs: error or not, even with return or break
    print("done")
```

- Put in the `try` **only** the line that can fail the way you expect. What follows goes in
  `else`, so you don't accidentally catch errors from other lines.
- `finally` is for cleanup. In practice, it's almost always replaced by a `with` (context
  manager), which we cover in the advanced functions module.

## EAFP vs. LBYL

```python
# LBYL (Look Before You Leap): check first
if "age" in data and data["age"].isdigit():
    age = int(data["age"])

# EAFP: try it and handle the error
try:
    age = int(data["age"])
except (KeyError, ValueError):
    age = None
```

EAFP is usually shorter, avoids repeating the validation logic and has no *race conditions*:
between "does the file exist?" and "open it", the file can disappear.

## What to catch (and what not to)

```python
try:
    ...
except Exception:          # ✗ almost always too broad
    pass                   # ✗✗ and it silences it too
```

- Catch the **most specific** exception you know how to handle.
- **Never** use a bare `except:`: it also catches `KeyboardInterrupt` and `SystemExit`, so
  your program can't be stopped with Ctrl+C.
- If you catch something broad (for example, at the edge of a server), **log** it with
  `logging.exception(...)` and re-raise or return an explicit error.

### The hierarchy worth knowing

```
BaseException
 ├── KeyboardInterrupt, SystemExit      ← don't catch these
 └── Exception
      ├── ArithmeticError → ZeroDivisionError
      ├── LookupError → KeyError, IndexError
      ├── ValueError       (right type, invalid value: int("x"))
      ├── TypeError        (wrong type: "a" + 1)
      ├── AttributeError, NameError
      ├── OSError → FileNotFoundError, PermissionError, TimeoutError…
      └── RuntimeError, NotImplementedError…
```

Catching a base class catches all of its subclasses: `except LookupError` covers `KeyError`
and `IndexError`.

## Raising exceptions

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount!r}")
    ...
```

Include **the value that caused the problem** in the message: it saves a lot of debugging time.

A bare `raise`, inside an `except`, re-raises the current exception while keeping the original
traceback:

```python
except ValueError:
    log.warning("invalid data")
    raise
```

## Custom exceptions

Define your own exceptions when the caller needs to **tell your error apart** in order to
handle it:

```python
class BankError(Exception):
    """Base for this module's errors."""

class InsufficientFunds(BankError):
    def __init__(self, balance: float, amount: float) -> None:
        super().__init__(f"balance {balance} is not enough to withdraw {amount}")
        self.balance = balance
        self.amount = amount
```

Good practices:

- Inherit from `Exception` (or from a standard exception that makes sense, like `ValueError`).
- Have **one base exception per package**, so users of your library can catch "any error
  from this package" with a single `except`.
- Name the classes with an `Error` suffix or with a name that describes the problem.
- Store the data needed to handle the error as attributes.

## Chaining: `raise ... from ...`

When you translate a low-level error into one from your domain, chain the cause:

```python
class ConfigError(Exception): ...

def read_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise ConfigError(f"missing config file: {path}") from e
```

The traceback shows both exceptions ("The above exception was the direct cause…") and the
original is kept in `error.__cause__`. With `from None` you hide the cause, when it adds
nothing.

## `assert` is not for validation

```python
assert amount > 0, "invalid amount"     # ✗ to validate input
```

`assert` statements **are removed** if Python runs with `-O`. They're for expressing internal
invariants ("this should never happen") and for tests, not for validating user data.

## Summary

- EAFP: try it and handle the error.
- Small `try`; the rest goes in `else`; cleanup goes in `finally` or `with`.
- Catch specific exceptions. Never a bare `except:`; never silence without logging.
- Custom exceptions with one base per package and useful attributes.
- `raise NewError(...) from e` to translate errors without losing the cause.
- `assert` is not validation.

## Exercise

Four functions: conversion with EAFP, a custom exception that carries data, chaining with
`from`, and batch processing that collects errors without stopping.

**Further reading:** [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html),
[Built-in exceptions (full hierarchy)](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).
