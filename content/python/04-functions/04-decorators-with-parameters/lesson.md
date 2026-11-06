# Decorators with parameters

`@lru_cache(maxsize=128)`, `@app.get("/users")` and `@pytest.mark.parametrize(...)` are
decorators that **take arguments**. The trick is that they aren't decorators: they're
**factories that return a decorator**. That adds one more level of nested functions, and
it's worth understanding why.

## Why you need another level

```python
@repeat(3)
def greet(): ...
```

is equivalent to:

```python
decorator = repeat(3)           # 1. the factory is called with the parameters
greet = decorator(greet)        # 2. the result decorates the function
```

So `repeat(3)` has to return something that receives a function, that is, a decorator.
That makes three levels:

```python
import functools
import random

def repeat(n):                          # level 1: factory (receives the parameters)
    def decorator(func):                # level 2: decorator (receives the function)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):   # level 3: wrapper (receives the call's arguments)
            return [func(*args, **kwargs) for _ in range(n)]
        return wrapper
    return decorator

@repeat(3)
def roll_die():
    return random.randint(1, 6)

roll_die()     # [4, 1, 6]
```

Each level is a closure over the previous one: `wrapper` sees both `func` and `n`.

## A realistic example: retries

```python
import time

def retry(times, exceptions=(Exception,), delay=0.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise                  # out of attempts: re-raise the last one
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(3, exceptions=(ConnectionError, TimeoutError), delay=0.5)
def call_api(): ...
```

Design details worth copying:

- Catch **only** the given exceptions: a `KeyError` caused by a bug shouldn't be retried.
- Re-raise the **last** exception with `raise` when the attempts run out.
- In production you add exponential *backoff* and *jitter*, or use a library like
  `tenacity`.

## Common mistakes

```python
@repeat           # ✗ no parentheses: repeat receives the FUNCTION as `n`
def f(): ...

@retry()          # ✗ parentheses but missing the required argument → TypeError
def g(): ...
```

If your decorator takes parameters, it's **always** used with parentheses, even if they all
have defaults: `@lru_cache()` (or `@lru_cache`, allowed since 3.8 thanks to the trick below).

## Decorators with optional parentheses

Some decorators work both ways, `@deco` and `@deco(option=...)`. The trick is to check
whether the first argument is the function:

```python
import warnings

def deprecated(func=None, *, replacement=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            msg = f"{f.__name__} is deprecated"
            if replacement:
                msg += f"; use {replacement}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return f(*args, **kwargs)
        return wrapper

    if func is not None:        # used as @deprecated (no parentheses)
        return decorator(func)
    return decorator            # used as @deprecated(replacement="...")
```

The `*` makes the options **keyword-only**, so there's no ambiguity between "I got a
function" and "I got a positional option". `stacklevel=2` makes the warning point to the
caller of the deprecated function instead of the wrapper.

## Alternative: a class as a decorator

When the decorator has a lot of state or configuration, you can write it as a class:

```python
class RateLimiter:
    def __init__(self, per_second):
        self.per_second = per_second

    def __call__(self, func):              # the instance acts as the decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ...
        return wrapper

@RateLimiter(per_second=5)
def send(): ...
```

## Summary

- `@factory(args)` → `factory(args)` returns the decorator → the decorator returns the wrapper.
- That's three levels of functions; each one sees the variables of the previous one.
- Always `functools.wraps` on the wrapper.
- With parameters, use parentheses. To make the parentheses optional: `func=None` and
  keyword-only options.
- If there's a lot of state, a class with `__call__`.

## Exercise

Four decorators with parameters: repeat, retry, clamp the result and deprecate with
optional parentheses.

**Further reading:** *Python Cookbook* (Beazley & Jones), ch. 9,
[warnings](https://docs.python.org/3/library/warnings.html), [tenacity](https://tenacity.readthedocs.io/).
