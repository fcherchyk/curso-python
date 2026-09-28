# Desempaquetado

*Desempaquetar* (unpacking) es asignar los elementos de un iterable a varios nombres de una
sola vez. Parece un detalle de sintaxis, pero aparece en todos lados: en asignaciones, en
bucles `for`, en llamadas a funciones y al combinar colecciones. Si lo dominás, desaparecen
casi todos los `x[0]`, `x[1]` y `x[-1]` sueltos que hacen difícil leer el código.

## Asignación múltiple

```python
x, y = 3, 4                  # la derecha es una tupla (los paréntesis son opcionales)
nombre, dominio = "ana@uba.ar".split("@")
a, b = b, a                  # swap sin variable temporal
```

Funciona con **cualquier iterable**: listas, tuplas, strings, generadores, el resultado de
`dict.items()`, etc. La única regla es que la cantidad de nombres coincida con la cantidad
de elementos:

```python
a, b = [1, 2, 3]   # ValueError: too many values to unpack (expected 2)
a, b, c = [1, 2]   # ValueError: not enough values to unpack (expected 3, got 2)
```

Ese error es una ventaja: si una función "debería" devolver dos cosas y un día devuelve
tres, te enterás enseguida en lugar de arrastrar un dato incorrecto.

### ¿Cómo funciona el swap?

`a, b = b, a` primero evalúa la derecha completa y construye la tupla `(b, a)` con los valores
**viejos**. Recién después asigna. Por eso no hace falta una variable temporal.

## Desempaquetado extendido: `*resto`

Un nombre con asterisco "se lleva" todo lo que sobra, siempre como **lista**:

```python
primero, *resto = [1, 2, 3, 4]      # primero=1, resto=[2, 3, 4]
*init, ultimo = "abc"               # init=['a', 'b'], ultimo='c'
cabeza, *medio, cola = range(5)     # 0, [1, 2, 3], 4
primero, *resto = [7]               # primero=7, resto=[]
```

- Solo puede haber **un** nombre con `*` por asignación.
- Si no sobra nada, el resto es una lista vacía (no falla).
- Si faltan elementos para los nombres **sin** asterisco, sí falla: `a, *b = []` levanta
  `ValueError`.

Para descartar valores, la convención es `_`:

```python
_, dominio = email.split("@")
primero, *_, ultimo = linea.split(",")
```

## En bucles `for`

Cada elemento que produce el iterable se desempaqueta en los nombres del `for`. Es lo que
hacés sin pensar con `dict.items()`:

```python
for clave, valor in config.items():
    ...

puntos = [(0, 0), (3, 4), (1, 1)]
for x, y in puntos:
    print(x + y)

# Estructuras anidadas: los paréntesis siguen la forma de los datos
for i, (x, y) in enumerate(puntos):
    ...
```

Comparalo con la alternativa:

```python
for p in puntos:
    print(p[0] + p[1])     # ¿qué era p[0]?
```

## Desempaquetar al llamar funciones: `*` y `**`

En una **llamada**, `*` expande un iterable en argumentos posicionales y `**` expande un dict
en argumentos por nombre:

```python
def conectar(host, puerto, timeout=5): ...

args = ("db.local", 5432)
opciones = {"timeout": 10}
conectar(*args, **opciones)     # == conectar("db.local", 5432, timeout=10)

print(*["a", "b", "c"], sep="-")  # a-b-c
```

Es el mismo asterisco que en la **definición** `def f(*args, **kwargs)`, pero al revés: en
la definición *junta* argumentos y en la llamada los *expande*.

## Combinar colecciones con `*` y `**`

Dentro de literales de lista, tupla, set y dict, los asteriscos "vuelcan" el contenido:

```python
a = [1, 2]
b = (3, 4)
todo = [*a, *b, 5]             # [1, 2, 3, 4, 5]
unicos = {*a, *b}              # {1, 2, 3, 4}

defaults = {"debug": False, "puerto": 80}
config   = {"puerto": 8080}
final = {**defaults, **config, "host": "x"}
# {'debug': False, 'puerto': 8080, 'host': 'x'}  <- la derecha pisa a la izquierda
```

### El operador `|` para dicts (3.9+)

Para fusionar dicts, `|` suele leerse mejor que `{**a, **b}`:

```python
final = defaults | config          # nuevo dict, no modifica ninguno
defaults |= config                 # actualiza defaults en el lugar (como .update)
```

Las dos formas crean un dict **nuevo** y no mutan los originales, salvo `|=`, que sí
modifica el de la izquierda. Tené esa diferencia presente cuando el dict lo recibiste como
parámetro: modificarlo es un efecto secundario que quien llama no espera.

## Desempaquetar lo que devuelve una función

Devolver una tupla y desempaquetarla es la forma idiomática de retornar varios valores:

```python
def min_max(xs: list[int]) -> tuple[int, int]:
    return min(xs), max(xs)

menor, mayor = min_max([3, 1, 4])
cociente, resto = divmod(17, 5)
```

Si los valores son más de tres o tienen significado propio, conviene una `NamedTuple`: se
sigue pudiendo desempaquetar como una tupla y además cada campo tiene nombre
(`r.cociente`). Lo vemos en el módulo de modelado.

## Trampas comunes

```python
# 1. Asumir que *resto es tupla: siempre es LISTA
_, *resto = (1, 2, 3)
type(resto)                   # list

# 2. Olvidar la coma en una tupla de un elemento
(x,) = [42]                   # x = 42
x, = [42]                     # igual, más críptico

# 3. Mutar el dict que te pasaron al fusionar
def aplicar(base, extra):
    base.update(extra)        # ✗ modifica el dict de quien llama
    return base

def aplicar(base, extra):
    return base | extra       # ✓ devuelve uno nuevo
```

## Resumen

| Querés…                               | Usá                          |
|---------------------------------------|------------------------------|
| separar el primero del resto          | `primero, *resto = xs`       |
| quedarte con extremos                 | `primero, *_, ultimo = xs`   |
| intercambiar valores                  | `a, b = b, a`                |
| recorrer pares                        | `for k, v in d.items()`      |
| pasar una lista como argumentos       | `f(*lista)`                  |
| pasar un dict como keyword arguments  | `f(**opciones)`              |
| concatenar iterables                  | `[*a, *b]`                   |
| fusionar dicts sin mutar              | `a | b` o `{**a, **b}`       |

## Ejercicio

Vas a implementar cuatro funciones que se resuelven con desempaquetado y sin índices.

**Para profundizar:** [PEP 3132 — Extended Iterable Unpacking](https://peps.python.org/pep-3132/),
[PEP 448 — Additional Unpacking Generalizations](https://peps.python.org/pep-0448/),
[PEP 584 — operador `|` para dicts](https://peps.python.org/pep-0584/).
