# Día 3: Funciones, closures, decoradores y context managers

**Objetivo:** dominar las herramientas en las que se apoyan casi todos los frameworks. Las
rutas de FastAPI y Flask, las fixtures de pytest y los `@property` son decoradores; las
sesiones de base de datos y las transacciones son context managers.

## 1. Las funciones son objetos

```python
ops = {"+": operator.add, "*": operator.mul}
ops["+"](2, 3)  # 5
sorted(xs, key=len)  # pasar funciones como argumento
from functools import partial

int_base2 = partial(int, base=2)  # fijar argumentos
```

## 2. Closures y `nonlocal`

Una función interna "recuerda" las variables del scope donde se definió.

```python
def multiplicador(k):
    def f(x):
        return x * k  # k queda capturada

    return f


def acumulador():
    total = 0

    def sumar(x):
        nonlocal total  # sin esto, `total += x` da UnboundLocalError
        total += x
        return total

    return sumar
```

**Trampa:** las closures capturan variables, no valores.
`[lambda: i for i in range(3)]` devuelve funciones que dan `2` las tres. La solución es
`lambda i=i: i`.

## 3. Decoradores

`@deco` sobre `def f` es azúcar para `f = deco(f)`.

```python
import functools


def loguear(func):
    @functools.wraps(func)  # preserva __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        print(f"llamando {func.__name__}")
        return func(*args, **kwargs)

    return wrapper
```

Un **decorador con parámetros** es una función que devuelve un decorador, así que son tres
niveles:

```python
def repetir(n):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(n)]

        return wrapper

    return decorador


@repetir(3)
def hola(): ...
```

Decoradores de la biblioteca estándar que tenés que conocer: `@functools.cache` /
`@lru_cache(maxsize=...)`, `@property`, `@staticmethod`, `@classmethod`,
`@dataclass`, `@contextmanager` y `@functools.singledispatch`.

## 4. Context managers

Garantizan limpieza (cerrar, liberar, restaurar) aunque haya excepciones.

**Con clase:**

```python
class Conexion:
    def __enter__(self):
        self.abrir()
        return self  # es lo que queda en `as`

    def __exit__(self, exc_type, exc, tb):
        self.cerrar()
        return False  # True = suprime la excepción (casi nunca)
```

**Con generador (más común):**

```python
from contextlib import contextmanager


@contextmanager
def transaccion(db):
    db.begin()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
```

Más de contextlib: `suppress(FileNotFoundError)`, `ExitStack` para una cantidad dinámica de
recursos, `closing()`, `redirect_stdout()` y `asynccontextmanager`.

Desde 3.10 se pueden agrupar varios context managers entre paréntesis:

```python
with (
    open("a") as a,
    open("b") as b,
):
    ...
```

## Ejercicios

```bash
uv run pytest semana1/dia3_funciones
```

**Reto extra:** agregale a `memoizar` un parámetro opcional `maxsize` (decorador que funcione
con y sin paréntesis: `@memoizar` y `@memoizar(maxsize=100)`).

## Para profundizar

- *Fluent Python*, cap. 7 y 9 (funciones y decoradores/closures) y cap. 18 (`with`).
- [Doc de contextlib](https://docs.python.org/3/library/contextlib.html).
