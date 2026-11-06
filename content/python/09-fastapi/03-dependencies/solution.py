from dataclasses import asdict, dataclass, field
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status


@dataclass
class Usuario:
    nombre: str
    es_admin: bool = False


TOKENS = {"t-ana": Usuario("ana", es_admin=True), "t-beto": Usuario("beto")}


@dataclass
class Pagina:
    offset: int
    limite: int


@dataclass
class RepoProductos:
    productos: list[str] = field(default_factory=list)

    def listar(self, offset: int, limite: int) -> list[str]:
        return self.productos[offset : offset + limite]

    def borrar(self, indice: int) -> bool:
        if 0 <= indice < len(self.productos):
            del self.productos[indice]
            return True
        return False


REPO = RepoProductos([f"producto {i}" for i in range(1, 26)])


def get_repo() -> RepoProductos:
    return REPO


def paginacion(
    pagina: Annotated[int, Query(ge=1)] = 1,
    por_pagina: Annotated[int, Query(ge=1, le=50)] = 10,
) -> Pagina:
    return Pagina(offset=(pagina - 1) * por_pagina, limite=por_pagina)


def usuario_actual(authorization: Annotated[str | None, Header()] = None) -> Usuario:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="falta el token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario = TOKENS.get(authorization.removeprefix("Bearer "))
    if usuario is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="token inválido")
    return usuario


def solo_admin(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> Usuario:
    if not usuario.es_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="requiere admin")
    return usuario


Repo = Annotated[RepoProductos, Depends(get_repo)]

app = FastAPI()


@app.get("/productos")
def listar(pag: Annotated[Pagina, Depends(paginacion)], repo: Repo) -> list[str]:
    return repo.listar(pag.offset, pag.limite)


@app.get("/yo")
def yo(usuario: Annotated[Usuario, Depends(usuario_actual)]) -> dict[str, object]:
    return asdict(usuario)


@app.delete("/productos/{id}", status_code=204, dependencies=[Depends(solo_admin)])
def borrar(id: int, repo: Repo) -> None:
    if not repo.borrar(id):
        raise HTTPException(404, "producto inexistente")
