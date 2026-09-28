# Ordenar: sorted, key y comparaciones

En Python casi nunca se escribe una función de comparación. Se ordena indicando **por qué
valor** comparar cada elemento con el parámetro `key`. Esa idea alcanza para resolver desde
"por edad" hasta "por país ascendente y fecha descendente".

## `sorted` vs. `list.sort`

```python
nums = [3, 1, 2]

ordenada = sorted(nums)   # devuelve una lista NUEVA; nums no cambia
nums.sort()               # ordena EN EL LUGAR y devuelve None
```

- `sorted(iterable)` acepta **cualquier iterable** (sets, claves de dict, generadores) y
  siempre devuelve una lista.
- `lista.sort()` solo existe en listas, no copia y devuelve `None`.

Un error clásico es `nums = nums.sort()`, que deja `nums` en `None`. La convención de la
stdlib es que los métodos que mutan un objeto devuelven `None`, justamente para que no se
confundan con los que devuelven un valor nuevo.

Los dos aceptan los mismos parámetros: `key` y `reverse`.

## `key`: ordenar por una proyección

`key` recibe una función que se aplica **una vez por elemento**. Se ordena según el valor
que devuelve:

```python
palabras = ["banana", "Ana", "cereza", "ábaco"]

sorted(palabras)                     # ['Ana', 'banana', 'cereza', 'ábaco']  (por código Unicode)
sorted(palabras, key=str.lower)      # ['Ana', 'banana', 'cereza', 'ábaco']
sorted(palabras, key=len)            # ['Ana', 'ábaco', 'banana', 'cereza']

personas = [{"nombre": "Zoe", "edad": 30}, {"nombre": "Ana", "edad": 25}]
sorted(personas, key=lambda p: p["edad"])
```

> Para ordenar texto en español "como en un diccionario" (con `á` junto a la `a`) hace falta
> `locale.strxfrm` o una librería como PyICU. `str.lower` no alcanza para los acentos.

## Varias claves: tuplas

Las tuplas se comparan **elemento a elemento**: primero el primero y, si empatan, el
segundo, y así. Eso permite ordenar por varios criterios devolviendo una tupla en `key`:

```python
# Por edad y, a igual edad, por nombre
sorted(personas, key=lambda p: (p["edad"], p["nombre"]))
```

### Mezclar ascendente y descendente

`reverse=True` invierte **todo**. Si necesitás un criterio descendente y otro ascendente,
tenés dos caminos:

**1. Negar la clave numérica.** Es lo más directo cuando la clave descendente es un número:

```python
# Edad descendente, nombre ascendente
sorted(personas, key=lambda p: (-p["edad"], p["nombre"]))
```

**2. Ordenar en varias pasadas, aprovechando la estabilidad.** El sort de Python es
**estable**: si dos elementos empatan en la clave, conservan el orden relativo que traían.
Por eso se puede ordenar primero por el criterio *menos* importante y después por el *más*
importante:

```python
res = sorted(personas, key=lambda p: p["nombre"])            # criterio secundario
res = sorted(res, key=lambda p: p["edad"], reverse=True)     # criterio principal
```

Esta segunda forma sirve también para claves que no se pueden negar, como strings.

## `operator.itemgetter` y `attrgetter`

Para los casos típicos de "ordenar por un campo", el módulo `operator` tiene funciones ya
hechas que además son un poco más rápidas que una lambda:

```python
from operator import attrgetter, itemgetter

sorted(filas, key=itemgetter("pais"))              # == lambda f: f["pais"]
sorted(filas, key=itemgetter("pais", "ciudad"))    # devuelve una tupla: varias claves
sorted(tuplas, key=itemgetter(1))                  # por el segundo elemento
sorted(usuarios, key=attrgetter("apellido", "nombre"))
```

## `min`, `max` y `heapq` también aceptan `key`

No hace falta ordenar todo para encontrar un extremo:

```python
max(productos, key=lambda p: p["precio"])          # el más caro: O(n)
min(palabras, key=len)                             # la más corta
max([], default=None)                              # evita ValueError con vacíos

import heapq
heapq.nlargest(3, productos, key=lambda p: p["precio"])   # top 3 sin ordenar todo
```

Ordenar cuesta O(n log n). Si solo querés el máximo, `max` es O(n), y para "los k mayores"
con k chico, `heapq.nlargest` es más eficiente.

## Ordenar dicts

Un dict no tiene un método para ordenarse, pero se puede construir uno nuevo con el orden
que quieras, porque los dicts conservan el orden de inserción:

```python
stock = {"pera": 3, "manzana": 10, "uva": 7}

dict(sorted(stock.items()))                           # por clave
dict(sorted(stock.items(), key=itemgetter(1)))        # por valor
sorted(stock, key=stock.get, reverse=True)            # claves por valor desc: ['manzana', 'uva', 'pera']
```

## Trampas comunes

- `lista = lista.sort()` deja la lista en `None`.
- Mezclar tipos incomparables: `sorted([1, "2"])` levanta `TypeError` en Python 3.
- `None` en los datos: `sorted([3, None])` falla. Una solución es
  `key=lambda x: (x is None, x or 0)` para mandar los `None` al final.
- Ordenar strings con números: `sorted(["10", "9"])` da `['10', '9']`. Si son números,
  convertilos en la clave: `key=int`.

## Resumen

| Querés…                                  | Usá                                           |
|------------------------------------------|-----------------------------------------------|
| una copia ordenada                       | `sorted(xs)`                                  |
| ordenar en el lugar                      | `xs.sort()`                                   |
| por un campo                             | `key=itemgetter("campo")` / `attrgetter`      |
| por varios campos                        | `key=lambda x: (x.a, x.b)`                    |
| un criterio desc y otro asc              | negar el numérico, o dos pasadas estables     |
| solo el máximo o el mínimo               | `max(xs, key=...)`, `min(...)`                |
| los k mayores                            | `heapq.nlargest(k, xs, key=...)`              |

## Ejercicio

Cuatro funciones de ordenamiento: con claves compuestas, `max` con `key` e `itemgetter`.

**Para profundizar:** [Sorting HOW TO](https://docs.python.org/3/howto/sorting.html) (en la
documentación oficial, muy recomendable).
