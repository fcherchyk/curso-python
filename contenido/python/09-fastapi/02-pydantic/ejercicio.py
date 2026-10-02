"""Pydantic: validar datos con tipos.

1. Direccion: calle (str, mín. 3 caracteres), ciudad (str), cp (str de exactamente 4 dígitos).
2. UsuarioNuevo:
   - nombre: 2 a 50 caracteres, SIN espacios alrededor (field_validator que hace strip;
     el largo se valida después del strip)
   - email: tiene que contener "@"; se guarda en minúscula (field_validator)
   - edad: entre 0 y 130
   - password: mínimo 8 caracteres
   - direccion: Direccion | None = None
   - regla entre campos (model_validator): password distinto del nombre (sin importar
     mayúsculas) → si no, ValueError("la contraseña no puede ser igual al nombre")
3. UsuarioPublico: id, nombre, email, edad (sin password ni dirección).
4. POST /usuarios: body UsuarioNuevo → 201 con UsuarioPublico (response_model), id incremental.
   GET  /usuarios/{id}: UsuarioPublico o 404.
"""

from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, Field, field_validator, model_validator  # noqa: F401


class Direccion(BaseModel):
    calle: str
    ciudad: str
    cp: str


class UsuarioNuevo(BaseModel):
    nombre: str
    email: str
    edad: int
    password: str
    direccion: Direccion | None = None


class UsuarioPublico(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int


app = FastAPI()
USUARIOS: dict[int, dict[str, object]] = {}
