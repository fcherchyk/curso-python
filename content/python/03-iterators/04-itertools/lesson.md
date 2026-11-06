# itertools: las piezas de lego

`itertools` es un módulo de la stdlib con bloques de construcción para iteradores: están
implementados en C, son perezosos y se combinan entre sí. Muchos bucles con variables
auxiliares, índices y `if`s se reducen a una o dos funciones de `itertools`. Este capítulo
repasa las que más se usan, agrupadas por para qué sirven.

## Cortar y saltear

```python
from itertools import islice, takewhile, dropwhile

islice(it, 5)              # los primeros 5
islice(it, 2, 8, 2)        # como [2:8:2], pero perezoso
takewhile(lambda x: x < 10, nums)   # mientras se cumpla; corta en el primero que falla
dropwhile(lambda l: l.startswith("#"), lineas)   # saltea el encabezado de comentarios
```

`takewhile` y `dropwhile` miran **solo el prefijo**: cuando la condición cambia una vez, no
vuelven a evaluarla. No son un `filter`.

## Infinitos

```python
from itertools import count, cycle, repeat

count(10, 5)               # 10, 15, 20, ...
cycle(["rojo", "verde"])   # rojo, verde, rojo, verde, ...
repeat("x", 3)             # x, x, x   (sin el 3 es infinito)

for i, color in zip(count(1), cycle(["par", "impar"])): ...
```

Combinalos siempre con algo que corte: `islice`, `zip` con un iterable finito, `takewhile` o
un `break`.

## Unir

```python
from itertools import chain

chain([1, 2], (3,), range(4, 6))          # 1, 2, 3, 4, 5
chain.from_iterable(lista_de_listas)      # aplana un nivel, perezoso
```

`chain.from_iterable` es la versión perezosa de `[x for sub in xs for x in sub]`.

## Agrupar: `groupby`

`groupby(iterable, key)` agrupa elementos **consecutivos** que tienen la misma clave:

```python
from itertools import groupby

for letra, grupo in groupby("aaabccaa"):
    print(letra, list(grupo))
# a ['a', 'a', 'a']
# b ['b']
# c ['c', 'c']
# a ['a', 'a']        ← ¡otra vez 'a'! solo agrupa CONSECUTIVOS
```

Para agrupar "todos los que tienen la misma clave", **ordená primero por esa clave**, o usá
un `defaultdict(list)`:

```python
ventas.sort(key=lambda v: v.mes)
for mes, del_mes in groupby(ventas, key=lambda v: v.mes):
    print(mes, sum(v.monto for v in del_mes))
```

Otra trampa: cada `grupo` es un iterador que comparte el iterador de base. Si avanzás al
siguiente grupo, el anterior queda vacío. Si lo necesitás después, convertilo a lista.

## Ventanas y pares

```python
from itertools import pairwise, batched     # pairwise 3.10+, batched 3.12+

list(pairwise([1, 2, 3, 4]))      # [(1, 2), (2, 3), (3, 4)]
list(batched(range(7), 3))        # [(0, 1, 2), (3, 4, 5), (6,)]
```

Para ventanas deslizantes de tamaño `n` no hay una función directa. La receta usa
`collections.deque(maxlen=n)`, que descarta el elemento más viejo al agregar uno nuevo:

```python
from collections import deque

def ventanas(it, n):
    ventana = deque(maxlen=n)
    for x in it:
        ventana.append(x)
        if len(ventana) == n:
            yield tuple(ventana)
```

## Acumular

```python
from itertools import accumulate
import operator

list(accumulate([1, 2, 3, 4]))                   # [1, 3, 6, 10]   sumas parciales
list(accumulate([3, 1, 4, 1, 5], max))           # [3, 3, 4, 4, 5] máximo hasta acá
list(accumulate([1, 2, 3], operator.mul))        # [1, 2, 6]
list(accumulate([100, -30, 50], initial=1000))   # [1000, 1100, 1070, 1120]
```

## Combinatoria

```python
from itertools import product, permutations, combinations, combinations_with_replacement

list(product("ab", [1, 2]))       # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]  bucles anidados
list(product([0, 1], repeat=3))   # las 8 combinaciones de 3 bits
list(permutations("abc", 2))      # 6: importa el orden
list(combinations("abc", 2))      # 3: [('a','b'), ('a','c'), ('b','c')]
```

`product` reemplaza bucles `for` anidados. Cuidado con el tamaño: las permutaciones crecen
factorialmente. Son perezosas, pero recorrerlas todas puede no terminar nunca en la práctica.

## Otras útiles

| Función                       | Para qué                                         |
|-------------------------------|--------------------------------------------------|
| `zip_longest(a, b, fillvalue=)`| zip que completa el más corto                   |
| `starmap(f, pares)`           | `f(*par)` para cada par                          |
| `compress(datos, mascara)`    | filtra según una lista de booleanos              |
| `tee(it, n)`                  | duplica un iterador (guarda en memoria lo que uno lee y el otro no) |
| `filterfalse(pred, it)`       | lo contrario de `filter`                         |

La documentación oficial tiene una sección **"Itertools Recipes"** con decenas de funciones
armadas con estas piezas (`unique_everseen`, `sliding_window`, `roundrobin`…). También las
trae ya hechas el paquete `more-itertools`.

## Resumen

- Cortar: `islice`, `takewhile`, `dropwhile`. Unir: `chain`. Infinitos: `count`, `cycle`, `repeat`.
- `groupby` agrupa solo **consecutivos**: ordená antes.
- `pairwise`, `batched` y la receta de ventanas con `deque(maxlen=n)`.
- `accumulate` para totales parciales; `product`, `permutations` y `combinations` para
  combinatoria.
- Todo es perezoso: combinalo con algo que corte.

## Ejercicio

Cuatro funciones que se resuelven con una o dos piezas de `itertools`.

**Para profundizar:** [itertools](https://docs.python.org/3/library/itertools.html), en
especial la sección de recetas.
