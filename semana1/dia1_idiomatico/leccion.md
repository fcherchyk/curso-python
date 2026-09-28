# Día 1: Python idiomático

**Objetivo:** volver a escribir Python "que se lee como Python", no como Java o C traducido.
**Tiempo:** unos 20 min de lectura y 40 min de ejercicios.

## 1. Comprehensions

```python
cuadrados = [x * x for x in nums if x % 2 == 0]  # list
por_id = {u.id: u for u in usuarios}  # dict
dominios = {email.split("@")[1] for email in emails}  # set
total = sum(p.precio for p in productos)  # generator (sin corchetes)
plano = [x for fila in matriz for x in fila]  # anidada: mismo orden que los for
```

Regla práctica: si la comprehension necesita más de un `if` o dos `for`, usá un bucle normal
o una función auxiliar.

## 2. Desempaquetado

```python
a, b = b, a  # swap
primero, *resto = [1, 2, 3]  # primero=1, resto=[2, 3]
*init, ultimo = "abc"  # init=['a', 'b'], ultimo='c'
for i, (x, y) in enumerate(puntos):
    ...
merged = {**defaults, **config}  # o mejor en 3.9+: defaults | config
llamar(*args, **kwargs)
```

## 3. Iterar bien

| En vez de                                    | Usá                                          |
|----------------------------------------------|----------------------------------------------|
| `for i in range(len(xs)): xs[i]`              | `for x in xs` / `for i, x in enumerate(xs)`  |
| índices para recorrer dos listas             | `zip(a, b, strict=True)` (3.10+)             |
| `if len(xs) == 0`                            | `if not xs`                                  |
| `d.has_key(k)` / `k in d.keys()`             | `k in d`                                     |
| `try: d[k] except KeyError: d[k] = []`       | `d.setdefault(k, [])` o `defaultdict(list)`  |
| contar a mano con un dict                    | `Counter(xs)`, `.most_common(n)`             |

`zip(strict=True)` levanta `ValueError` si los largos no coinciden. Sin `strict`, el sobrante
se pierde en silencio y es una fuente clásica de bugs.

## 4. Ordenar

```python
sorted(personas, key=lambda p: p.edad)  # asc
sorted(personas, key=lambda p: (-p.edad, p.nombre))  # edad desc, nombre asc
sorted(palabras, key=str.lower)
max(productos, key=lambda p: p.precio)
from operator import attrgetter, itemgetter

sorted(filas, key=itemgetter("pais", "ciudad"))
```

El sort de Python es **estable**, así que se pueden encadenar ordenamientos por varias claves
(de la menos a la más importante).

## 5. Firmas de funciones

```python
def f(pos_only, /, normal, *args, kw_only, **kwargs): ...
```

- Lo que va antes de `/` es **solo posicional** (3.8+).
- Lo que va después de `*` o `*args` es **solo keyword**. Sirve para flags booleanos:
  `conectar(host, timeout=5, reintentar=True)` se lee mucho mejor que `conectar(host, 5, True)`.
- **Trampa clásica:** los defaults mutables se evalúan una sola vez.

```python
def mal(x, acc=[]):          # la misma lista se comparte entre llamadas
def bien(x, acc=None):
    acc = [] if acc is None else acc
```

## 6. Dicts

- Mantienen orden de inserción (garantizado desde 3.7).
- `d | otro` devuelve uno nuevo y `d |= otro` actualiza en el lugar (3.9+).
- `d.get(k, default)`, `d.setdefault(k, [])`, `d.pop(k, None)`.

## 7. Strings

```python
f"{nombre!r} tiene {edad} años"  # !r usa repr
f"{precio:,.2f}"  # 1,234.50
f"{x=}"  # debug: imprime "x=42" (3.8+)
"-".join(partes)  # nunca concatenar en un bucle
s.removeprefix("http://")  # 3.9+
```

## Ejercicios

Abrí `ejercicios.py`, implementá cada función y corré:

```bash
uv run pytest semana1/dia1_idiomatico          # todo el día
uv run pytest semana1/dia1_idiomatico -x       # frena en el primer fallo
uv run pytest semana1/dia1_idiomatico -k url   # solo tests que matchean "url"
```

**Reto extra:** que ninguna solución tenga más de 3 líneas, salvo `construir_url`.

## Para profundizar

- [Python Tutorial: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- *Fluent Python* (2ª ed.), cap. 2 y 3.
- *Effective Python* (3ª ed.), ítems sobre comprehensions y argumentos keyword-only.
