# Decoradores con parámetros

`@lru_cache(maxsize=128)`, `@app.get("/usuarios")` o `@pytest.mark.parametrize(...)` son
decoradores que **reciben argumentos**. El truco es que no son decoradores: son **fábricas
que devuelven un decorador**. Eso agrega un nivel más de funciones anidadas, y vale la pena
entender por qué.

## Por qué hace falta otro nivel

```python
@repetir(3)
def saludar(): ...
```

equivale a:

```python
decorador = repetir(3)          # 1. se llama a la fábrica con los parámetros
saludar = decorador(saludar)    # 2. el resultado decora la función
```

Entonces `repetir(3)` tiene que devolver algo que reciba una función, es decir, un
decorador. Quedan tres niveles:

```python
import functools
import random

def repetir(n):                         # nivel 1: fábrica (recibe los parámetros)
    def decorador(func):                # nivel 2: decorador (recibe la función)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):   # nivel 3: wrapper (recibe los argumentos de la llamada)
            return [func(*args, **kwargs) for _ in range(n)]
        return wrapper
    return decorador

@repetir(3)
def tirar_dado():
    return random.randint(1, 6)

tirar_dado()     # [4, 1, 6]
```

Cada nivel es una closure del anterior: `wrapper` ve tanto `func` como `n`.

## Un ejemplo realista: reintentos

```python
import time

def reintentar(veces, excepciones=(Exception,), espera=0.0):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(1, veces + 1):
                try:
                    return func(*args, **kwargs)
                except excepciones:
                    if intento == veces:
                        raise                  # se agotaron: re-levantar la última
                    time.sleep(espera)
        return wrapper
    return decorador

@reintentar(3, excepciones=(ConnectionError, TimeoutError), espera=0.5)
def consultar_api(): ...
```

Detalles de diseño que conviene imitar:

- Atrapar **solo** las excepciones indicadas: un `KeyError` por un bug no se tiene que
  reintentar.
- Re-levantar la **última** excepción con `raise` cuando se agotan los intentos.
- En producción se agrega *backoff* exponencial y *jitter*, o se usa una librería como
  `tenacity`.

## Errores comunes

```python
@repetir          # ✗ sin paréntesis: repetir recibe la FUNCIÓN como `n`
def f(): ...

@reintentar()     # ✗ con paréntesis pero sin el argumento obligatorio → TypeError
def g(): ...
```

Si tu decorador tiene parámetros, **siempre** se usa con paréntesis, aunque todos tengan
default: `@lru_cache()` (o `@lru_cache`, que se permite desde 3.8 por el truco que sigue).

## Decoradores con paréntesis opcionales

Algunos decoradores funcionan de las dos formas, `@deco` y `@deco(opcion=...)`. El truco es
mirar si el primer argumento es la función:

```python
import warnings

def deprecado(func=None, *, reemplazo=None):
    def decorador(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            msg = f"{f.__name__} está deprecada"
            if reemplazo:
                msg += f"; usá {reemplazo}"
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return f(*args, **kwargs)
        return wrapper

    if func is not None:        # se usó como @deprecado (sin paréntesis)
        return decorador(func)
    return decorador            # se usó como @deprecado(reemplazo="...")
```

El `*` hace que las opciones sean **solo keyword**, así no hay ambigüedad entre "me pasaron
una función" y "me pasaron una opción posicional". `stacklevel=2` hace que la advertencia
apunte a quien llamó a la función deprecada y no al wrapper.

## Alternativa: una clase como decorador

Cuando el decorador tiene mucho estado o configuración, se puede escribir como clase:

```python
class Limitador:
    def __init__(self, por_segundo):
        self.por_segundo = por_segundo

    def __call__(self, func):              # la instancia actúa como decorador
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ...
        return wrapper

@Limitador(por_segundo=5)
def enviar(): ...
```

## Resumen

- `@fabrica(args)` → `fabrica(args)` devuelve el decorador → el decorador devuelve el wrapper.
- Son tres niveles de funciones; cada uno ve las variables del anterior.
- Siempre `functools.wraps` en el wrapper.
- Con parámetros, se usa con paréntesis. Para que los paréntesis sean opcionales:
  `func=None` y opciones solo keyword.
- Si hay mucho estado, una clase con `__call__`.

## Ejercicio

Cuatro decoradores con parámetros: repetir, reintentar, acotar el resultado y deprecar con
paréntesis opcionales.

**Para profundizar:** *Python Cookbook* (Beazley & Jones), cap. 9,
[warnings](https://docs.python.org/3/library/warnings.html), [tenacity](https://tenacity.readthedocs.io/).
