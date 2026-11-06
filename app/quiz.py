"""Quiz grading."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from app.content import Question

PASS_THRESHOLD = 0.8


@dataclass(frozen=True)
class GradedAnswer:
    question: Question
    chosen: int | None
    ok: bool


@dataclass(frozen=True)
class QuizResult:
    answers: list[GradedAnswer]

    @property
    def correct(self) -> int:
        return sum(a.ok for a in self.answers)

    @property
    def total(self) -> int:
        return len(self.answers)

    @property
    def score(self) -> float:
        return self.correct / self.total if self.total else 0.0

    @property
    def passed(self) -> bool:
        return self.total > 0 and self.score >= PASS_THRESHOLD


def grade(questions: list[Question], chosen: Mapping[int, int | None]) -> QuizResult:
    """`chosen` maps question index -> option index (None if unanswered)."""
    return QuizResult(
        [
            GradedAnswer(q, chosen.get(i), chosen.get(i) == q.correct)
            for i, q in enumerate(questions)
        ]
    )
