# Dicts, defaultdict y Counter

El dict es la estructura central de Python: con dicts se implementan los objetos, los
módulos, los namespaces y los kwargs. Saber usarlo bien, junto con sus variantes de
`collections`, elimina una gran cantidad de código repetitivo: contadores a mano,
`if clave not in d` y `try/except KeyError`.

## Lo básico que conviene tener fresco

- Los dicts **conservan el orden de inserción** (garantizado desde 3.7).
- Las claves tienen que ser **hashables**: `str`, `int`, `tuple` de hashables y
  `frozenset` sirven; `list`, `dict` y `set` no.
- Buscar, insertar y borrar cuestan O(1) en promedio.
- `k in d` pregunta por **claves** (no hace falta `.keys()`).

## Leer sin romperse: `get`, `setdefault` y `pop`

```python
precios = {"pan": 1200}

precios["leche"]                 # KeyError
precios.get("leche")             # None
precios.get("leche", 0)          # 0

precios.pop("pan")               # 1200 y la saca
precios.pop("pan", None)         # None; sin default, levanta KeyError
```

`setdefault(k, default)` devuelve el valor de `k` y, si no existe, primero lo inserta con
`default`. Sirve para agrupar sin un `if`:

```python
grupos = {}
for palabra in palabras:
    grupos.setdefault(palabra[0], []).append(palabra)
```

Tiene un detalle: el `default` se construye **siempre**, aunque la clave ya exista. En el
ejemplo se crea una lista vacía en cada vuelta y casi siempre se descarta. Para agrupar,
`defaultdict` queda más limpio.

## `defaultdict`: valores por defecto automáticos

```python
from collections import defaultdict

grupos = defaultdict(list)          # recibe una FÁBRICA (list, int, set…), no un valor
for palabra in palabras:
    grupos[palabra[0]].append(palabra)

conteo = defaultdict(int)           # int() == 0
for letra in texto:
    conteo[letra] += 1
```

Cuando accedés con `[]` a una clave que no existe, `defaultdict` llama a la fábrica, guarda
el resultado y te lo devuelve.

### Cuidado con los efectos secundarios

```python
d = defaultdict(list)
if d["x"]:          # ¡esto CREA la clave "x" con []!
    ...
"x" in d            # True
```

Leer con `[]` inserta la clave. Para consultar sin modificar, usá `in` o `.get()`. Por la
misma razón, **no devuelvas un `defaultdict` desde una API pública**: quien lo reciba puede
crear claves sin darse cuenta. Convertilo antes con `dict(grupos)`.

## `Counter`: contar cosas

```python
from collections import Counter

c = Counter("abracadabra")
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

c["a"]             # 5
c["z"]             # 0  <- no levanta KeyError ni inserta la clave
c.most_common(2)   # [('a', 5), ('b', 2)]
c.total()          # 11 (3.10+)
```

`most_common` ordena por cantidad y, **ante empates, respeta el orden en que cada elemento
apareció por primera vez**. Con eso se resuelve un "top N" sin ordenar a mano.

`Counter` también tiene aritmética de multiconjuntos:

```python
stock   = Counter(manzana=3, pera=1)
pedido  = Counter(manzana=2, pera=2)

stock - pedido      # Counter({'manzana': 1})  <- descarta los <= 0
pedido - stock      # Counter({'pera': 1})      <- lo que falta
stock + pedido      # suma cantidades
stock & pedido      # mínimo de cada uno
stock | pedido      # máximo de cada uno
```

`pedido - stock` vacío (falsy) significa "alcanza con el stock". Es un truco muy práctico
para problemas de anagramas y de disponibilidad.

## Construir e invertir dicts

```python
dict(zip(claves, valores))                  # a partir de dos listas
dict.fromkeys(["a", "b"], 0)                # {'a': 0, 'b': 0}
{v: k for k, v in d.items()}                # invertir si los valores son únicos

# Si los valores se repiten, invertir agrupando:
inverso = defaultdict(list)
for k, v in d.items():
    inverso[v].append(k)
```

> `dict.fromkeys(claves, [])` es una trampa: **todas** las claves comparten la misma lista.
> Usá una comprehension: `{k: [] for k in claves}`.

## Fusionar y actualizar

```python
a | b          # nuevo dict (3.9+); b pisa a a
a |= b         # actualiza a en el lugar (como a.update(b))
{**a, **b}     # equivalente a a | b, anterior a 3.9
```

## Otros de `collections` que vale la pena conocer

| Tipo           | Para qué                                                              |
|----------------|-----------------------------------------------------------------------|
| `deque`        | cola con append/pop O(1) en los dos extremos (lo vemos en algoritmos) |
| `ChainMap`     | buscar en varios dicts en capas (por ejemplo, config → env → defaults) sin copiarlos |
| `OrderedDict`  | casi obsoleto: tiene `move_to_end` y su igualdad tiene en cuenta el orden |
| `namedtuple`   | tupla con nombres; hoy suele preferirse `typing.NamedTuple`           |

## Resumen

| Querés…                                | Usá                                    |
|----------------------------------------|----------------------------------------|
| leer con un default                    | `d.get(k, default)`                    |
| agrupar                                | `defaultdict(list)` y después `dict()` |
| contar                                 | `Counter(iterable)`                    |
| top N por frecuencia                   | `Counter(...).most_common(n)`          |
| saber si alcanza un stock              | `not (pedido - stock)`                 |
| quitar sin fallar                      | `d.pop(k, None)`                       |

## Ejercicio

Cuatro funciones: agrupar, contar palabras, invertir agrupando y un problema de
disponibilidad con aritmética de `Counter`.

**Para profundizar:** [collections — Container datatypes](https://docs.python.org/3/library/collections.html),
*Fluent Python* (2.ª ed.), cap. 3.
