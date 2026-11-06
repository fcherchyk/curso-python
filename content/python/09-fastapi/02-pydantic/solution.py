from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator


class Direccion(BaseModel):
    calle: str = Field(min_length=3)
    ciudad: str
    cp: str = Field(pattern=r"^\d{4}$")


class UsuarioNuevo(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    email: str
    edad: int = Field(ge=0, le=130)
    password: str = Field(min_length=8)
    direccion: Direccion | None = None

    # mode="before": el strip corre antes de chequear el largo.
    @field_validator("nombre", mode="before")
    @classmethod
    def limpiar_nombre(cls, v: object) -> object:
        return v.strip() if isinstance(v, str) else v

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email inválido")
        return v.lower()

    @model_validator(mode="after")
    def password_distinto_del_nombre(self) -> "UsuarioNuevo":
        if self.password.lower() == self.nombre.lower():
            raise ValueError("la contraseña no puede ser igual al nombre")
        return self


class UsuarioPublico(BaseModel):
    id: int
    nombre: str
    email: str
    edad: int


app = FastAPI()
USUARIOS: dict[int, dict[str, object]] = {}


@app.post("/usuarios", response_model=UsuarioPublico, status_code=201)
def crear_usuario(datos: UsuarioNuevo) -> dict[str, object]:
    nuevo_id = len(USUARIOS) + 1
    USUARIOS[nuevo_id] = {"id": nuevo_id, **datos.model_dump()}
    return USUARIOS[nuevo_id]  # incluye password: response_model lo filtra


@app.get("/usuarios/{id}", response_model=UsuarioPublico)
def ver_usuario(id: int) -> dict[str, object]:
    if id not in USUARIOS:
        raise HTTPException(404, "usuario inexistente")
    return USUARIOS[id]
