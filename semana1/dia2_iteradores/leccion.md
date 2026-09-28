# Día 2: Iteradores, generadores e itertools

**Objetivo:** entender el protocolo de iteración y usar pipelines perezosos, que es lo que
separa código Python que escala del que carga todo en memoria.

## 1. Iterable vs. iterador

- **Iterable:** tiene `__iter__()` y devuelve un iterador nuevo, por ejemplo `list`, `dict`,
  `str`, `range` o un archivo.
- **Iterador:** tiene `__next__()` (y `__iter__` que devuelve `self`). Se **consume una vez**.

```python
it = iter([1, 2])
next(it)  # 1
next(it)  # 2
next(it)  # StopIteration
```

El `for` hace exactamente eso: llama a `iter()` y después a `next()` hasta `StopIteration`.

**Trampa:** si una función recibe un iterador (por ejemplo un generador) y lo recorre dos
veces, la segunda vuelta está vacía. Si necesitás recorrer dos veces, pedí una colección o
materializá con `list()`.

## 2. Generadores

Una función con `yield` devuelve un generador: un iterador que ejecuta el cuerpo de a pedazos.

```python
def leer_grande(path):
    with open(path) as f:
        for linea in f:  # el archivo ya es un iterador perezoso
            yield linea.rstrip()


def arbol(nodo):
    yield nodo
    for hijo in nodo.hijos:
        yield from arbol(hijo)  # delega en otro iterable
```

Generator expressions: `(f(x) for x in xs if cond(x))`. Si es el único argumento, no hacen
falta paréntesis extra: `sum(x * x for x in xs)`.

## 3. Pipelines perezosos

```python
lineas = open("access.log")
datos = (parsear(l) for l in lineas)
errores = (d for d in datos if d.status >= 500)
primeros = list(itertools.islice(errores, 10))  # lee solo lo necesario
```

Nada se ejecuta hasta que alguien pide elementos. Con este patrón se procesa un archivo de
50 GB con memoria constante.

## 4. itertools y amigos (los que más se usan)

| Función                        | Para qué                                           |
|--------------------------------|----------------------------------------------------|
| `islice(it, n)`                | cortar un iterador (no admite `it[:n]`)            |
| `count()`, `cycle()`, `repeat()` | secuencias infinitas                             |
| `chain(a, b)` / `chain.from_iterable` | concatenar iterables                        |
| `groupby(it, key)`             | agrupar **consecutivos** (ordená antes si hace falta) |
| `pairwise(it)` (3.10)          | `(a, b), (b, c), ...`                              |
| `batched(it, n)` (3.12)        | lotes de tamaño n                                  |
| `combinations`, `permutations`, `product` | combinatoria                           |
| `accumulate(it)`               | sumas parciales (o cualquier función binaria)      |
| `zip_longest`                  | zip rellenando el más corto                        |

También sirven `any()`, `all()`, `sum()`, `min()`, `max()` y `sorted()`, que consumen
iterables, y `collections.deque(maxlen=n)` para ventanas.

## 5. Walrus en bucles (preview del día 5)

```python
while lote := tuple(islice(it, n)):
    procesar(lote)
```

## Ejercicios

```bash
uv run pytest semana1/dia2_iteradores
```

**Reto extra:** reescribí `en_lotes` con `itertools.batched` y `ventanas` sin `deque`, usando
`itertools.tee` + `islice`.

## Para profundizar

- [Doc de itertools](https://docs.python.org/3/library/itertools.html). La sección "Itertools
  Recipes" es oro.
- *Fluent Python*, cap. 17 ("Iterators, Generators, and Classic Coroutines").
