# Vectorization: think in arrays, not loops

The most important idea in NumPy (and in pandas) is **vectorization**: instead of walking through
the elements with a `for`, you write **one operation on the whole array** and NumPy runs it in C.
The code gets shorter, reads like a math formula, and is 10 to 100 times
faster. Learning to "think vectorized" is the mindset shift you need to make to
work with data.

## Element-wise operations

```python
prices = np.array([100.0, 250.0, 80.0])
quantities = np.array([2, 1, 5])

prices * quantities          # [200. 250. 400.]: multiplies position by position
prices * 1.21                # tax on all of them
prices + 10                  # adds 10 to each one
prices ** 2, -prices, prices / quantities
(prices * quantities).sum()  # 850.0: the total
```

With two arrays, the shapes have to be compatible (or "broadcastable", next chapter).
With a scalar, it applies to every element.

Compare it with the plain Python version:

```python
total = 0
for p, q in zip(prices, quantities):
    total += p * q
```

## Universal functions (ufuncs)

NumPy ships vectorized versions of the math functions:

```python
np.sqrt(v), np.exp(v), np.log(v), np.abs(v), np.round(v, 2)
np.maximum(a, b)            # element-wise maximum (don't confuse with np.max, which reduces)
np.hypot(x, y)              # sqrt(x² + y²)
np.clip(v, 0, 100)          # clamps each value to the range [0, 100]
```

`math.sqrt` does **not** work with arrays (it expects a number). In NumPy code, always use
`np.sqrt` and friends.

## Vectorized conditionals: `np.where` and `np.select`

An `if` inside a loop is replaced by `np.where(condition, if_true, if_false)`:

```python
# 10% discount on prices greater than 200
np.where(prices > 200, prices * 0.9, prices)     # [100. 225.  80.]
```

For several branches, `np.select`:

```python
conditions = [temps < 10, temps < 25]
choices = ["cold", "mild"]
np.select(conditions, choices, default="hot")
```

## Why it's so fast

A Python `for` over an array does, **for each element**:

1. create a Python object (a `float` or an `int` with its header),
2. look up the `__mul__` method and dispatch it dynamically,
3. check types and manage the reference count.

The vectorized operation, on the other hand, walks contiguous memory with a known type, in a
compiled C loop that can also use the processor's SIMD instructions. With a million
elements:

```python
v = np.random.default_rng(0).random(1_000_000)

# Plain Python: ~150 ms
sum(x * x for x in v)

# NumPy: ~1 ms
(v * v).sum()        # or np.dot(v, v), or np.sum(v ** 2)
```

Measure it yourself with `timeit`:

```python
import timeit
timeit.timeit(lambda: (v * v).sum(), number=100) / 100
```

### Anti-patterns that kill performance

```python
# ✗ append in a loop
res = np.array([])
for x in data:
    res = np.append(res, f(x))     # copies the WHOLE array on every iteration: O(n²)!

# ✗ np.vectorize "to make it fast"
f_vec = np.vectorize(f)            # it's a Python for loop in disguise: NO speedup
```

If an operation can't be expressed with ufuncs, `where`, slicing or aggregations, it's worth
rethinking the algorithm before falling back to a loop. If there's no alternative, there's **Numba**
(compiles functions with `@njit`) or Cython.

## Thinking vectorized: an example

"For each day, how much did the price go up relative to the previous day, as a percentage?"

```python
prices = np.array([100, 102, 99, 105])
# Loop: for i in range(1, len(prices)): (prices[i] - prices[i-1]) / prices[i-1]
pct = prices[1:] / prices[:-1] - 1      # [ 0.02  -0.0294  0.0606]
```

Comparing `a[1:]` with `a[:-1]` (the array "shifted" by one position) is a trick you'll see all
over data analysis. In pandas it's `pct_change()`.

## Summary

- Operations between arrays (and with scalars) are element-wise.
- Ufuncs (`np.sqrt`, `np.exp`, `np.maximum`, `np.clip`…) instead of `math` and loops.
- `np.where` / `np.select` replace the `if` inside the loop.
- Vectorization is 10 to 100 times faster: contiguous memory, known types and
  loops in C.
- Avoid `np.append` in loops and don't expect miracles from `np.vectorize`.

## Exercise

Four functions without Python loops. One of them has a test that **measures** that your version
is much faster than a loop.

**Further reading:** [Universal functions](https://numpy.org/doc/stable/reference/ufuncs.html),
[Why is NumPy fast?](https://numpy.org/doc/stable/user/whatisnumpy.html#why-is-numpy-fast)
