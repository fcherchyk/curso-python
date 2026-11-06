"""Loads the courses from `content/`.

Expected layout:

    content/
      <course>/
        course.toml              # title, language (python), order, description
        NN-module/
          module.toml            # title, description
          NN-chapter/
            lesson.md            # the first line `# Title` is the chapter title
            quiz.toml            # [[questions]] text, options, correct (0-based), explanation
            <exercise>           # starter code           (exercise.py)
            <tests>              # tests                  (test_exercise.py)
            <solution>           # reference solution     (solution.py)
            ...                  # support files the tests need
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from app.languages import LANGUAGES, Language

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "content"


@dataclass(frozen=True)
class Question:
    text: str
    options: list[str]
    correct: int
    explanation: str = ""


@dataclass
class Chapter:
    course: str
    module: str
    slug: str
    title: str
    path: Path
    language: Language

    @property
    def id(self) -> str:
        return f"{self.course}/{self.module}/{self.slug}"

    @property
    def number(self) -> str:
        return self.slug.split("-", 1)[0]

    def lesson(self) -> str:
        """The lesson's Markdown without the title line."""
        text = (self.path / "lesson.md").read_text(encoding="utf-8")
        first, _, rest = text.partition("\n")
        return rest if first.startswith("# ") else text

    def questions(self) -> list[Question]:
        path = self.path / "quiz.toml"
        if not path.exists():
            return []
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        return [Question(**q) for q in data.get("questions", [])]

    def starter_code(self) -> str:
        return (self.path / self.language.exercise_file).read_text(encoding="utf-8")

    def solution(self) -> str:
        return (self.path / self.language.solution_file).read_text(encoding="utf-8")

    @property
    def tests_file(self) -> Path:
        return self.path / self.language.tests_file

    def support_files(self) -> list[Path]:
        """Tests, data and folders (e.g. `templates/`) the exercise needs."""
        private = self.language.private_files
        return [
            p
            for p in sorted(self.path.iterdir())
            if p.name not in private
            and not p.name.startswith((".", "__pycache__"))
            and (p.is_file() or p.is_dir())
        ]


@dataclass
class Module:
    slug: str
    title: str
    description: str
    chapters: list[Chapter] = field(default_factory=list)

    @property
    def number(self) -> str:
        return self.slug.split("-", 1)[0]


@dataclass
class Course:
    slug: str
    title: str
    description: str
    language: Language
    order: int
    modules: list[Module] = field(default_factory=list)

    def chapters(self) -> list[Chapter]:
        return [c for m in self.modules for c in m.chapters]

    def chapter(self, module: str, slug: str) -> Chapter | None:
        return next((c for c in self.chapters() if c.module == module and c.slug == slug), None)

    def module(self, slug: str) -> Module | None:
        return next((m for m in self.modules if m.slug == slug), None)

    def neighbors(self, chapter: Chapter) -> tuple[Chapter | None, Chapter | None]:
        everything = self.chapters()
        i = next(i for i, c in enumerate(everything) if c.id == chapter.id)
        previous = everything[i - 1] if i > 0 else None
        following = everything[i + 1] if i + 1 < len(everything) else None
        return previous, following


def _title_of(lesson: Path, default: str) -> str:
    with lesson.open(encoding="utf-8") as f:
        first = f.readline().strip()
    return first.removeprefix("# ").strip() if first.startswith("# ") else default


def _read_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def load_course(course_dir: Path) -> Course:
    meta = _read_toml(course_dir / "course.toml")
    language = LANGUAGES[str(meta["language"])]
    course = Course(
        slug=course_dir.name,
        title=str(meta.get("title", course_dir.name)),
        description=str(meta.get("description", "")),
        language=language,
        order=int(meta.get("order", 99)),  # type: ignore[call-overload]
    )
    for module_dir in sorted(p for p in course_dir.iterdir() if (p / "module.toml").exists()):
        module_meta = _read_toml(module_dir / "module.toml")
        module = Module(
            slug=module_dir.name,
            title=str(module_meta.get("title", module_dir.name)),
            description=str(module_meta.get("description", "")),
        )
        for chapter_dir in sorted(p for p in module_dir.iterdir() if (p / "lesson.md").exists()):
            module.chapters.append(
                Chapter(
                    course=course.slug,
                    module=module_dir.name,
                    slug=chapter_dir.name,
                    title=_title_of(chapter_dir / "lesson.md", chapter_dir.name),
                    path=chapter_dir,
                    language=language,
                )
            )
        course.modules.append(module)
    return course


def load_courses(root: Path = CONTENT_ROOT) -> list[Course]:
    courses = [load_course(d) for d in root.iterdir() if (d / "course.toml").exists()]
    return sorted(courses, key=lambda c: (c.order, c.slug))
