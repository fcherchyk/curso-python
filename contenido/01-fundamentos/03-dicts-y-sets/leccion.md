# Dicts y sets: lo esencial

Los dos se implementan con **tablas hash**. Eso les da búsqueda, inserción y borrado en O(1)
promedio, y también la restricción de que sus claves o elementos tienen que ser
**hashables**. Este capítulo cubre la base; los patrones avanzados (`defaultdict`, `Counter`,
fusión con `|`) están en el módulo 02.

## Dicts: mapeos clave → valor

```python
edades = {"ana": 31, "beto": 27}
edades["caro"] = 40            # insertar o reemplazar
edades["ana"]                  # 31
edades["zoe"]                  # KeyError
edades.get("zoe")              # None
edades.get("zoe", 0)           # 0
"ana" in edades                # True (busca en las CLAVES, en O(1))
del edades["beto"]
len(edades)                    # 2
```

Otras formas de construirlos:

```python
dict(ana=31, beto=27)                    # con keywords (claves string válidas)
dict([("ana", 31), ("beto", 27)])        # desde pares
dict(zip(nombres, edades))
{n: len(n) for n in nombres}             # comprehension
```

### Recorrerlos

```python
for nombre in edades:                    # claves
for edad in edades.values():
for nombre, edad in edades.items():
```

`keys()`, `values()` e `items()` devuelven **vistas**: no son copias, sino ventanas al dict
que reflejan los cambios. Las vistas de `keys()` e `items()` además soportan operaciones de
conjunto: `d1.keys() & d2.keys()` da las claves en común.

### Orden

Desde Python 3.7, los dicts **conservan el orden de inserción**. Reemplazar el valor de una
clave existente no cambia su posición; borrarla y volver a insertarla la manda al final.

## Hashable: qué puede ser clave

Un objeto es hashable si tiene un `hash()` que no cambia durante su vida y se puede comparar
con `==`. En la práctica:

- **Sí:** `int`, `float`, `str`, `bytes`, `bool`, `None`, `tuple` (si todo lo que contiene es
  hashable), `frozenset`, las clases propias (por defecto se hashean por identidad) y las
  dataclasses con `frozen=True`.
- **No:** `list`, `dict`, `set`, es decir, los contenedores mutables.

La regla tiene sentido: si una clave mutable cambiara después de insertarla, su hash dejaría
de coincidir con el lugar de la tabla donde quedó guardada y no se la podría volver a encontrar.

```python
{[1, 2]: "x"}          # TypeError: unhashable type: 'list'
{(1, 2): "x"}          # ✓
```

## Sets: colecciones sin repetidos

```python
colores = {"rojo", "verde"}
vacio = set()                   # ¡{} es un dict vacío, no un set!
colores.add("azul")
colores.discard("negro")        # no falla si no está (remove sí levantaría KeyError)
"rojo" in colores               # O(1)

set([3, 1, 3, 2])               # {1, 2, 3}  elimina duplicados
```

El caso de uso principal de un set es preguntar **"¿está X?"** muchas veces. En una lista,
cada `in` es O(n); en un set, O(1). Si vas a buscar en un bucle, convertí la lista a set
**una vez** antes:

```python
prohibidas = set(lista_prohibidas)          # O(n) una sola vez
limpias = [p for p in palabras if p not in prohibidas]   # cada `in` es O(1)
```

### Álgebra de conjuntos

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}

a | b     # {1, 2, 3, 4, 5}   unión
a & b     # {3, 4}            intersección
a - b     # {1, 2}            diferencia (en a y no en b)
a ^ b     # {1, 2, 5}         diferencia simétrica (en uno solo)
{1, 2} <= a                   # subconjunto
a.isdisjoint({9})             # sin elementos en común
```

Los métodos equivalentes (`a.union(lista)`, `a.intersection(...)`) aceptan cualquier
iterable, no solo sets.

### El orden de un set no está garantizado

Un set **no** mantiene el orden de inserción. Si necesitás "únicos en el orden en que
aparecen", el truco idiomático usa un dict, que sí lo conserva:

```python
list(dict.fromkeys(["b", "a", "b", "c", "a"]))    # ['b', 'a', 'c']
```

Si el resultado final tiene que ser determinista (por ejemplo, para comparar en un test),
ordenalo: `sorted(conjunto)`.

### `frozenset`

Es la versión inmutable y hashable de un set. Sirve como clave de dict o como elemento de
otro set:

```python
grupos_vistos = {frozenset({"ana", "beto"})}
frozenset({"beto", "ana"}) in grupos_vistos     # True: el orden no importa
```

## Elegir la estructura

| Necesitás…                                   | Usá             |
|----------------------------------------------|-----------------|
| orden y repetidos, acceso por posición       | `list`          |
| registro fijo o clave compuesta              | `tuple`         |
| buscar por clave y asociarle datos           | `dict`          |
| pertenencia rápida, sin repetidos            | `set`           |
| lo mismo pero inmutable o como clave         | `frozenset`     |
| únicos respetando el orden                   | `dict.fromkeys` |

## Resumen

- Dicts y sets son tablas hash: `in` cuesta O(1) y las claves tienen que ser hashables.
- `d[k]` falla si no existe la clave; `d.get(k, default)` no.
- `{}` es un dict; el set vacío es `set()`.
- Los sets no tienen orden: para únicos en orden, `dict.fromkeys`.
- Si buscás muchas veces en una lista, convertila a set una vez.

## Ejercicio

Cuatro funciones que se resuelven con sets y dicts, sin bucles anidados.

**Para profundizar:** [Mapping types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict),
[Set types](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset).
