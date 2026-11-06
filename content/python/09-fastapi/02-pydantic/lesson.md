# Pydantic: validar datos con tipos

Pydantic es la librería de validación más usada de Python, y es el corazón de FastAPI. Declarás
un **modelo** con type hints y Pydantic **valida, convierte y serializa** los datos que llegan
de afuera (JSON de una API, archivos de configuración, variables de entorno). Si algo no cumple,
te da errores detallados por campo. Se diferencia de las dataclasses del módulo 05 en que
estas **no validan** nada.

## Un modelo

```python
from pydantic import BaseModel

class Producto(BaseModel):
    nombre: str
    precio: float
    tags: list[str] = []          # con default: opcional (Pydantic copia el default, no hay trampa)
    descripcion: str | None = None

p = Producto(nombre="yerba", precio="3500")     # "3500" se convierte a 3500.0
p.precio                                        # 3500.0
p.model_dump()                                  # dict
p.model_dump_json()                             # JSON (str)
Producto.model_validate({"nombre": "café", "precio": 10})   # desde un dict
Producto.model_validate_json('{"nombre": "té", "precio": 5}')
```

Si los datos no sirven, levanta `ValidationError` con **todos** los problemas juntos:

```python
Producto(nombre="x", precio="caro")
# ValidationError: 1 validation error for Producto
# precio
#   Input should be a valid number, unable to parse string as a number
```

Por defecto Pydantic está en **modo laxo**: convierte `"3500"` en `3500`. Con
`model_config = ConfigDict(strict=True)` (o `Field(strict=True)` en un campo) exige el tipo
exacto.

## Restricciones con `Field`

```python
from typing import Annotated
from pydantic import BaseModel, Field

class UsuarioNuevo(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    edad: int = Field(ge=0, le=130)              # ≥ 0 y ≤ 130
    password: str = Field(min_length=8)
    cp: str = Field(pattern=r"^\d{4}$")           # regex
    precio: Annotated[float, Field(gt=0)]         # forma equivalente con Annotated
```

Restricciones típicas: `gt`/`ge`/`lt`/`le` para números, `min_length`/`max_length` para strings
y listas, `pattern` para regex y `default`/`default_factory`. Para emails, `EmailStr` (necesita
`pip install "pydantic[email]"`).

## Validadores propios

```python
from pydantic import field_validator, model_validator

class UsuarioNuevo(BaseModel):
    nombre: str
    email: str
    password: str

    @field_validator("nombre", mode="before")
    @classmethod
    def limpiar_nombre(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v   # puede TRANSFORMAR el valor…

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email inválido")   # …o rechazarlo
        return v.lower()

    @model_validator(mode="after")
    def password_distinto_del_nombre(self) -> "UsuarioNuevo":
        if self.password.lower() == self.nombre.lower():
            raise ValueError("la contraseña no puede ser igual al nombre")
        return self
```

- `field_validator` valida **un campo**; devuelve el valor (transformado o no) o levanta
  `ValueError`.
- `model_validator(mode="after")` valida **reglas entre campos**, con el modelo ya construido.
- El orden importa. Con `mode="after"` (el default), tu validador corre **después** del tipo y
  de las restricciones de `Field`. Con `mode="before"`, corre **antes**, sobre el dato crudo
  (que puede no ser un `str`). Por eso el `strip` del ejemplo es `before`: así `min_length` se
  chequea sobre el nombre ya limpio.

## Modelos anidados

```python
class Direccion(BaseModel):
    calle: str
    ciudad: str

class Cliente(BaseModel):
    nombre: str
    direccion: Direccion                 # se valida recursivamente
    otras: list[Direccion] = []
```

Los errores indican la ruta completa: `direccion.ciudad: Field required`.

## Pydantic en FastAPI

FastAPI usa los modelos en las dos direcciones:

```python
class UsuarioPublico(BaseModel):          # lo que DEVOLVÉS (sin password)
    id: int
    nombre: str
    email: str

@app.post("/usuarios", response_model=UsuarioPublico, status_code=201)
def crear(datos: UsuarioNuevo):            # lo que RECIBÍS (validado)
    usuario = {"id": 1, **datos.model_dump()}
    return usuario                         # incluye password…
                                           # …pero response_model lo FILTRA
```

- El parámetro de tipo modelo es el **body**. Si no valida, FastAPI responde **422** con la lista
  de errores (`loc`, `msg`, `type`) sin entrar a tu función.
- `response_model` (o el tipo de retorno anotado) **filtra y valida la salida**: aunque devuelvas
  un dict con `password`, la respuesta solo tiene los campos de `UsuarioPublico`. Es la forma
  idiomática de no filtrar datos sensibles.
- El patrón habitual es tener **un modelo por caso de uso**: `XCrear` (entrada), `XActualizar`
  (con campos opcionales) y `XPublico` (salida).

## Serialización

```python
p.model_dump(exclude={"password"})
p.model_dump(exclude_none=True)           # sin los campos None
p.model_dump(mode="json")                 # tipos JSON-compatibles (fechas a string, etc.)
p.model_copy(update={"precio": 10})       # copia con cambios
```

## En los otros frameworks

- **Flask** no trae validación: se hace a mano, o con Pydantic, marshmallow o WTForms.
- **Django** valida con `Form` (HTML) y Django REST Framework con `Serializer`: la misma idea con
  otra sintaxis.
- También se usa Pydantic fuera de la web: `pydantic-settings` lee la configuración desde
  variables de entorno con tipos.

## Resumen

- `BaseModel` + type hints = validación y conversión; `ValidationError` reporta todos los errores.
- `Field(...)` para las restricciones (`ge`, `min_length`, `pattern`…).
- `field_validator` para un campo; `model_validator(mode="after")` para reglas entre campos.
- Modelos anidados y listas de modelos se validan recursivamente.
- En FastAPI: modelo como parámetro = body validado (si falla, 422); `response_model` filtra la
  salida.

## Ejercicio

Modelos de usuario con restricciones, normalización, una regla entre campos y una API que
nunca devuelve la contraseña.

**Para profundizar:** [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/),
[Validators](https://docs.pydantic.dev/latest/concepts/validators/),
[FastAPI: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).
