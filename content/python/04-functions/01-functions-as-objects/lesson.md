# Functions as objects

In Python, functions are **first-class objects**: you can assign them to variables, store
them in data structures, pass them as arguments and return them from other functions. Almost
everything in this module (closures, decorators and framework *callbacks*) builds on this
idea.

## A function is just another value

```python
def greet(name):
    return f"hello {name}"

f = greet                # no parentheses: the function, not its result
f("alice")               # 'hello alice'
f.__name__               # 'greet'
type(f)                  # <class 'function'>

actions = [str.upper, str.lower, str.title]
[action("hELLO") for action in actions]    # ['HELLO', 'hello', 'Hello']
```

A common mistake is passing `func()` (its result) when `func` (the function) was expected.

## Functions that take functions

You've already used them: `sorted(key=...)`, `max(key=...)`, `map`, `filter`. The general
pattern is **separating the "what" from the "how"**:

```python
def apply_to_all(func, xs):
    return [func(x) for x in xs]

apply_to_all(len, ["a", "bcd"])      # [1, 3]
```

In modern Python, `map` and `filter` are usually replaced by comprehensions, which read
better. Where functions as arguments really shine is `key=`, callbacks and behavior
injection: "how to retry", "how to format", "what to do when done".

## Dispatching with dicts: replacing `if` chains

```python
import operator

OPERATIONS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def calculate(op, a, b):
    try:
        return OPERATIONS[op](a, b)
    except KeyError:
        raise ValueError(f"unknown operation: {op!r}") from None
```

Adding an operation means adding an entry, without touching the logic. The `operator` module
provides function versions of every operator (`add`, `mul`, `itemgetter`, `attrgetter`,
`methodcaller`…).

## `lambda`: anonymous single-expression functions

```python
sorted(people, key=lambda p: p.age)
```

A `lambda` is just a short way to write a function made of **one expression**. Use it for
short arguments, like `key=`. If you need to assign it to a name (`double = lambda x: x * 2`),
write a `def`: it has a name in tracebacks, supports a docstring, and ruff will flag the
lambda anyway (rule E731).

## Functions that return functions

```python
def make_multiplier(k):
    def multiply(x):
        return x * k
    return multiply

double = make_multiplier(2)
double(21)    # 42
```

`multiply` "remembers" the `k` it was created with: it's a **closure**, the topic of the next
chapter.

## `functools.partial`: fixing arguments

```python
from functools import partial

int_binary = partial(int, base=2)
int_binary("1010")                  # 10

log_error = partial(print, "[ERROR]", sep=" ")
log_error("connection failed")      # [ERROR] connection failed
```

`partial` creates a new function with some arguments already filled in. It's very handy for
adapting a function to the signature other code expects (a no-argument callback, a
single-argument `key=`, etc.).

## Composing functions

```python
from functools import reduce

def compose(*funcs):
    """compose(f, g, h)(x) == f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)

clean = compose(str.title, str.strip)
clean("  alice smith ")    # 'Alice Smith'
```

`reduce` combines the elements pairwise from left to right. It's uncommon in application
code (a `for` loop usually reads better), but it shows up in utilities like this one.

## *Callables*: not just functions

Any object with `__call__` can be "called": classes (calling them creates instances),
methods, `partial` objects and instances of your own classes that define `__call__`.
`callable(obj)` tells you whether something can be called.

```python
class Counter:
    def __init__(self):
        self.n = 0
    def __call__(self):
        self.n += 1
        return self.n

c = Counter()
c(), c()     # (1, 2)
```

## Summary

- Functions are values: pass them without parentheses.
- Use a dict of functions instead of `if/elif` to dispatch on a value.
- `lambda` only for short expressions passed as arguments.
- `functools.partial` fixes arguments; `operator` gives you operators as functions.
- Any object with `__call__` is a *callable*.

## Exercise

Function composition, repeated application, dispatching with a dict of operators, and
`partial`.

**Further reading:** [functools](https://docs.python.org/3/library/functools.html),
[operator](https://docs.python.org/3/library/operator.html), *Fluent Python*, ch. 7.
