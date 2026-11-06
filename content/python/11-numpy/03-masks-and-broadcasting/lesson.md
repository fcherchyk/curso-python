# Boolean masks, fancy indexing and broadcasting

Two tools complete "thinking vectorized". **Boolean masks** let you
filter and modify the elements that meet a condition without writing an `if`.
**Broadcasting** lets you operate on arrays of different shapes (a matrix with a vector, a
column with a row) without copying data. These two ideas solve most
data transformations.

## Boolean masks

A comparison on an array returns **an array of booleans** of the same size:

```python
v = np.array([5, -2, 8, -1, 3])
v > 0                 # [ True False  True False  True]
v[v > 0]              # [5 8 3]: filters with the mask
(v > 0).sum()         # 3: True counts as 1
(v > 0).mean()        # 0.6: proportion
(v > 0).any(), (v > 0).all()
```

### Combining conditions: `&`, `|`, `~` (with parentheses!)

```python
v[(v > 0) & (v < 6)]          # [5 3]
v[(v < 0) | (v > 7)]          # [-2  8 -1]
v[~(v > 0)]                   # [-2 -1]: negation
```

- With arrays you don't use `and`/`or`/`not`: they raise "*The truth value of an array is ambiguous*".
  You use `&`, `|` and `~`.
- **The parentheses are mandatory**: `&` has higher precedence than `>`, so
  `v > 0 & v < 6` is parsed as `v > (0 & v) < 6`.

### Modifying with masks

```python
v[v < 0] = 0                  # replaces the negatives IN PLACE
np.where(v < 0, 0, v)         # version that returns a new array
```

## Fancy indexing: indexing with arrays of positions

```python
v = np.array([10, 20, 30, 40, 50])
v[[0, 2, 4]]                  # [10 30 50]
np.argsort(v)                 # positions that would sort the array
v[np.argsort(v)[-3:]]         # the 3 largest
np.argmax(v), np.argmin(v)    # position of the maximum and of the minimum
```

`argsort`/`argmax` return **positions**, not values. They're very handy for "which one was the
best?" when there's another parallel array with names or dates: `names[np.argmax(sales)]`.

## Broadcasting: operating on different shapes

You've already seen the simplest case: `array * scalar`. The scalar is "stretched" to the shape of
the array. Broadcasting generalizes that idea to dimensions.

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])          # shape (2, 3)
row = np.array([10, 20, 30])       # shape (3,)

m + row
# [[11 22 33]
#  [14 25 36]]      ← the row is added to EACH row of m
```

### The rules

Shapes are compared **from the right**. Two dimensions are compatible if they are **equal or
one of them is 1**:

```
m:     (2, 3)
row:      (3,)   → treated as (1, 3) → stretched to (2, 3)      ✓

col:   (2, 1)    → stretched to (2, 3)                          ✓
other:    (2,)   → (1, 2) vs (2, 3): 2 ≠ 3 and neither is 1     ✗ error
```

### Columns: `keepdims` and `[:, None]`

A typical case: subtract from each row **its own** mean.

```python
means = m.mean(axis=1)                  # shape (2,)  → doesn't broadcast against (2, 3)
means = m.mean(axis=1, keepdims=True)   # shape (2, 1) → ✓
m - means
# [[-1.  0.  1.]
#  [-1.  0.  1.]]
```

`keepdims=True` keeps the reduced dimension with size 1. The alternative is to add an axis:
`v[:, None]` (or `v[:, np.newaxis]`) turns `(n,)` into `(n, 1)`.

### The "outer product" for free

```python
a = np.arange(1, 4)
a[:, None] * a[None, :]
# [[1 2 3]
#  [2 4 6]
#  [3 6 9]]          ← multiplication table without loops
```

A column `(3, 1)` against a row `(1, 3)` gives a `(3, 3)` matrix. This pattern computes
distances between all pairs of points, or combines every option with every other.

## Axes: `axis=0` and `axis=1`

```python
m.sum(axis=0)       # [5 7 9]   ← collapses the ROWS: one result per column
m.sum(axis=1)       # [ 6 15]   ← collapses the COLUMNS: one result per row
```

Rule of thumb: the `axis` you pass is the one that **disappears**. We'll go deeper in the
next chapter.

## Summary

- A comparison gives a mask; `v[mask]` filters, `v[mask] = x` modifies and `.sum()`/
  `.mean()` count.
- `&`, `|` and `~` with parentheses; never `and`/`or`.
- Fancy indexing with lists of positions; `argsort`, `argmax` and `argmin` to find
  positions.
- Broadcasting: dimensions are compared from the right and are compatible if they are equal or
  1; `keepdims=True` and `[:, None]` to line them up.

## Exercise

Filter with combined conditions, replace with masks, find the best with
`argsort`, center columns with broadcasting, and build a multiplication table without loops.

**Further reading:** [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html),
[Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html).
