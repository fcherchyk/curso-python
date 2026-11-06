# Interfaces: Protocol vs. ABC

Python no tiene la palabra clave `interface`. Tiene **duck typing** ("si camina como pato y
hace cuac, es un pato") y dos herramientas para formalizarlo: las **clases base abstractas**
(ABC), que exigen herencia, y los **Protocol**, que describen una forma sin exigir nada. Saber
cuál usar en cada caso es parte de diseñar APIs pythónicas.

## Duck typing: el punto de partida

```python
def area_total(figuras):
    return sum(f.area() for f in figuras)
```

A esta función no le importa **qué es** cada figura, sino **qué sabe hacer**: tener un método
`area()`. Cualquier objeto que lo tenga sirve. Es flexible, pero la "interfaz" solo está en
tu cabeza. Si alguien pasa un objeto sin `area`, se entera al ejecutar.

## ABC: interfaz nominal, con herencia

```python
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar(self, destino: str, mensaje: str) -> bool:
        """Envía un mensaje. Devuelve True si salió bien."""

    def enviar_a_todos(self, destinos: list[str], mensaje: str) -> int:
        # método concreto que usa al abstracto (patrón "template method")
        return sum(self.enviar(d, mensaje) for d in destinos)

class NotificadorEmail(Notificador):
    def enviar(self, destino, mensaje):
        ...
        return True
```

Qué te da una ABC:

- **No se puede instanciar** la base: `Notificador()` levanta `TypeError`.
- **No se puede instanciar una subclase incompleta**: si `NotificadorEmail` no implementa
  `enviar`, falla al crear la instancia (no más tarde, al llamar al método).
- Puede traer **métodos concretos** compartidos, como `enviar_a_todos`.
- `isinstance(x, Notificador)` funciona.

El costo es que hay que **heredar**. No sirve para clases que no controlás (de otra librería).

## Protocol: interfaz estructural, sin herencia

```python
from typing import Protocol

class TieneArea(Protocol):
    def area(self) -> float: ...

class Circulo:                     # no hereda de TieneArea
    def __init__(self, r): self.r = r
    def area(self) -> float: return math.pi * self.r ** 2

def area_total(figuras: Iterable[TieneArea]) -> float:
    return sum(f.area() for f in figuras)
```

Un `Protocol` describe **la forma** que tiene que tener un objeto. Cualquier clase que tenga
esos métodos, con esas firmas, **cumple automáticamente**, sin heredar ni registrarse. Es duck
typing, pero **verificado por el type checker** (mypy o pyright): si pasás algo sin `area()`,
lo marca antes de ejecutar.

Por defecto, un Protocol **no existe al ejecutar**: `isinstance(x, TieneArea)` levanta
`TypeError`. Si necesitás chequearlo en runtime, decoralo con `@runtime_checkable`:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Cerrable(Protocol):
    def close(self) -> None: ...

isinstance(open("x.txt"), Cerrable)     # True
```

Ojo: `runtime_checkable` solo verifica que **existan** los métodos, no sus firmas ni sus tipos.

## ¿Cuál elegir?

| Situación                                                      | Usá          |
|----------------------------------------------------------------|--------------|
| Tipar un parámetro: "necesito algo que tenga `.read()`"        | **Protocol** |
| Las implementaciones son de terceros o no las controlás        | **Protocol** |
| Querés compartir código entre implementaciones (template method) | **ABC**    |
| Querés que falle al instanciar una implementación incompleta   | **ABC**      |
| Es una jerarquía propia con una relación "es un" clara         | **ABC**      |

En la práctica moderna, **Protocol es la opción por defecto para tipar dependencias**: hace
que el código sea fácil de testear (cualquier *fake* que tenga los métodos sirve) y no acopla
a quien implementa con tu jerarquía de clases.

## Las ABCs de la stdlib: `collections.abc`

La stdlib define ABCs para los protocolos del lenguaje, y conviene usarlas en las anotaciones
de tipo:

```python
from collections.abc import Iterable, Iterator, Sequence, Mapping, Callable

def procesar(items: Iterable[str]) -> list[str]: ...     # acepta list, set, generador…
def buscar(tabla: Mapping[str, int], k: str) -> int: ...   # acepta dict y más
```

Son "mixins" inteligentes: si heredás de `collections.abc.Sequence` e implementás `__getitem__`
y `__len__`, te regalan `__contains__`, `__iter__`, `__reversed__`, `index` y `count`.

Principio útil: **aceptá lo más abstracto** (`Iterable`, `Mapping`) y **devolvé lo más
concreto** (`list`, `dict`).

## Resumen

- Duck typing: importa lo que el objeto sabe hacer, no qué es.
- ABC: herencia obligatoria, falla al instanciar si falta algo y permite compartir código.
- Protocol: forma estructural sin herencia, verificada por el type checker; en runtime, solo
  con `@runtime_checkable`.
- Para tipar dependencias, Protocol por defecto.
- En las anotaciones, `collections.abc` (`Iterable`, `Mapping`…).

## Ejercicio

Un Protocol para figuras, una ABC con un método template y un Protocol `runtime_checkable`
para cerrar recursos.

**Para profundizar:** [PEP 544 — Protocols](https://peps.python.org/pep-0544/),
[abc](https://docs.python.org/3/library/abc.html), *Fluent Python*, cap. 13.
