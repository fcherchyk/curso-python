"""What changes between languages: file names, editor, highlighting and runner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.runner import RunResult, run_tests


@dataclass(frozen=True)
class Language:
    name: str
    exercise_file: str
    tests_file: str
    solution_file: str
    editor_mode: str  # CodeMirror 5 mode
    lexer: str  # Pygments lexer
    indent_with_tabs: bool
    where_instructions_are: str
    run: Callable[[str, list[Path]], RunResult]

    @property
    def private_files(self) -> frozenset[str]:
        """Chapter files that are NOT copied to the directory where the tests run."""
        return frozenset({"lesson.md", "quiz.toml", self.exercise_file, self.solution_file})


PYTHON = Language(
    name="python",
    exercise_file="exercise.py",
    tests_file="test_exercise.py",
    solution_file="solution.py",
    editor_mode="python",
    lexer="python",
    indent_with_tabs=False,
    where_instructions_are="the docstrings",
    run=run_tests,
)

LANGUAGES = {language.name: language for language in (PYTHON,)}
