# Funciones y firmas

Las firmas de Python son muy expresivas: parámetros con default, por posición o por nombre,
variádicos, solo-posicionales y solo-keyword. Bien usadas, hacen que las llamadas se lean
solas y que los errores de uso se detecten en el momento. Mal usadas, producen el bug más
famoso del lenguaje: el default mutable.

## Anatomía

```python
def conectar(host: str, puerto: int = 5432, *, timeout: float = 5.0) -> Conexion:
    """Abre una conexión. (docstring: la primera línea resume)"""
    ...
```

- `host` es obligatorio.
- `puerto` tiene un default.
- Todo lo que va después de `*` es **solo keyword**.
- Las anotaciones (`: str`, `-> Conexion`) son documentación verificable por herramientas,
  pero no se chequean al ejecutar.
- Una función sin `return` explícito devuelve `None`.

## Posicionales y por nombre

Al llamar, cualquier parámetro "normal" se puede pasar por posición o por nombre:

```python
conectar("db.local", 5433)
conectar(host="db.local", puerto=5433)
conectar("db.local", puerto=5433)
conectar(puerto=5433, host="db.local")   # por nombre, el orden no importa
```

Regla: los posicionales van primero. `conectar(host="x", 5433)` es un error de sintaxis.

## Solo keyword: después de `*`

```python
def exportar(datos, *, formato="csv", comprimir=False): ...

exportar(filas, formato="json", comprimir=True)   # ✓
exportar(filas, "json", True)                      # TypeError
```

Forzar el nombre es muy útil para **flags booleanos y opciones**: `exportar(filas, "json", True)`
no dice nada, mientras que `comprimir=True` sí. También te deja reordenar o agregar opciones
sin romper a quien llama.

## Solo posicional: antes de `/` (3.8+)

```python
def distancia(a, b, /): ...

distancia(p1, p2)        # ✓
distancia(a=p1, b=p2)    # TypeError
```

Sirve cuando el nombre del parámetro no aporta nada o querés poder cambiarlo sin romper la
API. Muchas funciones built-in son así: `len(obj, /)`.

La forma completa:

```python
def f(pos_only, /, normal, *, kw_only): ...
```

## Variádicos: `*args` y `**kwargs`

```python
def promedio(*numeros):          # numeros es una TUPLA
    return sum(numeros) / len(numeros)

promedio(1, 2, 3)

def etiqueta(texto, **attrs):    # attrs es un DICT
    extras = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<span {extras}>{texto}</span>"

etiqueta("hola", id="x", clase="y")
```

Los nombres `args` y `kwargs` son solo una convención; lo que importa son los asteriscos.
Los dos juntos, `def f(*args, **kwargs)`, aceptan cualquier cosa, lo que es útil en
decoradores y wrappers que reenvían argumentos a otra función.

Y al revés, al **llamar**, `*` y `**` expanden (lo viste en desempaquetado):

```python
nums = [1, 2, 3]
promedio(*nums)
opciones = {"formato": "json"}
exportar(filas, **opciones)
```

## La trampa del default mutable

**Los defaults se evalúan una sola vez**, cuando se define la función, no en cada llamada:

```python
def agregar(item, lista=[]):     # ✗ la misma lista para todas las llamadas
    lista.append(item)
    return lista

agregar(1)   # [1]
agregar(2)   # [1, 2]   ← ¡sorpresa!
```

La solución idiomática es usar `None` como centinela:

```python
def agregar(item, lista=None):
    if lista is None:
        lista = []
    lista.append(item)
    return lista
```

Lo mismo aplica a `dict`, `set`, objetos, e incluso a `datetime.now()`: el default
`creado=datetime.now()` queda congelado en el momento en que se importó el módulo.

> Si `None` es un valor válido para tu parámetro, usá un centinela propio:
> `_FALTA = object()` y `def f(x=_FALTA): if x is _FALTA: ...`.

## Devolver varios valores

Una función devuelve **un** objeto; para "varios", devolvé una tupla y desempaquetá:

```python
def min_max(xs):
    return min(xs), max(xs)

menor, mayor = min_max(datos)
```

## Docstrings

La primera línea resume la función en modo imperativo; después, si hace falta, van los
detalles. Los doctests (`>>> ...`) sirven como ejemplo y como test:

```python
def area(base: float, altura: float) -> float:
    """Área de un triángulo.

    >>> area(4, 3)
    6.0
    """
    return base * altura / 2
```

`help(area)` y los editores muestran este texto.

## Resumen

- Después de `*`, solo keyword: ideal para flags y opciones.
- Antes de `/`, solo posicional: cuando el nombre no importa.
- `*args` es una tupla; `**kwargs` es un dict.
- **Nunca** uses un mutable como default: usá `None` y crealo adentro.
- Sin `return`, la función devuelve `None`.

## Ejercicio

Cuatro funciones que practican firmas: default mutable, variádicos, parámetros
solo-posicionales y solo-keyword, y `**kwargs`.

**Para profundizar:** [Defining functions](https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions),
[PEP 570 (positional-only)](https://peps.python.org/pep-0570/), [PEP 3102 (keyword-only)](https://peps.python.org/pep-3102/).
