# Arrays and dtypes

NumPy is the foundation of all numerical Python: pandas, matplotlib, scikit-learn, SciPy and PyTorch
are built on top of its central object, the **`ndarray`**. An array looks like a list, but it is
very different inside: **all its elements have the same type**, they are stored
**contiguously in memory**, and operations run in C, without paying the interpreter's cost for
each element.

```bash
uv add numpy
```

```python
import numpy as np        # the alias is a universal convention
```

## Creating arrays

```python
np.array([1, 2, 3])                     # from a list
np.array([[1, 2], [3, 4]])              # 2D (matrix)
np.zeros(5)                             # [0. 0. 0. 0. 0.]
np.ones((2, 3))                         # 2 rows, 3 columns of ones
np.full(3, 7)                           # [7 7 7]
np.arange(0, 10, 2)                     # [0 2 4 6 8]: like range, but returns an array
np.linspace(0, 1, 5)                    # [0. 0.25 0.5 0.75 1.]: 5 evenly spaced points, endpoint included
np.eye(3)                               # identity matrix
```

`arange` with decimal steps can surprise you because of rounding errors. For "n points between a
and b", use `linspace`.

## Shape, dimensions and size

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
m.shape        # (2, 3): rows, columns
m.ndim         # 2
m.size         # 6: total number of elements
len(m)         # 2: the length of the first dimension

m.reshape(3, 2)        # [[1 2] [3 4] [5 6]]: same data, different shape
m.reshape(-1)          # flattened; -1 = "you figure it out"
m.T                    # transpose: shape (3, 2)
```

`reshape` usually returns a **view** (it doesn't copy the data). The number of elements
has to match: `reshape(4, 2)` on 6 elements fails.

## dtype: the type of ALL the elements

```python
np.array([1, 2, 3]).dtype          # int64
np.array([1.5, 2]).dtype           # float64  ← one float "infects" all of them
np.array([1, 2], dtype=np.float32)
np.array([True, False]).dtype      # bool
np.array(["a", "bc"]).dtype        # <U2: fixed-length Unicode strings of length 2
a.astype(np.int32)                 # convert (returns a copy)
```

Unlike a Python list, which can mix anything, an array has **a single
type**. If you mix, NumPy picks the most general one (`int` + `float` → `float`). If you pass it
arbitrary objects, you end up with `dtype=object` and lose all the advantages.

### Careful: NumPy integers have a fixed size

```python
np.array([200], dtype=np.uint8) + 100      # [44]  ← silent overflow (300 - 256)
np.int64(2) ** 70                           # overflows; in plain Python, 2 ** 70 is exact
```

Just like in Go, NumPy integers are 8, 16, 32 or 64 bits. For real data `int64`/`float64` is
almost always enough, but it's worth knowing that overflow exists.

## Indexing and slicing

```python
v = np.array([10, 20, 30, 40, 50])
v[0], v[-1]          # 10, 50
v[1:4]               # [20 30 40]
v[::2]               # [10 30 50]

m = np.array([[1, 2, 3], [4, 5, 6]])
m[1, 2]              # 6: row 1, column 2 (instead of m[1][2])
m[:, 0]              # [1 4]: all of column 0
m[0, :]              # [1 2 3]: all of row 0
```

### ⚠️ Slices are views, not copies

```python
v = np.arange(5)
s = v[1:3]
s[0] = 99
v                    # [ 0 99  2  3  4]  ← the original changed!
```

This is the **opposite** of Python lists, where a slice copies, and the same as what happens with
Go slices. NumPy does it this way to avoid copying large data unnecessarily. If you need
independence, use `.copy()`.

## Lists vs. arrays

| Python list                          | `ndarray`                                  |
|--------------------------------------|--------------------------------------------|
| any mix of types                     | a single `dtype`                            |
| `[1, 2] + [3]` concatenates          | `a + b` adds element-wise (next chapter)    |
| `xs * 2` repeats the list            | `a * 2` multiplies each element             |
| grows with a cheap `append`          | fixed size: `np.append` creates a new array |
| a slice copies                       | a slice is a **view**                       |
| slow for bulk operations             | operations in C, 10 to 100 times faster     |

The last point is the one that matters: build the array **all at once** (with `np.array`, `zeros`,
`arange`…), instead of calling `append` inside a loop.

## Summary

- `np.array`, `zeros`, `ones`, `arange`, `linspace` and `eye` to create arrays.
- `shape`, `ndim`, `size`, `reshape` (with `-1`) and `.T`.
- One `dtype` per array; `astype` to convert; watch out for integer overflow.
- `m[row, column]`, `m[:, j]`, `m[i, :]`; slices are **views** (`.copy()` if needed).

## Exercise

Create arrays with the requested shape and type, change their shape, extract rows, columns and
diagonals, and demonstrate the difference between a view and a copy.

**Further reading:** [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html),
[Data types](https://numpy.org/doc/stable/user/basics.types.html).
