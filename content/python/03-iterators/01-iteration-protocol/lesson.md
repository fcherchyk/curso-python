# El protocolo de iteración

Todo `for` de Python se apoya en dos métodos: `__iter__` y `__next__`. Conocerlos explica
por qué un generador "se vacía" después del primer recorrido, por qué una lista se puede
recorrer infinitas veces y cómo hacer que tus propias clases funcionen con `for`, `list()`,
`sum()`, `in` y el desempaquetado.

## Iterable vs. iterador

Son dos roles distintos y conviene no mezclarlos:

- Un **iterable** es algo que se *puede recorrer*: implementa `__iter__()`, que devuelve un
  **iterador nuevo**. Ejemplos: `list`, `tuple`, `str`, `dict`, `set`, `range` o un archivo.
- Un **iterador** es el que *lleva la cuenta* del recorrido: implementa `__next__()`, que
  devuelve el siguiente elemento o levanta `StopIteration` cuando no quedan más. Además, su
  `__iter__()` devuelve `self`.

```python
nums = [10, 20]          # iterable
it = iter(nums)          # llama a nums.__iter__() → un list_iterator
next(it)                 # 10
next(it)                 # 20
next(it)                 # StopIteration
next(it, "fin")          # 'fin'  ← next con default no levanta
```

## Qué hace realmente un `for`

```python
for x in coleccion:
    cuerpo(x)
```

es equivalente a:

```python
it = iter(coleccion)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    cuerpo(x)
```

Eso es todo el protocolo. Cualquier objeto que respete `__iter__`/`__next__` funciona en un
`for`, en comprehensions, en `list(...)`, `sum(...)`, `zip(...)`, `in` y en el
desempaquetado `a, b = obj`.

## La diferencia que importa: los iteradores se consumen

Un **iterable** entrega un iterador nuevo cada vez que le pedís uno, así que se puede
recorrer muchas veces. Un **iterador** se devuelve a sí mismo, así que se recorre **una sola
vez**:

```python
nums = [1, 2, 3]
list(nums), list(nums)        # ([1, 2, 3], [1, 2, 3])

it = iter(nums)
list(it), list(it)            # ([1, 2, 3], [])   ← el segundo está vacío

gen = (x * 2 for x in nums)   # los generadores son iteradores
sum(gen), sum(gen)            # (12, 0)
```

Este es un bug muy común: una función que recibe "algo iterable" y lo recorre dos veces (por
ejemplo, para calcular el total y después cada porcentaje) funciona con listas y falla **en
silencio** con generadores. Si necesitás dos pasadas, materializá al principio con
`datos = list(datos)`, o pedí una `Sequence` en la anotación de tipo.

## Implementar un iterable propio

La forma más simple y robusta es que `__iter__` sea un **generador** (una función con
`yield`, capítulo siguiente). Cada llamada a `iter()` crea uno nuevo:

```python
class Playlist:
    def __init__(self, canciones: list[str]) -> None:
        self._canciones = canciones

    def __iter__(self):
        for c in self._canciones:
            yield c
        # o directamente: return iter(self._canciones)

p = Playlist(["a", "b"])
list(p), list(p)        # (['a', 'b'], ['a', 'b'])  ✓ se puede recorrer muchas veces
```

## Implementar un iterador "a mano"

Para entender el protocolo (o cuando necesitás estado explícito), se puede escribir la clase
iteradora completa:

```python
class Cuenta:
    def __init__(self, inicio: int, fin: int) -> None:
        self.actual = inicio
        self.fin = fin

    def __iter__(self):
        return self              # un iterador es su propio iterable

    def __next__(self) -> int:
        if self.actual >= self.fin:
            raise StopIteration
        valor = self.actual
        self.actual += 1
        return valor
```

En la práctica casi nunca hace falta: los generadores hacen lo mismo con menos código.
Pero cuando veas `__next__` en una librería, ya sabés qué está pasando.

## Iterables "fáciles": `__getitem__` y `__len__`

Por compatibilidad histórica, si una clase no tiene `__iter__` pero sí `__getitem__` con
índices 0, 1, 2… hasta un `IndexError`, Python también puede iterarla. Hoy conviene
implementar `__iter__` explícitamente: es más claro y funciona con cualquier fuente de datos.

## `iter()` con centinela

`iter(funcion, centinela)` crea un iterador que llama a `funcion()` hasta que devuelve el
centinela. Es muy útil para leer por bloques:

```python
from functools import partial

with open("grande.bin", "rb") as f:
    for bloque in iter(partial(f.read, 4096), b""):
        procesar(bloque)
```

## Herramientas que consumen iterables

`list`, `tuple`, `set`, `dict`, `sum`, `min`, `max`, `any`, `all`, `sorted`, `"".join`,
`enumerate`, `zip`, `map`, `filter`, `reversed` (este último necesita una secuencia o
`__reversed__`) y todo `itertools`. Si tu clase implementa `__iter__`, funciona con todas.

## Resumen

- Iterable: `__iter__` devuelve un iterador **nuevo**. Iterador: `__next__` más
  `__iter__` que devuelve `self`.
- Los iteradores (incluidos los generadores) se consumen una sola vez.
- Si necesitás recorrer dos veces, materializá con `list()`.
- Para tus clases, implementá `__iter__` como generador.
- `next(it, default)` evita el `StopIteration`.

## Ejercicio

Una clase iterable que se puede recorrer muchas veces, un iterador escrito a mano y dos
funciones que usan `next()` e `iter()`.

**Para profundizar:** [Iterator types](https://docs.python.org/3/library/stdtypes.html#iterator-types),
*Fluent Python* (2.ª ed.), cap. 17.
