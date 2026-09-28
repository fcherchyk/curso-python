# Nombres, objetos y mutabilidad

Si venís de otro lenguaje, lo más importante de Python no es la sintaxis sino su **modelo de
datos**: las variables no son cajas que guardan valores, sino **nombres que apuntan a
objetos**. Casi todos los bugs "raros" de principiante (listas que cambian solas, defaults
compartidos, copias que no son copias) salen de no tener clara esta idea.

## Todo es un objeto, las variables son etiquetas

```python
a = [1, 2, 3]
b = a            # b NO es una copia: es otro nombre para el MISMO objeto
b.append(4)
print(a)         # [1, 2, 3, 4]
```

Cada objeto tiene:

- **identidad**: `id(obj)`, que no cambia durante su vida;
- **tipo**: `type(obj)`, que tampoco cambia;
- **valor**: que puede cambiar o no, según el tipo sea mutable o inmutable.

La asignación `=` **nunca copia**: solo hace que un nombre apunte a un objeto. Lo mismo pasa
al pasar argumentos a una función: la función recibe una referencia al mismo objeto (lo que a
veces se llama *pass by object reference* o *call by sharing*).

## `==` vs. `is`

```python
a = [1, 2]
b = [1, 2]
a == b      # True:  mismo VALOR
a is b      # False: objetos distintos
```

- `==` compara valores (llama a `__eq__`).
- `is` compara identidad (¿es el mismo objeto?).

Usá `is` **solo** con singletons: `x is None`, `x is True`/`False` (raro) o centinelas propios.
Para todo lo demás, `==`. Que `a is b` dé `True` con enteros chicos o strings cortos es un
detalle de implementación (CPython reutiliza esos objetos); no dependas de eso.

## Mutables e inmutables

| Inmutables                                   | Mutables                          |
|----------------------------------------------|-----------------------------------|
| `int`, `float`, `bool`, `complex`, `Decimal` | `list`                            |
| `str`, `bytes`                               | `dict`                            |
| `tuple`, `frozenset`                         | `set`, `bytearray`                |
| `None`                                       | la mayoría de las clases propias  |

Con un inmutable, cualquier "modificación" crea un objeto nuevo:

```python
s = "hola"
t = s
s += "!"        # crea un str nuevo y reasigna s
print(t)        # "hola"  <- t sigue apuntando al original
```

Con un mutable, `+=` modifica **en el lugar**:

```python
xs = [1]
ys = xs
xs += [2]       # list.__iadd__ extiende el mismo objeto
print(ys)       # [1, 2]
```

> Una tupla es inmutable, pero si **contiene** un objeto mutable, ese objeto sí puede cambiar:
> `t = ([1], 2); t[0].append(9)` funciona. La tupla sigue apuntando a la misma lista.

## Consecuencia 1: funciones que mutan sus argumentos

```python
def agregar_iva(precios):
    for i, p in enumerate(precios):
        precios[i] = p * 1.21      # ✗ modifica la lista de quien llama
    return precios
```

Quien llama pierde sus datos originales sin enterarse. La convención en Python es:

- si la función **muta**, que devuelva `None` (como `list.sort()` o `dict.update()`);
- si **no muta**, que devuelva un objeto nuevo (como `sorted()`).

```python
def con_iva(precios):
    return [p * 1.21 for p in precios]   # ✓ no toca el original
```

## Consecuencia 2: copias superficiales y profundas

```python
import copy

original = [[1, 2], [3, 4]]

sup = original.copy()          # también: list(original), original[:]
sup[0].append(99)
print(original)                # [[1, 2, 99], [3, 4]]  <- ¡cambió!

prof = copy.deepcopy(original)
prof[0].append(100)
print(original)                # no cambia
```

Una copia **superficial** crea un contenedor nuevo con las *mismas* referencias adentro. Una
**profunda** copia recursivamente todo. Para una lista de listas alcanza con
`[fila.copy() for fila in m]`; `deepcopy` es el martillo general (más lento).

## Consecuencia 3: `[[0] * 3] * 3`

```python
tablero = [[0] * 3] * 3
tablero[0][0] = 1
print(tablero)   # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```

`* 3` repite **la referencia** a la misma lista interna. La forma correcta es
`[[0] * 3 for _ in range(3)]`: la comprehension crea una lista nueva en cada vuelta.

## Números: lo que conviene recordar

```python
7 / 2       # 3.5   división real, siempre float
7 // 2      # 3     división entera (floor)
-7 // 2     # -4    ¡redondea hacia -infinito, no hacia 0!
-7 % 2      # 1     el resto tiene el signo del divisor
divmod(-7, 2)       # (-4, 1)
2 ** 100    # los int no tienen límite de tamaño
0.1 + 0.2   # 0.30000000000000004  <- float binario (IEEE 754)
```

Para dinero o cualquier cálculo decimal exacto, usá `decimal.Decimal` **construido desde
string**:

```python
from decimal import Decimal
Decimal("0.1") + Decimal("0.2")    # Decimal('0.3')
Decimal(0.1)                       # Decimal('0.1000000000000000055511151231257827...')  ✗
```

Para comparar floats, `math.isclose(a, b)` en lugar de `==`.

## Verdad y falsedad (*truthiness*)

Cualquier objeto se puede evaluar como booleano. Son **falsos**: `None`, `False`, `0`, `0.0`,
`""`, `[]`, `{}`, `set()`, `()` y cualquier objeto cuyo `__bool__` devuelva `False` o cuyo
`__len__` devuelva 0. Todo lo demás es verdadero.

```python
if not items:            # ✓ idiomático para "vacío"
if len(items) == 0:      # ✗ ruido

nombre = entrada or "anónimo"   # default si entrada es falsy
```

Cuidado: `x or default` también reemplaza un `0` o un `""` válidos. Si lo que querés es
"si es `None`", escribilo: `x if x is not None else default`.

## Tipado dinámico pero fuerte

Los nombres no tienen tipo; los objetos sí. Y Python **no convierte implícitamente** entre
tipos incompatibles:

```python
"3" + 4          # TypeError (en JavaScript sería "34")
int("3") + 4     # 7
```

Los *type hints* (`def f(x: int) -> str`) no se verifican al ejecutar: los usan las
herramientas como mypy y los editores. Los vemos en el módulo de herramientas.

## Resumen

- `=` nunca copia; los argumentos se pasan como referencias al mismo objeto.
- `is` para `None` y centinelas; `==` para todo lo demás.
- Los mutables modificados "a distancia" son la fuente número uno de bugs: no mutes lo que
  te pasan, salvo que la función exista para eso.
- `list.copy()` es superficial; `copy.deepcopy()` es profunda.
- `//` y `%` redondean hacia -infinito; para dinero, `Decimal("...")`.

## Ejercicio

Cuatro funciones que te obligan a respetar el modelo de objetos: no mutar, copiar bien,
sumar dinero sin errores de float y entender la división entera.

**Para profundizar:** [Data model — Objects, values and types](https://docs.python.org/3/reference/datamodel.html#objects-values-and-types),
*Fluent Python* (2.ª ed.), cap. 6 ("Object References, Mutability, and Recycling").
