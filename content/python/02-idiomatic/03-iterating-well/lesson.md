# Iterar bien: enumerate, zip y compañía

El `for` de Python no es un `for (i = 0; i < n; i++)`: recorre **elementos**, no índices.
Casi todo el código que "huele a otro lenguaje" viene de pelearse con eso y reconstruir
índices a mano. Este capítulo presenta las herramientas que evitan hacerlo: `enumerate`,
`zip`, `reversed`, `itertools.pairwise`, `any` y `all`.

## El anti-patrón `range(len(...))`

```python
# ✗ Estilo C
for i in range(len(nombres)):
    print(nombres[i])

# ✓ Python
for nombre in nombres:
    print(nombre)
```

La versión con índice tiene más ruido, deja lugar a errores de uno más o uno menos y solo
funciona con secuencias indexables. El `for` directo funciona con **cualquier iterable**:
archivos, generadores, sets, claves de un dict o resultados de una query.

## `enumerate`: cuando también necesitás el índice

```python
for i, nombre in enumerate(nombres):
    print(i, nombre)

for n, linea in enumerate(archivo, start=1):   # numerar desde 1
    print(f"{n:>4} | {linea}", end="")
```

`enumerate` devuelve pares `(índice, elemento)` que se desempaquetan en el `for`. El
parámetro `start` cambia desde qué número cuenta; no saltea elementos.

## `zip`: recorrer varias secuencias en paralelo

```python
nombres = ["ana", "beto", "caro"]
notas   = [9, 7, 8]

for nombre, nota in zip(nombres, notas):
    print(nombre, nota)

dict(zip(nombres, notas))        # {'ana': 9, 'beto': 7, 'caro': 8}
```

### El problema del largo distinto y `strict=True` (3.10+)

Por defecto, `zip` **corta en la secuencia más corta sin avisar**:

```python
list(zip([1, 2, 3], ["a", "b"]))                 # [(1, 'a'), (2, 'b')]  <- ¡el 3 se perdió!
list(zip([1, 2, 3], ["a", "b"], strict=True))    # ValueError
```

Esto causa bugs silenciosos cuando dos listas "deberían" tener el mismo largo y por un error
anterior no lo tienen. **Regla práctica:** si las secuencias tienen que medir lo mismo, usá
`strict=True`. Si querés completar la más corta con un valor por defecto, está
`itertools.zip_longest(a, b, fillvalue=None)`.

### `zip` para "des-zipear"

`zip(*pares)` hace la operación inversa: convierte una lista de pares en dos tuplas.

```python
pares = [("ana", 9), ("beto", 7)]
nombres, notas = zip(*pares)     # ('ana', 'beto'), (9, 7)
```

## Elementos consecutivos: `pairwise` (3.10+)

Para comparar cada elemento con el siguiente, no hacen falta índices:

```python
from itertools import pairwise

temps = [18, 21, 19, 25]
[b - a for a, b in pairwise(temps)]    # [3, -2, 6]

# Antes de 3.10 (o con listas), el truco equivalente:
[b - a for a, b in zip(temps, temps[1:])]
```

`pairwise` funciona con cualquier iterable, incluso con generadores que no se pueden
recortar con `[1:]`.

## Recorrer al revés y ordenado

```python
for x in reversed(xs): ...        # sin copiar la lista (xs[::-1] sí copia)
for x in sorted(xs): ...          # recorre una copia ordenada; xs no cambia
for k in sorted(d): ...           # claves de un dict en orden
```

## `any` y `all`: preguntas sobre toda la colección

```python
any(n < 0 for n in nums)          # ¿hay algún negativo?
all(u.activo for u in usuarios)   # ¿están todos activos?
```

Las dos **cortan en cuanto saben la respuesta**: `any` se detiene en el primer verdadero
y `all` en el primer falso. Con un generator expression como argumento, además, no
construyen ninguna lista intermedia.

Casos borde que conviene recordar: `any([])` es `False` y `all([])` es `True`. En una
colección vacía no hay ningún elemento que falle.

## Recorrer dicts

```python
for clave in d:                   # claves (no hace falta .keys())
for valor in d.values():
for clave, valor in d.items():
```

Una trampa: **no agregues ni borres claves de un dict mientras lo recorrés**, porque
Python levanta `RuntimeError: dictionary changed size during iteration`. Si necesitás
hacerlo, recorré una copia (`for k in list(d):`) o construí un dict nuevo con una
comprehension.

## Resumen

| En vez de                                   | Usá                                     |
|---------------------------------------------|-----------------------------------------|
| `for i in range(len(xs)): xs[i]`            | `for x in xs`                           |
| llevar un contador a mano                   | `for i, x in enumerate(xs, start=1)`    |
| índices para recorrer dos listas            | `for a, b in zip(xs, ys, strict=True)`  |
| `xs[i+1] - xs[i]` con índices               | `for a, b in pairwise(xs)`              |
| `xs[::-1]` solo para recorrer               | `reversed(xs)`                          |
| un bucle con `flag = True` y `break`        | `any(...)` / `all(...)`                 |
| `if len(xs) == 0`                           | `if not xs`                             |

## Ejercicio

Cuatro funciones que se resuelven con `enumerate`, `zip` y `pairwise`, sin `range(len(...))`.

**Para profundizar:** [Built-in functions: enumerate, zip](https://docs.python.org/3/library/functions.html#enumerate),
[PEP 618 — zip strict](https://peps.python.org/pep-0618/),
[itertools.pairwise](https://docs.python.org/3/library/itertools.html#itertools.pairwise).
