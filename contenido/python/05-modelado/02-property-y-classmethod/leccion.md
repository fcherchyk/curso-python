# property, classmethod y staticmethod

Tres decoradores que cambian cómo se accede a un método. `@property` permite empezar con
atributos públicos simples y agregar lógica después **sin romper a nadie**. `@classmethod`
es la forma idiomática de escribir constructores alternativos. `@staticmethod` es para
funciones que viven en la clase por organización.

## El problema: getters y setters

En Java es habitual escribir `getSaldo()` y `setSaldo()` "por las dudas". En Python no:

```python
class Producto:
    def __init__(self, precio):
        self.precio = precio           # atributo público, simple

p = Producto(100)
p.precio = 120
```

Si mañana necesitás validar que el precio no sea negativo, no hace falta cambiar la API a
`set_precio()`: convertís el atributo en una **property** y todo el código que hace
`p.precio = x` sigue funcionando.

## `@property`: atributos calculados o controlados

```python
class Producto:
    def __init__(self, precio: float) -> None:
        self.precio = precio           # ¡pasa por el setter también!

    @property
    def precio(self) -> float:         # getter: se accede como p.precio
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise ValueError(f"precio negativo: {valor}")
        self._precio = valor

    @property
    def precio_con_iva(self) -> float:   # solo getter: de solo lectura
        return round(self._precio * 1.21, 2)
```

```python
p = Producto(100)
p.precio_con_iva          # 121.0  (sin paréntesis)
p.precio = -5             # ValueError
p.precio_con_iva = 1      # AttributeError: property has no setter
```

Detalles importantes:

- El valor real se guarda en otro atributo (`_precio`). Si el getter hiciera
  `return self.precio`, se llamaría a sí mismo en una recursión infinita.
- Asignar en `__init__` con `self.precio = …` hace que la **validación también corra al
  construir**.
- Una property sin setter es de **solo lectura**.
- Existe también `@precio.deleter`, pero casi nunca se usa.

### Cuándo usar una property

- **Valores derivados** baratos de calcular: `nombre_completo`, `total`, `es_mayor`.
- **Validación o normalización** al asignar.
- **Compatibilidad**: convertir un atributo en calculado sin cambiar la API.

Cuándo **no**:

- Si el cálculo es caro o tiene efectos secundarios (I/O, red): quien lee `obj.x` espera que
  sea instantáneo. Usá un método con nombre de verbo (`calcular_x()`) o
  `functools.cached_property`, que calcula la primera vez y guarda el resultado.

## `@classmethod`: constructores alternativos

Un classmethod recibe **la clase** (`cls`) en lugar de la instancia. Su uso principal es
ofrecer otras formas de crear objetos:

```python
from datetime import date

class Persona:
    def __init__(self, nombre: str, nacimiento: date) -> None:
        self.nombre = nombre
        self.nacimiento = nacimiento

    @classmethod
    def desde_dict(cls, datos: dict) -> "Persona":
        return cls(datos["nombre"], date.fromisoformat(datos["nacimiento"]))

    @classmethod
    def desde_csv(cls, linea: str) -> "Persona":
        nombre, fecha = linea.split(",")
        return cls(nombre.strip(), date.fromisoformat(fecha.strip()))
```

¿Por qué `cls(...)` y no `Persona(...)`? Porque si alguien hereda (`class Empleado(Persona)`),
`Empleado.desde_dict(...)` va a crear un `Empleado`. La stdlib usa este patrón en todos
lados: `dict.fromkeys`, `datetime.fromisoformat`, `int.from_bytes`, `Path.cwd()`.

La convención de nombres es `desde_…` / `from_…`.

## `@staticmethod`: una función en el namespace de la clase

```python
class Email:
    @staticmethod
    def normalizar(texto: str) -> str:
        return texto.strip().lower()
```

No recibe ni `self` ni `cls`: es una función común que vive dentro de la clase porque está
relacionada con ella. Muchas veces una función a nivel de módulo es igual de buena, o mejor.
Si el método necesita la clase, es un `classmethod`; si necesita la instancia, es un método
normal.

| Decorador       | Primer parámetro | Uso típico                            |
|-----------------|------------------|---------------------------------------|
| (ninguno)       | `self`           | comportamiento de la instancia        |
| `@classmethod`  | `cls`            | constructores alternativos, fábricas  |
| `@staticmethod` | —                | utilidades relacionadas con la clase  |
| `@property`     | `self`           | atributo calculado o validado         |

## Cómo funciona por dentro (una pincelada)

`property`, `classmethod` y `staticmethod` son **descriptores**: objetos con `__get__` (y
`__set__`) que Python consulta cuando accedés a un atributo de la clase. Con descriptores
están implementados los métodos (el `self` automático), las properties y los campos de
Django y SQLAlchemy. No hace falta escribirlos seguido, pero conviene saber que existen.

## Resumen

- Empezá con atributos públicos; convertilos en `@property` cuando necesites lógica.
- Guardá el valor real en `_atributo` y asigná por la property en `__init__` para validar
  siempre.
- Sin setter, la property es de solo lectura.
- `@classmethod` + `cls(...)` para constructores alternativos (`desde_…`).
- `@staticmethod` para utilidades sin estado; una función de módulo suele alcanzar.

## Ejercicio

Una `Temperatura` con properties validadas y convertibles, y un `Usuario` con email
normalizado, id de solo lectura y un constructor alternativo.

**Para profundizar:** [property](https://docs.python.org/3/library/functions.html#property),
[Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html), *Fluent Python*, cap. 22.
