import re
import sqlite3
from pathlib import Path
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient

from app.content import load_courses
from app.main import create_app
from app.progress import Progress

COURSES = {c.slug: c for c in load_courses()}
CHAPTER = COURSES["python"].chapters()[0]
URL = f"/c/{CHAPTER.id}"


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(db_path=tmp_path / "progress.db", legacy_db_path=None))


def make_course(root: Path, slug: str, order: int) -> None:
    """A minimal Python course with one chapter, to test multi-course support."""
    course = root / slug
    chapter = course / "01-module" / "01-chapter"
    chapter.mkdir(parents=True)
    (course / "course.toml").write_text(
        f'title = "{slug.title()}"\nlanguage = "python"\norder = {order}\n'
    )
    (course / "01-module" / "module.toml").write_text('title = "Module"\n')
    (chapter / "lesson.md").write_text(f"# Chapter of {slug}\n\nText.\n")
    for name in ("exercise.py", "solution.py", "test_exercise.py"):
        (chapter / name).write_text("")


@pytest.fixture
def two_courses_client(tmp_path: Path) -> TestClient:
    root = tmp_path / "content"
    make_course(root, "python", 1)
    make_course(root, "other", 2)
    return TestClient(
        create_app(content_root=root, db_path=tmp_path / "progress.db", legacy_db_path=None)
    )


def correct_answers() -> dict[str, str]:
    return {f"q{i}": str(q.correct) for i, q in enumerate(CHAPTER.questions())}


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert CHAPTER.title in r.text


def test_chapter(client):
    r = client.get(URL)
    assert r.status_code == 200
    assert "Quiz" in r.text and "exercise.py" in r.text


def test_missing_chapter(client):
    assert client.get("/c/python/nothing/nothing").status_code == 404


def test_mark_read_toggles(client):
    assert "✓ Read" in client.post(f"{URL}/read").text
    assert "Mark as read" in client.post(f"{URL}/read").text


def test_quiz_passed(client):
    r = client.post(f"{URL}/quiz", data=correct_answers())
    assert r.status_code == 200
    assert "Passed" in r.text
    assert 'id="mark-quiz"' in r.text


def test_failed_quiz_does_not_reveal_explanations(client):
    r = client.post(f"{URL}/quiz", data={})
    assert "You need" in r.text
    assert CHAPTER.questions()[0].explanation[:20] not in r.text


def test_tests_and_solution(client):
    assert "unlocks" in client.get(f"{URL}/solution").text

    r = client.post(f"{URL}/tests", data={"code": CHAPTER.starter_code()})
    assert "0 of" in r.text

    r = client.post(f"{URL}/tests", data={"code": CHAPTER.solution()})
    assert "Exercise passed" in r.text
    assert "<pre><code" in client.get(f"{URL}/solution").text


def test_progress_persists_and_completes(client):
    client.post(f"{URL}/read")
    client.post(f"{URL}/quiz", data=correct_answers())
    client.post(f"{URL}/tests", data={"code": CHAPTER.solution()})
    # A later failed attempt does not undo what was passed.
    client.post(f"{URL}/tests", data={"code": CHAPTER.starter_code()})
    client.post(f"{URL}/quiz", data={})

    index = client.get("/").text
    assert "chapter-row complete" in index


def test_autosave(client):
    assert client.post(f"{URL}/code", data={"code": "# my code"}).status_code == 204
    assert "# my code" in client.get(URL).text
    assert client.get(f"{URL}/starter").text == CHAPTER.starter_code()


def test_marking_steps_solved_completes_the_chapter(client):
    client.post(f"{URL}/read")
    r = client.post(f"{URL}/quiz/solved")
    assert "✓ Solved" in r.text and 'id="mark-quiz"' in r.text
    r = client.post(f"{URL}/tests/solved")
    assert "✓ Solved" in r.text and 'id="mark-tests"' in r.text
    assert "see the reference solution" in r.text

    assert "chapter-row complete" in client.get("/").text
    assert "<pre><code" in client.get(f"{URL}/solution").text


def test_mark_solved_is_a_toggle(client):
    client.post(f"{URL}/tests/solved")
    r = client.post(f"{URL}/tests/solved")
    assert "Mark as solved" in r.text
    assert "unlocks" in client.get(f"{URL}/solution").text


def test_mark_solved_invalid_step(client):
    assert client.post(f"{URL}/lesson/solved").status_code == 422


def test_course_tabs(two_courses_client):
    r = two_courses_client.get("/python")
    assert 'class="course-tab active"' in r.text
    assert 'href="/other"' in r.text


def test_no_tabs_with_a_single_course(client):
    assert 'class="course-tabs"' not in client.get("/python").text


def test_root_remembers_last_course(two_courses_client):
    two_courses_client.get("/other")
    r = two_courses_client.get("/", follow_redirects=False)
    assert r.headers["location"] == "/other"


def test_missing_course(client):
    assert client.get("/cobol").status_code == 404


def test_pre_course_spanish_url_redirects(client):
    r = client.get("/c/01-fundamentos/01-objetos-y-mutabilidad", follow_redirects=False)
    assert r.status_code == 301
    assert r.headers["location"] == "/c/python/01-fundamentals/01-objects-and-mutability"


def test_spanish_chapter_url_redirects(client):
    r = client.get("/c/python/14-finanzas/02-riesgo", follow_redirects=False)
    assert r.status_code == 301
    assert r.headers["location"] == "/c/python/14-finance/02-risk"


def make_legacy_db(path: Path, rows: list[tuple]) -> None:
    with sqlite3.connect(path) as con:
        con.execute(
            "CREATE TABLE capitulos (id TEXT PRIMARY KEY, leido INTEGER, quiz_ok INTEGER, "
            "quiz_mejor REAL, tests_ok INTEGER, codigo TEXT, actualizado TEXT)"
        )
        con.executemany("INSERT INTO capitulos VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    con.close()


def test_imports_legacy_progress(tmp_path):
    legacy = tmp_path / "progreso.db"
    make_legacy_db(
        legacy,
        [
            ("python/01-fundamentos/01-objetos-y-mutabilidad", 1, 1, 0.8, 1, "x = 1", "2026-10-01"),
            ("02-idiomatico/02-desempaquetado", 1, 0, 0.4, 0, None, "2026-10-02"),
            ("other/01-module/01-chapter", 1, 0, 0.0, 0, None, "2026-10-03"),
        ],
    )
    progress = Progress(tmp_path / "progress.db")
    assert progress.import_legacy(legacy) == 3
    statuses = progress.all()
    first = statuses["python/01-fundamentals/01-objects-and-mutability"]
    assert first.complete and first.quiz_best == 0.8 and first.code == "x = 1"
    assert statuses["python/02-idiomatic/02-unpacking"].read
    assert "other/01-module/01-chapter" in statuses
    # Idempotent: a second import does nothing because the store is no longer empty.
    assert progress.import_legacy(legacy) == 0


def test_app_imports_legacy_db_on_startup(tmp_path):
    legacy = tmp_path / "progreso.db"
    row = ("python/01-fundamentos/01-objetos-y-mutabilidad", 1, 1, 1.0, 1, None, "")
    make_legacy_db(legacy, [row])
    client = TestClient(create_app(db_path=tmp_path / "progress.db", legacy_db_path=legacy))
    assert "chapter-row complete" in client.get("/python").text


def test_progress_is_separate_per_course(two_courses_client):
    url = "/c/python/01-module/01-chapter"
    two_courses_client.post(f"{url}/read")
    two_courses_client.post(f"{url}/quiz/solved")
    two_courses_client.post(f"{url}/tests/solved")
    assert "chapter-row complete" in two_courses_client.get("/python").text
    assert "chapter-row complete" not in two_courses_client.get("/other").text


FONTS = {"fonts.googleapis.com", "fonts.gstatic.com"}  # with a local fallback in the CSS


def test_no_cdn_dependencies(client):
    """HTMX and CodeMirror are served from /static/vendor/: the app works offline."""
    for url in ("/python", URL):
        html = client.get(url).text
        resources = re.findall(r'<(?:script|link)\b[^>]*\b(?:src|href)="([^"]+)"', html)
        external = {
            urlparse(r).netloc for r in resources if urlparse(r).netloc not in {"", "testserver"}
        }
        assert external <= FONTS, f"{url} loads external resources: {external - FONTS}"
        vendor = [urlparse(r).path for r in resources if "/static/vendor/" in r]
        assert vendor, "expected resources from /static/vendor/"
        for path in vendor:
            assert client.get(path).status_code == 200, path
