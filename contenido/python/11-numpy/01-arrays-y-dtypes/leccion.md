# Arrays y dtypes

NumPy es la base de todo el Python numérico: pandas, matplotlib, scikit-learn, SciPy y PyTorch
están construidos sobre su objeto central, el **`ndarray`**. Un array se parece a una lista, pero
es muy distinto por dentro: **todos sus elementos tienen el mismo tipo**, están guardados
**contiguos en memoria** y las operaciones se ejecutan en C, sin el costo del intérprete por
cada elemento.

```bash
uv add numpy
```

```python
import numpy as np        # el alias es una convención universal
```

## Crear arrays

```python
np.array([1, 2, 3])                     # desde una lista
np.array([[1, 2], [3, 4]])              # 2D (matriz)
np.zeros(5)                             # [0. 0. 0. 0. 0.]
np.ones((2, 3))                         # 2 filas, 3 columnas de unos
np.full(3, 7)                           # [7 7 7]
np.arange(0, 10, 2)                     # [0 2 4 6 8]: como range, pero devuelve un array
np.linspace(0, 1, 5)                    # [0. 0.25 0.5 0.75 1.]: 5 puntos equiespaciados, con el final
np.eye(3)                               # matriz identidad
```

`arange` con pasos decimales puede sorprender por los errores de redondeo. Para "n puntos entre a
y b" usá `linspace`.

## Forma, dimensiones y tamaño

```python
m = np.array([[1, 2, 3], [4, 5, 6]])
m.shape        # (2, 3): filas, columnas
m.ndim         # 2
m.size         # 6: cantidad total de elementos
len(m)         # 2: el largo de la primera dimensión

m.reshape(3, 2)        # [[1 2] [3 4] [5 6]]: misma data, otra forma
m.reshape(-1)          # aplanado; -1 = "calculalo vos"
m.T                    # transpuesta: shape (3, 2)
```

`reshape` normalmente devuelve una **vista** (no copia los datos). La cantidad de elementos
tiene que coincidir: `reshape(4, 2)` sobre 6 elementos falla.

## dtype: el tipo de TODOS los elementos

```python
np.array([1, 2, 3]).dtype          # int64
np.array([1.5, 2]).dtype           # float64  ← un float "contagia" a todos
np.array([1, 2], dtype=np.float32)
np.array([True, False]).dtype      # bool
np.array(["a", "bc"]).dtype        # <U2: strings Unicode de largo fijo 2
a.astype(np.int32)                 # convertir (devuelve una copia)
```

A diferencia de una lista de Python, que puede mezclar cualquier cosa, un array tiene **un solo
tipo**. Si mezclás, NumPy elige el más general (`int` + `float` → `float`). Si le pasás objetos
arbitrarios, terminás con `dtype=object` y perdés todas las ventajas.

### Ojo: los enteros de NumPy tienen tamaño fijo

```python
np.array([200], dtype=np.uint8) + 100      # [44]  ← overflow silencioso (300 - 256)
np.int64(2) ** 70                           # se desborda; en Python puro, 2 ** 70 es exacto
```

Igual que en Go, los enteros de NumPy son de 8, 16, 32 o 64 bits. Para datos reales casi siempre
alcanza `int64`/`float64`, pero conviene saber que existe el overflow.

## Indexado y slicing

```python
v = np.array([10, 20, 30, 40, 50])
v[0], v[-1]          # 10, 50
v[1:4]               # [20 30 40]
v[::2]               # [10 30 50]

m = np.array([[1, 2, 3], [4, 5, 6]])
m[1, 2]              # 6: fila 1, columna 2 (en vez de m[1][2])
m[:, 0]              # [1 4]: toda la columna 0
m[0, :]              # [1 2 3]: toda la fila 0
```

### ⚠️ Los slices son vistas, no copias

```python
v = np.arange(5)
s = v[1:3]
s[0] = 99
v                    # [ 0 99  2  3  4]  ← ¡el original cambió!
```

Es lo **contrario** de las listas de Python, donde un slice copia, y lo mismo que pasa con los
slices de Go. NumPy lo hace así para no copiar datos grandes sin necesidad. Si necesitás
independencia, `.copy()`.

## Listas vs. arrays

| Lista de Python                      | `ndarray`                                  |
|--------------------------------------|--------------------------------------------|
| cualquier mezcla de tipos            | un solo `dtype`                             |
| `[1, 2] + [3]` concatena             | `a + b` suma elemento a elemento (próximo capítulo) |
| `xs * 2` repite la lista             | `a * 2` multiplica cada elemento            |
| crece con `append` barato            | tamaño fijo: `np.append` crea un array nuevo |
| el slice copia                       | el slice es una **vista**                   |
| lenta para operar en masa            | operaciones en C, entre 10 y 100 veces más rápidas |

El último punto es el que importa: construí el array **de una vez** (con `np.array`, `zeros`,
`arange`…), en lugar de hacerle `append` dentro de un bucle.

## Resumen

- `np.array`, `zeros`, `ones`, `arange`, `linspace` y `eye` para crear.
- `shape`, `ndim`, `size`, `reshape` (con `-1`) y `.T`.
- Un solo `dtype` por array; `astype` para convertir; cuidado con el overflow de enteros.
- `m[fila, columna]`, `m[:, j]`, `m[i, :]`; los slices son **vistas** (`.copy()` si hace falta).

## Ejercicio

Crear arrays con la forma y el tipo pedidos, cambiar su forma, extraer filas, columnas y
diagonales y demostrar la diferencia entre vista y copia.

**Para profundizar:** [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html),
[Data types](https://numpy.org/doc/stable/user/basics.types.html).
