"""Corrección de cuestionarios."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from app.contenido import Pregunta

UMBRAL_APROBACION = 0.8


@dataclass(frozen=True)
class RespuestaCorregida:
    pregunta: Pregunta
    elegida: int | None
    ok: bool


@dataclass(frozen=True)
class ResultadoQuiz:
    respuestas: list[RespuestaCorregida]

    @property
    def correctas(self) -> int:
        return sum(r.ok for r in self.respuestas)

    @property
    def total(self) -> int:
        return len(self.respuestas)

    @property
    def puntaje(self) -> float:
        return self.correctas / self.total if self.total else 0.0

    @property
    def aprobado(self) -> bool:
        return self.total > 0 and self.puntaje >= UMBRAL_APROBACION


def corregir(preguntas: list[Pregunta], elegidas: Mapping[int, int | None]) -> ResultadoQuiz:
    """`elegidas` mapea índice de pregunta -> índice de opción (None si no respondió)."""
    return ResultadoQuiz(
        [
            RespuestaCorregida(p, elegidas.get(i), elegidas.get(i) == p.correcta)
            for i, p in enumerate(preguntas)
        ]
    )
