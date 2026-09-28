# Context managers

`with` garantiza que algo se **limpie** (se cierre, se libere, se restaure o se confirme)
pase lo que pase dentro del bloque, incluso si hay una excepción o un `return`. Archivos,
locks, conexiones, transacciones, directorios temporales, mocks en tests: todos se manejan
con context managers.

## El problema que resuelven

```python
f = open("datos.txt")
procesar(f)          # si esto falla...
f.close()            # ...esto nunca se ejecuta
```

La versión correcta sin `with` necesita `try/finally`:

```python
f = open("datos.txt")
try:
    procesar(f)
finally:
    f.close()
```

`with` encapsula ese patrón:

```python
with open("datos.txt") as f:
    procesar(f)
# acá el archivo ya está cerrado, pase lo que pase
```

## El protocolo: `__enter__` y `__exit__`

```python
with expresion as nombre:
    cuerpo
```

hace, aproximadamente, esto:

```python
cm = expresion
nombre = cm.__enter__()
try:
    cuerpo
except BaseException as e:
    if not cm.__exit__(type(e), e, e.__traceback__):
        raise                  # __exit__ devolvió False → la excepción sigue
else:
    cm.__exit__(None, None, None)
```

- `__enter__` prepara el recurso y lo que devuelve queda en la variable del `as`. Muchas veces
  devuelve `self`, pero no siempre.
- `__exit__` recibe la excepción (o tres `None`) y hace la limpieza. Si devuelve `True`, **la
  excepción se suprime**. Casi siempre conviene devolver `None` o `False`.

## Con una clase

```python
import time

class Temporizador:
    def __enter__(self):
        self.inicio = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.duracion = time.perf_counter() - self.inicio
        # sin return → None → no suprime excepciones

with Temporizador() as t:
    hacer_algo()
print(f"tardó {t.duracion:.3f}s")
```

Conviene escribirlo como clase cuando el objeto tiene **más usos** además del `with`, como
atributos o métodos, o cuando se reutiliza.

## Con un generador: `@contextmanager`

Para la mayoría de los casos, `contextlib.contextmanager` es más corto. Todo lo que va antes
del `yield` es el `__enter__`, lo que se entrega con `yield` va al `as`, y lo que va después
es el `__exit__`:

```python
from contextlib import contextmanager
import os

@contextmanager
def en_directorio(ruta):
    anterior = os.getcwd()
    os.chdir(ruta)
    try:
        yield ruta
    finally:
        os.chdir(anterior)         # se ejecuta aunque el bloque falle
```

**El `try/finally` alrededor del `yield` es fundamental.** Si el bloque del `with` levanta una
excepción, se re-levanta **en la línea del `yield`**. Sin `finally`, la limpieza no se
ejecuta.

### Manejar la excepción del bloque

```python
@contextmanager
def transaccion(conexion):
    conexion.begin()
    try:
        yield conexion
    except Exception:
        conexion.rollback()
        raise                      # re-levantar: que quien llama se entere
    else:
        conexion.commit()
```

Si en el `except` **no** re-levantás, la excepción queda suprimida. A veces es lo que se
busca (ver `suppress` más abajo), pero tiene que ser una decisión consciente.

## Varios a la vez

```python
with open("entrada.txt") as src, open("salida.txt", "w") as dst:
    dst.write(src.read())

# 3.10+: entre paréntesis, uno por línea
with (
    open("a.txt") as a,
    open("b.txt") as b,
):
    ...
```

Se entran de izquierda a derecha y se salen en orden inverso.

## La caja de herramientas de `contextlib`

```python
from contextlib import suppress, ExitStack, closing, redirect_stdout, nullcontext

with suppress(FileNotFoundError):          # ignorar una excepción concreta
    os.remove("temporal.txt")

with ExitStack() as stack:                 # cantidad dinámica de recursos
    archivos = [stack.enter_context(open(r)) for r in rutas]

with closing(urlopen(url)) as pagina:      # objetos con .close() pero sin protocolo with
    ...

with redirect_stdout(io.StringIO()) as buf:   # capturar prints
    print("hola")

cm = lock if usar_lock else nullcontext()  # un "with que no hace nada"
```

Y en el mundo `async` existen `async with` y `@asynccontextmanager` (módulo de concurrencia).

## Dónde los vas a ver

- `open()`, `tempfile.TemporaryDirectory()`, `zipfile.ZipFile()`.
- `threading.Lock()`: `with lock:` adquiere y libera.
- SQLAlchemy: `with Session(engine) as session, session.begin():`.
- pytest: `with pytest.raises(ValueError):`, `with pytest.warns(...)`, `mock.patch(...)`.
- `decimal.localcontext()`, `warnings.catch_warnings()`.

## Resumen

- `with` garantiza la limpieza aunque haya excepciones o `return`.
- Protocolo: `__enter__` devuelve lo del `as`; `__exit__` limpia y, si devuelve `True`, suprime
  la excepción.
- `@contextmanager`: antes del `yield` es el setup y después, la limpieza. **Siempre** con
  `try/finally` alrededor del `yield`.
- `contextlib`: `suppress`, `ExitStack`, `closing`, `redirect_stdout`, `nullcontext`.

## Ejercicio

Un temporizador como clase, un cambio de directorio que se restaura siempre y un context
manager que captura ciertas excepciones y las entrega en una lista.

**Para profundizar:** [contextlib](https://docs.python.org/3/library/contextlib.html),
[PEP 343 — The "with" statement](https://peps.python.org/pep-0343/), *Fluent Python*, cap. 18.
