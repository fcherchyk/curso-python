"""Persistencia del progreso en SQLite (un solo usuario, local)."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

ESQUEMA = """
CREATE TABLE IF NOT EXISTS capitulos (
    id          TEXT PRIMARY KEY,
    leido       INTEGER NOT NULL DEFAULT 0,
    quiz_ok     INTEGER NOT NULL DEFAULT 0,
    quiz_mejor  REAL    NOT NULL DEFAULT 0,
    tests_ok    INTEGER NOT NULL DEFAULT 0,
    codigo      TEXT,
    actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
)
"""


@dataclass(frozen=True)
class Estado:
    leido: bool = False
    quiz_ok: bool = False
    quiz_mejor: float = 0.0
    tests_ok: bool = False
    codigo: str | None = None

    @property
    def completo(self) -> bool:
        return self.leido and self.quiz_ok and self.tests_ok


class Progreso:
    def __init__(self, ruta: Path) -> None:
        self.ruta = ruta

    def _conectar(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.ruta)
        con.row_factory = sqlite3.Row
        # Idempotente: si borrás progreso.db con la app corriendo, se recrea.
        con.execute(ESQUEMA)
        return con

    def _upsert(self, id_cap: str, **campos: object) -> None:
        columnas = ", ".join(campos)
        marcadores = ", ".join("?" for _ in campos)
        actualizar = ", ".join(f"{c} = excluded.{c}" for c in campos)
        sql = (
            f"INSERT INTO capitulos (id, {columnas}) VALUES (?, {marcadores}) "
            f"ON CONFLICT(id) DO UPDATE SET {actualizar}, actualizado = datetime('now')"
        )
        with closing(self._conectar()) as con, con:
            con.execute(sql, (id_cap, *campos.values()))

    def estado(self, id_cap: str) -> Estado:
        return self.todos().get(id_cap, Estado())

    def todos(self) -> dict[str, Estado]:
        with closing(self._conectar()) as con:
            filas = con.execute("SELECT * FROM capitulos").fetchall()
        return {
            f["id"]: Estado(
                leido=bool(f["leido"]),
                quiz_ok=bool(f["quiz_ok"]),
                quiz_mejor=f["quiz_mejor"],
                tests_ok=bool(f["tests_ok"]),
                codigo=f["codigo"],
            )
            for f in filas
        }

    def marcar_leido(self, id_cap: str, leido: bool = True) -> None:
        self._upsert(id_cap, leido=int(leido))

    def marcar_quiz(self, id_cap: str, ok: bool = True) -> None:
        self._upsert(id_cap, quiz_ok=int(ok))

    def marcar_tests(self, id_cap: str, ok: bool = True) -> None:
        self._upsert(id_cap, tests_ok=int(ok))

    def registrar_quiz(self, id_cap: str, puntaje: float, aprobado: bool) -> None:
        # El mejor puntaje y la aprobación no retroceden al reintentar.
        actual = self.estado(id_cap)
        self._upsert(
            id_cap,
            quiz_mejor=max(actual.quiz_mejor, puntaje),
            quiz_ok=int(actual.quiz_ok or aprobado),
        )

    def guardar_codigo(self, id_cap: str, codigo: str) -> None:
        self._upsert(id_cap, codigo=codigo)

    def registrar_tests(self, id_cap: str, codigo: str, aprobado: bool) -> None:
        actual = self.estado(id_cap)
        self._upsert(id_cap, codigo=codigo, tests_ok=int(actual.tests_ok or aprobado))
