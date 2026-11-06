# Closures and scopes

A **closure** is a function that remembers variables from the place where it was defined,
even after that place has finished running. It's the mechanism behind decorators, function
factories and much of the "private" state in Python without writing classes.

## The LEGB rule

When Python encounters a name, it looks it up in this order:

1. **L**ocal: the current function.
2. **E**nclosing: the functions that contain it, from the inside out.
3. **G**lobal: the module.
4. **B**uilt-in: `len`, `print`, `range`…

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        return x            # not local → found in enclosing
    return inner

outer()()                   # 'enclosing'
```

## What a closure is

```python
def make_multiplier(k):
    def multiply(x):
        return x * k        # k is a "free" variable: it comes from outside
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
double(5), triple(5)        # (10, 15)
```

When `make_multiplier` returns, its variable `k` should go away. But `multiply` uses it, so
Python keeps it in a **cell** attached to the function:

```python
double.__closure__[0].cell_contents   # 2
```

Each call to `make_multiplier` creates a new scope, so `double` and `triple` each have their
own `k`.

## Modifying outer variables: `nonlocal`

Reading a variable from the outer scope just works. **Assigning** it doesn't, because any
assignment inside a function creates a **local** variable:

```python
def make_counter():
    total = 0
    def increment():
        total += 1          # UnboundLocalError: `total` is local and read before assignment
        return total
    return increment
```

`nonlocal` tells Python that the name belongs to the enclosing scope:

```python
def make_counter():
    total = 0
    def increment():
        nonlocal total
        total += 1
        return total
    return increment

c = make_counter()
c(), c(), c()               # (1, 2, 3)
```

If what you capture is a **mutable** object and you only modify it (without reassigning the
name), you don't need `nonlocal`:

```python
def make_history():
    events = []
    def record(e):
        events.append(e)    # mutates the object, doesn't reassign the name
        return list(events)
    return record
```

Its relative `global` does the same for module variables. It's almost never a good idea:
global state makes testing and reasoning about the code harder.

## The classic trap: *late binding*

Closures capture **variables, not values**. The value is looked up **when the function is
called**, not when it's created:

```python
functions = [lambda: i for i in range(3)]
[f() for f in functions]    # [2, 2, 2]  ← not [0, 1, 2]!
```

All three lambdas share the same variable `i`, which is 2 at the end of the loop. Two
fixes:

```python
# 1. Default argument: evaluated at DEFINITION time, so it freezes the current value
functions = [lambda i=i: i for i in range(3)]

# 2. A factory: each call creates a new scope with its own value
def make(i):
    return lambda: i
functions = [make(i) for i in range(3)]
```

This trap also shows up with callbacks created in a loop (UI buttons, scheduled tasks,
etc.).

## Closure or class

A stateful closure is, at heart, an object with a single method:

```python
# Closure
def make_averager():
    values = []
    def add(x):
        values.append(x)
        return sum(values) / len(values)
    return add

# Equivalent class
class Averager:
    def __init__(self):
        self.values = []
    def __call__(self, x):
        self.values.append(x)
        return sum(self.values) / len(self.values)
```

Use a **closure** when there's a single operation and little state. Switch to a **class**
when you need several methods, when you want to inspect the state from outside, or when the
state grows.

## Summary

- LEGB: local → enclosing → global → built-in.
- A closure keeps the variables of the scope where it was defined.
- To **reassign** an outer variable you need `nonlocal`; to mutate an object, you don't.
- *Late binding*: closures see the value at the time they're **called**. Fix: a default
  argument or a factory.
- A stateful closure is an object with a single method; if it grows, use a class.

## Exercise

A counter with `nonlocal`, multipliers created in a loop (dodging the *late binding* trap)
and a running averager.

**Further reading:** [Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding),
*Fluent Python*, ch. 9.
