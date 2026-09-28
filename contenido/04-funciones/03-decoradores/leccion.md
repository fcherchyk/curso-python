# Decoradores

Un decorador es una función que **recibe una función y devuelve otra**, normalmente una
versión "envuelta" que agrega comportamiento antes o después de la original. Con decoradores
están hechos `@property`, `@dataclass`, `@functools.cache`, las rutas de FastAPI y Flask
(`@app.get(...)`) y las fixtures de pytest. Si entendés las closures, los decoradores son un
paso más.

## `@` es azúcar sintáctico

```python
@mi_decorador
def saludar():
    ...
```

es exactamente lo mismo que:

```python
def saludar():
    ...
saludar = mi_decorador(saludar)
```

El decorador se ejecuta **una sola vez**, al definir la función (normalmente al importar el
módulo). Lo que queda asignado al nombre `saludar` es lo que el decorador devolvió.

## El patrón básico: un wrapper

```python
import functools

def loguear(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"→ {func.__name__}{args}")
        resultado = func(*args, **kwargs)
        print(f"← {func.__name__} = {resultado!r}")
        return resultado
    return wrapper

@loguear
def sumar(a, b):
    return a + b

sumar(2, 3)
# → sumar(2, 3)
# ← sumar = 5
```

Las partes:

1. `loguear` recibe la función original.
2. Define `wrapper`, una **closure** que tiene acceso a `func`.
3. `wrapper` acepta `*args, **kwargs` para servir con **cualquier** firma y los reenvía.
4. **Devuelve el resultado** de la función original (olvidarlo es un bug muy común: la
   función decorada pasa a devolver `None`).
5. `loguear` devuelve `wrapper`, que reemplaza a la original.

## `functools.wraps`: no te lo saltees

Sin `@functools.wraps(func)`, la función decorada pierde su identidad:

```python
sumar.__name__     # 'wrapper'   ← sin wraps
sumar.__doc__      # None
```

Eso rompe tracebacks, logs, documentación, `help()`, frameworks que usan el nombre de la
función (por ejemplo, para registrar rutas) y herramientas de introspección. `wraps` copia
`__name__`, `__doc__`, `__module__`, `__qualname__` y `__dict__`, y agrega `__wrapped__`, que
apunta a la original.

## Decoradores con estado

Como el wrapper es un objeto función, se le pueden colgar atributos. Es la forma más simple
de exponer estado:

```python
def contar_llamadas(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.llamadas += 1
        return func(*args, **kwargs)
    wrapper.llamadas = 0
    return wrapper
```

Otra variante es guardar el estado en la closure (una variable del decorador) y exponerlo
con una función auxiliar.

## Decoradores que no envuelven: registrar

No todos los decoradores devuelven un wrapper. Algunos solo **registran** la función y la
devuelven tal cual. Así funcionan los sistemas de plugins y las rutas de los frameworks web:

```python
COMANDOS = {}

def comando(func):
    COMANDOS[func.__name__] = func
    return func             # la misma función, sin cambios

@comando
def ayuda(): ...

COMANDOS["ayuda"]()
```

## Memoización: el ejemplo clásico

```python
def memoizar(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoizar
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(100)     # instantáneo
```

Esto funciona porque dentro de `fib`, el nombre `fib` apunta a la versión **decorada**, así
que las llamadas recursivas también pasan por el caché.

En código real, usá la versión de la stdlib, que es más completa y está probada:

```python
from functools import cache, lru_cache

@cache                         # sin límite
def fib(n): ...

@lru_cache(maxsize=1024)       # descarta los menos usados
def consultar(id): ...

consultar.cache_info()         # hits, misses, tamaño
consultar.cache_clear()
```

Requisito: los argumentos tienen que ser **hashables**, porque son la clave del caché.

## Apilar decoradores

```python
@loguear
@memoizar
def f(x): ...
```

equivale a `f = loguear(memoizar(f))`: se aplican **de abajo hacia arriba**, y al llamar se
ejecutan de afuera hacia adentro. El orden importa: en este ejemplo se loguean todas las
llamadas, incluidas las que resuelve el caché. Invertidos, solo se loguearían las que
realmente ejecutan `f`.

## Decoradores de la stdlib que tenés que reconocer

| Decorador                     | Para qué                                               |
|-------------------------------|--------------------------------------------------------|
| `@functools.cache` / `lru_cache` | memoización                                         |
| `@functools.wraps`            | preservar metadatos en tus decoradores                 |
| `@property`                   | atributo calculado (módulo de modelado)                |
| `@classmethod`, `@staticmethod` | métodos de clase y estáticos                         |
| `@dataclass`                  | genera `__init__`, `__repr__` y `__eq__`               |
| `@contextlib.contextmanager`  | context manager a partir de un generador               |
| `@functools.singledispatch`   | sobrecarga según el tipo del primer argumento          |
| `@typing.override` (3.12)     | marca que un método sobrescribe al de la clase padre   |

## Resumen

- `@deco` sobre `def f` equivale a `f = deco(f)`, y se ejecuta una vez, al definir.
- El patrón: una closure `wrapper(*args, **kwargs)` que llama a `func` y **devuelve su
  resultado**.
- **Siempre** `@functools.wraps(func)`.
- Hay decoradores que solo registran y devuelven la misma función.
- Se apilan de abajo hacia arriba.
- Para cachear, `functools.cache` y `lru_cache`.

## Ejercicio

Tres decoradores: uno con estado en un atributo, un memoizador propio y uno de registro.

**Para profundizar:** [PEP 318 — Decorators](https://peps.python.org/pep-0318/),
[functools](https://docs.python.org/3/library/functools.html), *Fluent Python*, cap. 9.
