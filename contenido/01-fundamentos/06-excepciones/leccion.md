# Excepciones

En Python, las excepciones no son algo "excepcional" que se evita a toda costa: son el
mecanismo **normal** para señalar errores, y también para cosas como el fin de un iterador
(`StopIteration`). El estilo idiomático es **EAFP**: *"Easier to Ask Forgiveness than
Permission"*, es decir, intentar la operación y manejar el error, en lugar de preguntar
antes si se puede.

## `try` / `except` / `else` / `finally`

```python
try:
    archivo = open(ruta, encoding="utf-8")
except FileNotFoundError:
    print("no existe")
except (PermissionError, IsADirectoryError) as e:
    print(f"no se puede leer: {e}")
else:
    # corre SOLO si el try no levantó nada
    with archivo:
        procesar(archivo)
finally:
    # corre SIEMPRE: haya error o no, e incluso con return o break
    print("fin")
```

- Poné en el `try` **solo** la línea que puede fallar de la forma que esperás. Lo que sigue
  va en `else`, así no atrapás por accidente errores de otras líneas.
- `finally` es para limpieza. En la práctica, casi siempre la reemplaza un `with` (context
  manager), que vemos en el módulo de funciones avanzadas.

## EAFP vs. LBYL

```python
# LBYL (Look Before You Leap): preguntar antes
if "edad" in datos and datos["edad"].isdigit():
    edad = int(datos["edad"])

# EAFP: intentar y manejar el error
try:
    edad = int(datos["edad"])
except (KeyError, ValueError):
    edad = None
```

EAFP suele ser más corto, evita repetir la lógica de validación y no tiene *race conditions*:
entre "¿existe el archivo?" y "abrilo", el archivo puede desaparecer.

## Qué atrapar (y qué no)

```python
try:
    ...
except Exception:          # ✗ casi siempre demasiado amplio
    pass                   # ✗✗ y además lo silencia
```

- Atrapá la excepción **más específica** que sepas manejar.
- **Nunca** uses `except:` a secas: atrapa también `KeyboardInterrupt` y `SystemExit`, así que
  tu programa no se puede cortar con Ctrl+C.
- Si atrapás algo amplio (por ejemplo, en el borde de un servidor), **logueá** con
  `logging.exception(...)` y volvé a levantar o devolvé un error explícito.

### La jerarquía que conviene conocer

```
BaseException
 ├── KeyboardInterrupt, SystemExit      ← no los atrapes
 └── Exception
      ├── ArithmeticError → ZeroDivisionError
      ├── LookupError → KeyError, IndexError
      ├── ValueError       (tipo correcto, valor inválido: int("x"))
      ├── TypeError        (tipo incorrecto: "a" + 1)
      ├── AttributeError, NameError
      ├── OSError → FileNotFoundError, PermissionError, TimeoutError…
      └── RuntimeError, NotImplementedError…
```

Atrapar una clase base atrapa todas sus hijas: `except LookupError` cubre `KeyError` e
`IndexError`.

## Levantar excepciones

```python
def retirar(saldo, monto):
    if monto <= 0:
        raise ValueError(f"el monto tiene que ser positivo, llegó {monto!r}")
    ...
```

Incluí en el mensaje **el valor que causó el problema**: ahorra mucho tiempo al depurar.

`raise` sin argumentos, dentro de un `except`, vuelve a levantar la excepción actual
conservando el traceback original:

```python
except ValueError:
    log.warning("dato inválido")
    raise
```

## Excepciones propias

Definí tus propias excepciones cuando quien llama necesita **distinguir** tu error para
manejarlo:

```python
class ErrorBanco(Exception):
    """Base de los errores del módulo."""

class SaldoInsuficiente(ErrorBanco):
    def __init__(self, saldo: float, monto: float) -> None:
        super().__init__(f"saldo {saldo} insuficiente para retirar {monto}")
        self.saldo = saldo
        self.monto = monto
```

Buenas prácticas:

- Heredá de `Exception` (o de una excepción estándar que tenga sentido, como `ValueError`).
- Tené una **excepción base por paquete**, así quien usa tu librería puede atrapar "cualquier
  error de este paquete" con un solo `except`.
- Nombrá las clases con sufijo `Error` o con un nombre descriptivo del problema.
- Guardá como atributos los datos útiles para manejar el error.

## Encadenar: `raise ... from ...`

Cuando traducís un error de bajo nivel a uno de tu dominio, encadená la causa:

```python
class ConfigError(Exception): ...

def leer_config(ruta):
    try:
        with open(ruta) as f:
            return f.read()
    except FileNotFoundError as e:
        raise ConfigError(f"falta el archivo de configuración: {ruta}") from e
```

El traceback muestra las dos excepciones ("The above exception was the direct cause…") y la
original queda en `error.__cause__`. Con `from None` se oculta la causa, cuando no aporta
nada.

## `assert` no es para validar

```python
assert monto > 0, "monto inválido"     # ✗ para validar entradas
```

Los `assert` **se eliminan** si Python corre con `-O`. Sirven para expresar invariantes
internas ("esto no debería pasar nunca") y en los tests, no para validar datos del usuario.

## Resumen

- EAFP: intentá y manejá el error.
- `try` chico; lo demás va en `else`; la limpieza, en `finally` o `with`.
- Atrapá lo específico. Nunca `except:` a secas; nunca silencies sin loguear.
- Excepciones propias con una base por paquete y atributos útiles.
- `raise NuevoError(...) from e` para traducir errores sin perder la causa.
- `assert` no es validación.

## Ejercicio

Cuatro funciones: conversión con EAFP, una excepción propia con datos, encadenamiento con
`from` y procesamiento por lotes que acumula errores sin cortar.

**Para profundizar:** [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html),
[Built-in exceptions (jerarquía completa)](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).
