# Clases y el modelo de datos

Las clases de Python son simples: no hay `private`, ni sobrecarga de métodos, ni interfaces
obligatorias. Lo que las vuelve poderosas es el **modelo de datos**: un conjunto de métodos
especiales (los *dunder methods*, por *double underscore*) que permiten que tus objetos se
integren con la sintaxis del lenguaje: `len()`, `for`, `in`, `+`, `==`, `print`, `with`…

## Lo básico, rápido

```python
class Cuenta:
    comision = 0.01                      # atributo de CLASE (compartido)

    def __init__(self, titular: str, saldo: float = 0) -> None:
        self.titular = titular           # atributos de INSTANCIA
        self.saldo = saldo

    def depositar(self, monto: float) -> None:
        self.saldo += monto

c = Cuenta("Ana")
c.depositar(100)          # equivale a Cuenta.depositar(c, 100)
```

- `self` es explícito: es la instancia sobre la que se llama el método.
- `__init__` **inicializa**; no construye (eso lo hace `__new__`, que casi nunca se toca).
- Los atributos de clase se comparten entre instancias. Cuidado con los **mutables** ahí: una
  lista definida en la clase la comparten **todas** las instancias.

### Privacidad por convención

```python
self.saldo        # público
self._interno     # "privado" por convención: no lo toques desde afuera
self.__secreto    # name mangling: se renombra a _Cuenta__secreto (evita choques en herencia)
```

No hay privacidad real, y está bien: *"we are all consenting adults"*. Usá `_nombre` para
señalar lo interno.

## `__repr__` y `__str__`

```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Punto({self.x!r}, {self.y!r})"     # para devs: sin ambigüedad

    def __str__(self):
        return f"({self.x}, {self.y})"               # para humanos
```

- `repr(obj)` se usa en el REPL, en el debugger, en los logs y dentro de contenedores (`print([p])`
  muestra el `repr` de cada elemento). Idealmente es una expresión que recrea el objeto.
- `str(obj)` se usa en `print` y en f-strings. Si no lo definís, usa `__repr__`.

**Implementá siempre `__repr__`.** El default, `<Punto object at 0x10a3…>`, no ayuda a
depurar.

## Igualdad y hash

Por defecto, `==` compara **identidad**: dos objetos distintos nunca son iguales. Para
comparar por valor:

```python
def __eq__(self, otro):
    if not isinstance(otro, Punto):
        return NotImplemented            # ¡no False! deja que Python pruebe del otro lado
    return (self.x, self.y) == (otro.x, otro.y)

def __hash__(self):
    return hash((self.x, self.y))
```

Dos reglas:

1. Si dos objetos son `==`, tienen que tener el mismo `hash`. Por eso, **al definir
   `__eq__`, Python pone `__hash__ = None`** y los objetos dejan de poder usarse en sets o
   como claves. Si querés que sean hashables, definí `__hash__` a partir de los mismos campos.
2. Solo hasheá objetos cuyo valor **no cambie**. Si mutás un objeto que está adentro de un
   set, el set se rompe.

Devolver `NotImplemented` (una constante especial, no la excepción) le dice a Python "no sé
comparar con eso". Python prueba entonces con el método del otro operando y, si ninguno
puede, usa la identidad (para `==`) o levanta `TypeError` (para `<` y demás).

## Operadores

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, otro):               # v + w
        if not isinstance(otro, Vector):
            return NotImplemented
        return Vector(self.x + otro.x, self.y + otro.y)

    def __mul__(self, k):                  # v * 3
        if not isinstance(k, (int, float)):
            return NotImplemented
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                     # 3 * v  (el "r" es el operando derecho)

    def __abs__(self):                     # abs(v)
        return math.hypot(self.x, self.y)

    def __bool__(self):                    # if v:
        return bool(abs(self))
```

Para `3 * v`, Python primero prueba `int.__mul__(3, v)`, que devuelve `NotImplemented`, y
después `v.__rmul__(3)`. Por eso importa devolver `NotImplemented` y no levantar una
excepción.

Los operadores deben devolver un objeto **nuevo**. Los *in-place* (`__iadd__` para `+=`)
pueden mutar, pero solo en tipos mutables.

## Comportarse como una colección

| Querés…                   | Implementá                          |
|---------------------------|-------------------------------------|
| `len(x)`                  | `__len__`                           |
| `if x:` (vacío = falso)   | `__len__` o `__bool__`              |
| `for i in x`              | `__iter__`                          |
| `item in x`               | `__contains__` (si no, usa `__iter__`) |
| `x[i]`, `x[a:b]`          | `__getitem__`                       |
| `x[i] = v`, `del x[i]`    | `__setitem__`, `__delitem__`        |
| `reversed(x)`             | `__reversed__` (o `__len__` + `__getitem__`) |

Casi siempre alcanza con **delegar** en una colección interna:

```python
class Mazo:
    def __init__(self, cartas):
        self._cartas = list(cartas)

    def __len__(self):
        return len(self._cartas)

    def __getitem__(self, i):              # habilita x[0], slicing, e incluso for e in
        return self._cartas[i]
```

Con esos dos métodos, `random.choice(mazo)`, `mazo[:3]`, `for c in mazo`, `c in mazo` y
`reversed(mazo)` funcionan solos.

## Herencia: lo justo

```python
class CuentaPremium(Cuenta):
    comision = 0.0

    def __init__(self, titular, saldo=0, limite=1000):
        super().__init__(titular, saldo)   # siempre super(), no Cuenta.__init__(self, ...)
        self.limite = limite
```

Preferí **composición** (un objeto que *tiene* otro) antes que herencia (un objeto que *es*
otro), salvo que realmente haya una relación "es un". Las jerarquías profundas son difíciles
de seguir.

## Resumen

- `self` explícito, `__init__` inicializa, `_nombre` es privado por convención.
- Siempre `__repr__`; `__str__` si hace falta una versión para humanos.
- `__eq__` desactiva el hash: si necesitás hash, definilo con los mismos campos.
- Los operadores devuelven `NotImplemented` ante tipos que no manejan; `__rmul__` y
  compañía cubren el operando derecho.
- `__len__` + `__getitem__` (o `__iter__`) hacen que tu clase se comporte como colección.
- En el próximo capítulo de dataclasses vas a ver cómo **generar** casi todo esto.

## Ejercicio

Un `Vector` con operadores, igualdad y hash, y un `Carrito` que se comporta como colección.

**Para profundizar:** [Data model](https://docs.python.org/3/reference/datamodel.html),
*Fluent Python* (2.ª ed.), cap. 1 y 16.
