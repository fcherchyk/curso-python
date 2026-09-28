# Funciones como objetos

En Python las funciones son **objetos de primera clase**: se pueden asignar a variables,
guardar en estructuras, pasar como argumento y devolver desde otras funciones. Casi todo lo
que viene en este módulo (closures, decoradores y los *callbacks* de los frameworks) se apoya
en esta idea.

## Una función es un valor más

```python
def saludar(nombre):
    return f"hola {nombre}"

f = saludar              # sin paréntesis: la función, no su resultado
f("ana")                 # 'hola ana'
f.__name__               # 'saludar'
type(f)                  # <class 'function'>

acciones = [str.upper, str.lower, str.title]
[accion("hOLA") for accion in acciones]    # ['HOLA', 'hola', 'Hola']
```

Un error típico es pasar `func()` (su resultado) cuando se esperaba `func` (la función).

## Funciones que reciben funciones

Ya las usaste: `sorted(key=...)`, `max(key=...)`, `map`, `filter`. El patrón general es
**separar el "qué" del "cómo"**:

```python
def aplicar_a_todos(func, xs):
    return [func(x) for x in xs]

aplicar_a_todos(len, ["a", "bcd"])      # [1, 3]
```

En Python moderno, `map` y `filter` suelen reemplazarse por comprehensions, que se leen
mejor. Donde las funciones como argumento brillan es en `key=`, en los callbacks y en la
inyección de comportamiento: "cómo reintentar", "cómo formatear", "qué hacer al terminar".

## Despacho con dicts: reemplazar cadenas de `if`

```python
import operator

OPERACIONES = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

def calcular(op, a, b):
    try:
        return OPERACIONES[op](a, b)
    except KeyError:
        raise ValueError(f"operación desconocida: {op!r}") from None
```

Agregar una operación es agregar una entrada, sin tocar la lógica. El módulo `operator` trae
versiones en forma de función de todos los operadores (`add`, `mul`, `itemgetter`,
`attrgetter`, `methodcaller`…).

## `lambda`: funciones anónimas de una expresión

```python
sorted(personas, key=lambda p: p.edad)
```

Una `lambda` es solo una forma corta de escribir una función de **una expresión**. Úsala
para argumentos cortos, como en `key=`. Si necesitás asignarla a un nombre
(`doble = lambda x: x * 2`), escribí un `def`: tiene nombre en los tracebacks, admite
docstring y ruff te lo va a marcar (regla E731).

## Funciones que devuelven funciones

```python
def crear_multiplicador(k):
    def multiplicar(x):
        return x * k
    return multiplicar

doble = crear_multiplicador(2)
doble(21)    # 42
```

`multiplicar` "recuerda" el `k` con que se creó: es una **closure**, el tema del próximo
capítulo.

## `functools.partial`: fijar argumentos

```python
from functools import partial

int_binario = partial(int, base=2)
int_binario("1010")                 # 10

log_error = partial(print, "[ERROR]", sep=" ")
log_error("falló la conexión")      # [ERROR] falló la conexión
```

`partial` crea una función nueva con algunos argumentos ya puestos. Es muy útil para adaptar
una función a la firma que espera otro código (un callback sin argumentos, un `key=` de un
solo argumento, etc.).

## Componer funciones

```python
from functools import reduce

def componer(*funcs):
    """componer(f, g, h)(x) == f(g(h(x)))"""
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)

limpiar = componer(str.title, str.strip)
limpiar("  ana pérez ")    # 'Ana Pérez'
```

`reduce` combina los elementos de a pares de izquierda a derecha. Es poco común en código de
aplicación (un `for` suele leerse mejor), pero aparece en utilidades como esta.

## Los *callables*: no solo funciones

Cualquier objeto con `__call__` se puede "llamar": las clases (llamarlas crea instancias),
los métodos, los objetos `partial` y las instancias de clases propias que definan `__call__`.
`callable(obj)` pregunta si algo se puede llamar.

```python
class Contador:
    def __init__(self):
        self.n = 0
    def __call__(self):
        self.n += 1
        return self.n

c = Contador()
c(), c()     # (1, 2)
```

## Resumen

- Las funciones son valores: pasalas sin paréntesis.
- Dict de funciones en lugar de `if/elif` para despachar según un valor.
- `lambda` solo para expresiones cortas pasadas como argumento.
- `functools.partial` fija argumentos; `operator` da los operadores como funciones.
- Cualquier objeto con `__call__` es un *callable*.

## Ejercicio

Composición de funciones, aplicación repetida, despacho con un dict de operadores y
`partial`.

**Para profundizar:** [functools](https://docs.python.org/3/library/functools.html),
[operator](https://docs.python.org/3/library/operator.html), *Fluent Python*, cap. 7.
