"""Inyección de dependencias con Depends.

Dependencias a escribir:
- paginacion(pagina=1 (≥1), por_pagina=10 (≥1, ≤50)) → Pagina(offset, limite)
- usuario_actual(authorization: header) → Usuario
    sin header o sin "Bearer " → 401 detail "falta el token" (header WWW-Authenticate: Bearer)
    token que no está en TOKENS → 401 detail "token inválido"
- solo_admin(usuario = Depends(usuario_actual)) → el usuario, o 403 detail "requiere admin"
- get_repo() → RepoProductos (ya escrita: devolvé REPO)

Endpoints:
- GET    /productos             → repo.listar(offset, limite)  (paginado)
- GET    /yo                    → {"nombre", "es_admin"} del usuario actual
- DELETE /productos/{id}        → solo admin; repo.borrar(id) → 204, o 404 si no existía
"""

from dataclasses import dataclass, field
from typing import Annotated  # noqa: F401

from fastapi import Depends, FastAPI, Header, HTTPException, Query, status  # noqa: F401


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


def paginacion() -> Pagina:  # ← agregale los parámetros
    raise NotImplementedError("TODO")


def usuario_actual() -> Usuario:  # ← agregale el header
    raise NotImplementedError("TODO")


def solo_admin() -> Usuario:  # ← que dependa de usuario_actual
    raise NotImplementedError("TODO")


app = FastAPI()
