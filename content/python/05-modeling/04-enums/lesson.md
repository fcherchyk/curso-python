# Enums

Un **enum** es un conjunto cerrado de valores con nombre: estados de un pedido, niveles de
log, métodos HTTP, días de la semana. Usarlos en lugar de strings o números sueltos
("mágicos") hace que el código se autodocumente, que los errores de tipeo fallen al
instante y que el editor pueda autocompletar.

## El problema de los strings mágicos

```python
if pedido.estado == "enviado": ...
if pedido.estado == "envíado": ...      # typo: nunca es True y nadie se entera
```

Con un enum:

```python
from enum import Enum

class Estado(Enum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"

if pedido.estado is Estado.ENVIADO: ...
if pedido.estado is Estado.ENVIADOO: ...  # AttributeError inmediato
```

## Lo básico

```python
Estado.ENVIADO              # <Estado.ENVIADO: 'enviado'>
Estado.ENVIADO.name         # 'ENVIADO'
Estado.ENVIADO.value        # 'enviado'
Estado("enviado")           # lookup por VALOR → Estado.ENVIADO
Estado["ENVIADO"]           # lookup por NOMBRE
Estado("perdido")           # ValueError
list(Estado)                # los miembros, en orden de definición
len(Estado)                 # 3
Estado.ENVIADO in Estado    # True
```

Los miembros son **singletons**: se comparan con `is` (aunque `==` también funciona).

## `auto()`: cuando el valor no importa

```python
from enum import Enum, auto

class Color(Enum):
    ROJO = auto()      # 1
    VERDE = auto()     # 2
```

## `StrEnum` e `IntEnum`: enums que además son str o int

Un `Enum` común **no** es igual a su valor: `Estado.ENVIADO == "enviado"` da `False`. Eso es
molesto en los bordes del programa (JSON, base de datos, parámetros de una URL). `StrEnum`
(3.11+) e `IntEnum` hacen que los miembros **sean** strings o enteros:

```python
from enum import StrEnum, IntEnum, auto

class Metodo(StrEnum):
    GET = auto()          # con StrEnum, auto() da el nombre en minúscula: "get"
    POST = auto()

Metodo.GET == "get"       # True
f"{Metodo.GET}"           # 'get'
json.dumps({"m": Metodo.GET})   # '{"m": "get"}'  ← serializa directo

class Prioridad(IntEnum):
    BAJA = 1
    MEDIA = 2
    ALTA = 3

Prioridad.ALTA > Prioridad.BAJA     # True: se comparan como ints
sorted([Prioridad.ALTA, Prioridad.BAJA])
```

Regla práctica: **`StrEnum` para casi todo lo que viaja a JSON o a la base**; `IntEnum` cuando
el orden numérico tiene sentido (prioridades, niveles); `Enum` puro cuando no querés que se
mezcle con strings.

FastAPI, Pydantic y SQLAlchemy entienden enums: validan que el valor recibido sea uno de los
miembros y lo documentan en OpenAPI.

## Los enums son clases: pueden tener métodos

```python
class Estado(StrEnum):
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"

    @property
    def es_final(self) -> bool:
        return self is Estado.ENTREGADO

    def siguiente(self) -> "Estado":
        miembros = list(Estado)
        i = miembros.index(self)
        if i == len(miembros) - 1:
            raise ValueError("ya está en el estado final")
        return miembros[i + 1]
```

Así la lógica de "máquina de estados" vive junto a los estados.

## `Flag`: combinaciones

Para permisos u opciones combinables, `Flag` permite operar con bits:

```python
from enum import Flag, auto

class Permiso(Flag):
    LEER = auto()        # 1
    ESCRIBIR = auto()    # 2
    BORRAR = auto()      # 4
    TODOS = LEER | ESCRIBIR | BORRAR

p = Permiso.LEER | Permiso.ESCRIBIR
Permiso.ESCRIBIR in p       # True
Permiso.BORRAR in p         # False
p & Permiso.BORRAR          # Permiso(0): vacío, falsy
```

## Enums y `match`

Los enums combinan muy bien con `match` (módulo 06). Ojo con usar el nombre completo con
punto:

```python
match estado:
    case Estado.PENDIENTE:     # ✓ compara con el miembro
        ...
    case PENDIENTE:            # ✗ ¡captura cualquier valor en una variable llamada PENDIENTE!
        ...
```

## Resumen

- Enum en lugar de strings o números mágicos: errores tempranos y código autodocumentado.
- `.name`, `.value`, `Clase(valor)`, `Clase["NOMBRE"]`, `list(Clase)`.
- `StrEnum` para valores que viajan a JSON o a la base; `IntEnum` si el orden numérico
  importa.
- Los enums pueden tener métodos y properties.
- `Flag` para combinaciones de opciones.

## Ejercicio

Un `StrEnum` con una máquina de estados, un `IntEnum` para ordenar por prioridad y un `Flag`
de permisos.

**Para profundizar:** [enum](https://docs.python.org/3/library/enum.html),
[Enum HOWTO](https://docs.python.org/3/howto/enum.html).
