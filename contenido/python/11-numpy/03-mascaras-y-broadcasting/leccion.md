# Máscaras booleanas, fancy indexing y broadcasting

Dos herramientas completan el "pensar vectorizado". Las **máscaras booleanas** permiten
filtrar y modificar elementos que cumplen una condición sin escribir un `if`. El
**broadcasting** permite operar arrays de formas distintas (una matriz con un vector, una
columna con una fila) sin copiar datos. Con estas dos ideas se resuelven la mayoría de las
transformaciones de datos.

## Máscaras booleanas

Una comparación sobre un array devuelve **un array de booleanos** del mismo tamaño:

```python
v = np.array([5, -2, 8, -1, 3])
v > 0                 # [ True False  True False  True]
v[v > 0]              # [5 8 3]: filtra con la máscara
(v > 0).sum()         # 3: True cuenta como 1
(v > 0).mean()        # 0.6: proporción
(v > 0).any(), (v > 0).all()
```

### Combinar condiciones: `&`, `|`, `~` (¡con paréntesis!)

```python
v[(v > 0) & (v < 6)]          # [5 3]
v[(v < 0) | (v > 7)]          # [-2  8 -1]
v[~(v > 0)]                   # [-2 -1]: negación
```

- Con arrays no se usan `and`/`or`/`not`: levantan "*The truth value of an array is ambiguous*".
  Se usan `&`, `|` y `~`.
- **Los paréntesis son obligatorios**: `&` tiene más precedencia que `>`, así que
  `v > 0 & v < 6` se interpreta como `v > (0 & v) < 6`.

### Modificar con máscaras

```python
v[v < 0] = 0                  # reemplaza los negativos EN EL LUGAR
np.where(v < 0, 0, v)         # versión que devuelve un array nuevo
```

## Fancy indexing: indexar con arrays de posiciones

```python
v = np.array([10, 20, 30, 40, 50])
v[[0, 2, 4]]                  # [10 30 50]
np.argsort(v)                 # posiciones que ordenarían el array
v[np.argsort(v)[-3:]]         # los 3 mayores
np.argmax(v), np.argmin(v)    # posición del máximo y del mínimo
```

`argsort`/`argmax` devuelven **posiciones**, no valores. Son muy útiles para "¿cuál fue el
mejor?" cuando hay otro array paralelo con nombres o fechas: `nombres[np.argmax(ventas)]`.

## Broadcasting: operar formas distintas

Ya viste el caso más simple: `array * escalar`. El escalar se "estira" a la forma del array. El
broadcasting generaliza esa idea a dimensiones.

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])          # shape (2, 3)
fila = np.array([10, 20, 30])      # shape (3,)

m + fila
# [[11 22 33]
#  [14 25 36]]      ← la fila se suma a CADA fila de m
```

### Las reglas

Se comparan las formas **desde la derecha**. Dos dimensiones son compatibles si son **iguales o
alguna es 1**:

```
m:     (2, 3)
fila:     (3,)   → se trata como (1, 3) → se estira a (2, 3)   ✓

col:   (2, 1)    → se estira a (2, 3)                           ✓
otra:     (2,)   → (1, 2) vs (2, 3): 2 ≠ 3 y ninguna es 1        ✗ error
```

### Columnas: `keepdims` y `[:, None]`

Un caso típico: restar a cada fila **su propio** promedio.

```python
promedios = m.mean(axis=1)                  # shape (2,)  → no broadcastea contra (2, 3)
promedios = m.mean(axis=1, keepdims=True)   # shape (2, 1) → ✓
m - promedios
# [[-1.  0.  1.]
#  [-1.  0.  1.]]
```

`keepdims=True` conserva la dimensión reducida con tamaño 1. La alternativa es agregar un eje:
`v[:, None]` (o `v[:, np.newaxis]`) convierte `(n,)` en `(n, 1)`.

### El "producto exterior" gratis

```python
a = np.arange(1, 4)
a[:, None] * a[None, :]
# [[1 2 3]
#  [2 4 6]
#  [3 6 9]]          ← tabla de multiplicar sin bucles
```

Una columna `(3, 1)` contra una fila `(1, 3)` da una matriz `(3, 3)`. Este patrón calcula
distancias entre todos los pares de puntos o combina todas las opciones con todas.

## Ejes: `axis=0` y `axis=1`

```python
m.sum(axis=0)       # [5 7 9]   ← colapsa las FILAS: un resultado por columna
m.sum(axis=1)       # [ 6 15]   ← colapsa las COLUMNAS: un resultado por fila
```

Regla mnemotécnica: el `axis` que pasás es el que **desaparece**. Lo profundizamos en el
próximo capítulo.

## Resumen

- Una comparación da una máscara; `v[mascara]` filtra, `v[mascara] = x` modifica y `.sum()`/
  `.mean()` cuentan.
- `&`, `|` y `~` con paréntesis; nunca `and`/`or`.
- Fancy indexing con listas de posiciones; `argsort`, `argmax` y `argmin` para encontrar
  posiciones.
- Broadcasting: las dimensiones se comparan desde la derecha y son compatibles si son iguales o
  1; `keepdims=True` y `[:, None]` para alinear.

## Ejercicio

Filtrar con condiciones combinadas, reemplazar con máscaras, encontrar los mejores con
`argsort`, centrar columnas con broadcasting y una tabla de multiplicar sin bucles.

**Para profundizar:** [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html),
[Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html).
