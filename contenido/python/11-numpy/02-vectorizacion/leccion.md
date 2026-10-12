# Vectorización: pensar en arrays, no en bucles

La idea más importante de NumPy (y de pandas) es la **vectorización**: en lugar de recorrer los
elementos con un `for`, escribís **una operación sobre el array entero** y NumPy la ejecuta en C.
El código queda más corto, se lee como una fórmula matemática y es entre 10 y 100 veces más
rápido. Aprender a "pensar vectorizado" es el cambio de mentalidad que hay que hacer para
trabajar con datos.

## Operaciones elemento a elemento

```python
precios = np.array([100.0, 250.0, 80.0])
cantidades = np.array([2, 1, 5])

precios * cantidades         # [200. 250. 400.]: multiplica posición a posición
precios * 1.21               # IVA a todos
precios + 10                 # suma 10 a cada uno
precios ** 2, -precios, precios / cantidades
(precios * cantidades).sum() # 850.0: el total
```

Con dos arrays, las formas tienen que ser compatibles (o "broadcasteables", próximo capítulo).
Con un escalar, se aplica a todos.

Comparalo con la versión de Python puro:

```python
total = 0
for p, c in zip(precios, cantidades):
    total += p * c
```

## Funciones universales (ufuncs)

NumPy trae versiones vectorizadas de las funciones matemáticas:

```python
np.sqrt(v), np.exp(v), np.log(v), np.abs(v), np.round(v, 2)
np.maximum(a, b)            # máximo elemento a elemento (no confundir con np.max, que reduce)
np.hypot(x, y)              # sqrt(x² + y²)
np.clip(v, 0, 100)          # acota cada valor al rango [0, 100]
```

`math.sqrt` **no** funciona con arrays (espera un número). Dentro de código NumPy, usá siempre
`np.sqrt` y compañía.

## Condicionales vectorizados: `np.where` y `np.select`

Un `if` dentro de un bucle se reemplaza por `np.where(condicion, si_verdadero, si_falso)`:

```python
# 10 % de descuento a los precios mayores a 200
np.where(precios > 200, precios * 0.9, precios)     # [100. 225.  80.]
```

Para varias ramas, `np.select`:

```python
condiciones = [temps < 10, temps < 25]
opciones = ["frío", "templado"]
np.select(condiciones, opciones, default="calor")
```

## Por qué es tan rápido

Un `for` de Python sobre un array hace, **por cada elemento**:

1. crear un objeto Python (un `float` o un `int` con su cabecera),
2. buscar el método `__mul__` y despacharlo dinámicamente,
3. verificar tipos y manejar el contador de referencias.

La operación vectorizada, en cambio, recorre memoria contigua con un tipo conocido, en un bucle
de C compilado que además puede usar instrucciones SIMD del procesador. Con un millón de
elementos:

```python
v = np.random.default_rng(0).random(1_000_000)

# Python puro: ~150 ms
sum(x * x for x in v)

# NumPy: ~1 ms
(v * v).sum()        # o np.dot(v, v), o np.sum(v ** 2)
```

Medilo vos con `timeit`:

```python
import timeit
timeit.timeit(lambda: (v * v).sum(), number=100) / 100
```

### Anti-patrones que matan la performance

```python
# ✗ append en un bucle
res = np.array([])
for x in datos:
    res = np.append(res, f(x))     # ¡copia TODO el array en cada vuelta: O(n²)!

# ✗ np.vectorize "para que sea rápido"
f_vec = np.vectorize(f)            # es un for de Python con otra cara: NO acelera
```

Si una operación no se puede expresar con ufuncs, `where`, slicing o agregaciones, vale la pena
repensar el algoritmo antes de recurrir a un bucle. Si no hay alternativa, existen **Numba**
(compila funciones con `@njit`) o Cython.

## Pensar vectorizado: un ejemplo

"Para cada día, ¿cuánto subió el precio respecto del día anterior, en porcentaje?"

```python
precios = np.array([100, 102, 99, 105])
# Bucle: for i in range(1, len(precios)): (precios[i] - precios[i-1]) / precios[i-1]
cambios = precios[1:] / precios[:-1] - 1      # [ 0.02  -0.0294  0.0606]
```

Comparar `a[1:]` con `a[:-1]` (el array "corrido" un lugar) es un truco que vas a ver en todo el
análisis de datos. En pandas es `pct_change()`.

## Resumen

- Las operaciones entre arrays (y con escalares) son elemento a elemento.
- Ufuncs (`np.sqrt`, `np.exp`, `np.maximum`, `np.clip`…) en lugar de `math` y de bucles.
- `np.where` / `np.select` reemplazan al `if` dentro del bucle.
- La vectorización es entre 10 y 100 veces más rápida: memoria contigua, tipos conocidos y
  bucles en C.
- Evitá `np.append` en bucles y no esperes milagros de `np.vectorize`.

## Ejercicio

Cuatro funciones sin bucles de Python. Una de ellas tiene un test que **mide** que tu versión
sea mucho más rápida que un bucle.

**Para profundizar:** [Universal functions](https://numpy.org/doc/stable/reference/ufuncs.html),
[Why is NumPy fast?](https://numpy.org/doc/stable/user/whatisnumpy.html#why-is-numpy-fast)
