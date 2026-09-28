# Dataclasses

En el capítulo anterior escribiste `__init__`, `__repr__`, `__eq__` y `__hash__` a mano.
`@dataclass` los **genera** a partir de las anotaciones de la clase. Es la forma idiomática
de definir objetos que son principalmente datos: DTOs, registros, configuraciones,
entidades de dominio.

## Lo mínimo

```python
from dataclasses import dataclass

@dataclass
class Producto:
    sku: str
    nombre: str
    precio: float = 0.0          # con default

p = Producto("A1", "Yerba", 3500)
p                                # Producto(sku='A1', nombre='Yerba', precio=3500)
p == Producto("A1", "Yerba", 3500)   # True: compara campo a campo
```

Se generan `__init__`, `__repr__` y `__eq__`. Los **campos** son los atributos de clase
**anotados**. Los atributos sin anotación no son campos.

Regla: los campos con default van **después** de los que no tienen default, igual que en
cualquier firma de función. Si no, `TypeError: non-default argument follows default argument`.

## Defaults mutables: `field(default_factory=...)`

```python
from dataclasses import field

@dataclass
class Carrito:
    items: list[str] = []                         # ValueError: mutable default
    items: list[str] = field(default_factory=list)   # ✓ una lista nueva por instancia
```

Es la misma trampa del default mutable de las funciones, pero `dataclass` **la detecta** y te
frena. `default_factory` recibe una función sin argumentos (`list`, `dict`, `set` o
`lambda: {"a": 1}`) que se llama para cada instancia nueva.

Otras opciones de `field`:

```python
id: int = field(default=0, repr=False)         # no aparece en el repr
cache: dict = field(default_factory=dict, compare=False)   # no participa de ==
_interno: int = field(init=False, default=0)    # no está en el __init__
```

## Opciones del decorador

```python
@dataclass(frozen=True, order=True, slots=True, kw_only=True)
```

| Opción          | Qué hace                                                            |
|-----------------|---------------------------------------------------------------------|
| `frozen=True`   | inmutable (asignar levanta `FrozenInstanceError`) **y hashable**    |
| `order=True`    | genera `<`, `<=`, `>`, `>=` comparando los campos como una tupla, en orden |
| `slots=True`    | (3.10) usa `__slots__`: menos memoria, acceso más rápido, no se pueden agregar atributos |
| `kw_only=True`  | (3.10) todos los campos son solo keyword en el `__init__`           |
| `eq=False`      | no genera `__eq__` (igualdad por identidad)                          |

`frozen=True` es una muy buena opción por defecto para objetos de valor (puntos, dinero,
versiones, coordenadas): son más fáciles de razonar, se pueden compartir sin miedo y se
pueden usar en sets y como claves de dict.

`order=True` compara los campos **en el orden en que están declarados**. Por eso, el orden
de los campos pasa a ser parte del diseño:

```python
@dataclass(frozen=True, order=True)
class Version:
    mayor: int
    menor: int = 0
    parche: int = 0

sorted([Version(1, 10), Version(1, 2)])     # [Version(1, 2, 0), Version(1, 10, 0)]
```

## Validar: `__post_init__`

El `__init__` generado llama a `__post_init__` al final, si existe. Es el lugar para validar
o calcular campos derivados:

```python
@dataclass
class Rango:
    desde: int
    hasta: int

    def __post_init__(self) -> None:
        if self.desde > self.hasta:
            raise ValueError(f"rango inválido: {self.desde} > {self.hasta}")
```

En un dataclass `frozen`, para asignar un campo derivado dentro de `__post_init__` hay que
usar `object.__setattr__(self, "campo", valor)`, porque la asignación normal está bloqueada.

## "Modificar" un frozen: `replace`

```python
from dataclasses import replace

v = Version(1, 2, 3)
v2 = replace(v, parche=4)       # copia con un campo cambiado; v no se toca
```

Así se trabaja con objetos inmutables: en lugar de mutar, se crean versiones nuevas.

## Utilidades

```python
from dataclasses import asdict, astuple, fields

asdict(p)       # {'sku': 'A1', 'nombre': 'Yerba', 'precio': 3500}  (recursivo)
astuple(p)      # ('A1', 'Yerba', 3500)
[f.name for f in fields(p)]
```

`asdict` es útil para serializar a JSON: `json.dumps(asdict(p))`.

## Métodos y properties siguen funcionando

Una dataclass es una clase normal. Podés agregarle métodos, properties, classmethods y
dunders propios. Si definís un método que el decorador también generaría (por ejemplo,
`__repr__`), **se respeta el tuyo**.

```python
@dataclass(frozen=True, order=True)
class Version:
    mayor: int
    menor: int = 0
    parche: int = 0

    @classmethod
    def desde_str(cls, texto: str) -> "Version":
        return cls(*(int(p) for p in texto.split(".")))

    def __str__(self) -> str:
        return f"{self.mayor}.{self.menor}.{self.parche}"
```

## ¿Dataclass, NamedTuple, dict o Pydantic?

| Opción             | Cuándo                                                              |
|--------------------|---------------------------------------------------------------------|
| `dict`             | datos sueltos y temporales, o JSON que solo pasa de largo            |
| `typing.NamedTuple`| registros inmutables chicos que además querés desempaquetar o indexar |
| `@dataclass`       | objetos de tu dominio, internos: el caso por defecto                |
| Pydantic `BaseModel` | datos que vienen **de afuera** (JSON de una API, config) y hay que **validar y convertir** |

Las dataclasses **no validan tipos**: `Producto("A1", "Yerba", "caro")` se crea sin quejarse.
Las anotaciones son para las herramientas. Si necesitás validación real al recibir datos
externos, eso es Pydantic, que vemos en el módulo de frameworks.

## Resumen

- `@dataclass` genera `__init__`, `__repr__` y `__eq__` a partir de las anotaciones.
- Para defaults mutables, `field(default_factory=list)`.
- `frozen=True` da objetos inmutables y hashables; `order=True` compara por los campos en orden.
- `__post_init__` para validar; `replace` para "modificar" un frozen; `asdict` para serializar.
- No valida tipos: para datos externos, Pydantic.

## Ejercicio

Un `Punto` frozen, una `Version` comparable y un `Pedido` con default mutable, validación y
operaciones inmutables.

**Para profundizar:** [dataclasses](https://docs.python.org/3/library/dataclasses.html),
[PEP 557](https://peps.python.org/pep-0557/), *Fluent Python*, cap. 5.
