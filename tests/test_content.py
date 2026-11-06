"""Validates the whole syllabus: every chapter must be complete and consistent."""

import pytest

from app.content import load_courses
from app.render import markdown

COURSES = load_courses()
CHAPTERS = [c for course in COURSES for c in course.chapters()]


def test_there_is_content():
    assert CHAPTERS
    assert "python" in {c.slug for c in COURSES}


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c.id)
def test_chapter_has_all_files(chapter):
    language = chapter.language
    for name in (
        "lesson.md",
        "quiz.toml",
        language.exercise_file,
        language.tests_file,
        language.solution_file,
    ):
        assert (chapter.path / name).exists(), f"missing {name}"
    assert chapter.title != chapter.slug, "lesson.md must start with '# Title'"


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c.id)
def test_lesson_renders(chapter):
    html = markdown(chapter.lesson())
    assert "<h2>" in html


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c.id)
def test_quiz_is_valid(chapter):
    questions = chapter.questions()
    assert len(questions) >= 4
    for q in questions:
        assert q.text and q.explanation
        assert len(q.options) >= 2
        assert 0 <= q.correct < len(q.options)
        assert len(set(q.options)) == len(q.options), "duplicated options"


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c.id)
def test_solution_passes_the_tests(chapter):
    result = chapter.language.run(chapter.solution(), chapter.support_files())
    assert result.error is None, result.error
    failed = [t for t in result.tests if not t.ok]
    assert not failed, "\n\n".join(f"{t.name}\n{t.message}" for t in failed)


@pytest.mark.parametrize("chapter", CHAPTERS, ids=lambda c: c.id)
def test_starter_code_does_not_pass(chapter):
    result = chapter.language.run(chapter.starter_code(), chapter.support_files())
    assert result.error is None, f"the starter code must compile: {result.error}"
    # Every test must fail while the exercise is unsolved.
    passing = [t.name for t in result.tests if t.ok]
    assert not passing, f"these tests pass without solving the exercise: {passing}"
