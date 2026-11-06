"""Course web app: reading → quiz → exercise checked by tests.

uv run uvicorn app.main:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Literal

from fastapi import FastAPI, Form, HTTPException, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import legacy_ids, render
from app.content import CONTENT_ROOT, Chapter, Course, load_courses
from app.progress import Progress, Status
from app.quiz import PASS_THRESHOLD, grade

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent / "progress.db"
LEGACY_DB = HERE.parent / "progreso.db"  # Spanish-era progress file, imported once
COURSE_COOKIE = "course"


def create_app(
    content_root: Path = CONTENT_ROOT,
    db_path: Path | None = None,
    reload_content: bool = True,
    legacy_db_path: Path | None = LEGACY_DB,
) -> FastAPI:
    app = FastAPI(title="Programming courses", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")

    templates = Jinja2Templates(directory=HERE / "templates")
    templates.env.filters["markdown"] = render.markdown
    templates.env.filters["markdown_inline"] = render.markdown_inline
    templates.env.globals["THRESHOLD"] = int(PASS_THRESHOLD * 100)
    # Cache-busting for app.css/app.js: changes whenever any static file is edited.
    templates.env.globals["V"] = max(int(p.stat().st_mtime) for p in (HERE / "static").iterdir())

    progress = Progress(db_path or Path(os.environ.get("COURSE_DB", DEFAULT_DB)))
    if legacy_db_path is not None:
        progress.import_legacy(legacy_db_path)
    cache: dict[str, list[Course]] = {}

    def courses() -> list[Course]:
        # In development the content is re-read on every request so changes show up at once.
        if reload_content or "c" not in cache:
            cache["c"] = load_courses(content_root)
        return cache["c"]

    def find_course(slug: str) -> Course:
        course = next((c for c in courses() if c.slug == slug), None)
        if course is None:
            raise HTTPException(404, "Course not found")
        return course

    def find(course: str, module: str, chapter: str) -> tuple[Course, Chapter]:
        c = find_course(course)
        found = c.chapter(module, chapter)
        if found is None:
            raise HTTPException(404, "Chapter not found")
        return c, found

    def page(
        request: Request, template: str, course: Course, context: dict[str, object]
    ) -> HTMLResponse:
        response = templates.TemplateResponse(
            request, template, {"courses": courses(), "course": course, **context}
        )
        response.set_cookie(COURSE_COOKIE, course.slug, max_age=60 * 60 * 24 * 365)
        return response

    @app.get("/pygments.css", include_in_schema=False)
    def pygments_css() -> Response:
        return Response(render.pygments_css(), media_type="text/css")

    @app.get("/", include_in_schema=False)
    def root(request: Request) -> RedirectResponse:
        slugs = [c.slug for c in courses()]
        preferred = request.cookies.get(COURSE_COOKIE)
        return RedirectResponse(f"/{preferred if preferred in slugs else slugs[0]}")

    @app.get("/c/{module}/{chapter}", include_in_schema=False)
    def pre_course_url(module: str, chapter: str) -> RedirectResponse:
        # Before multi-course support, Python chapters lived at /c/{module}/{chapter}.
        new_id = legacy_ids.translate_id(f"{module}/{chapter}")
        return RedirectResponse(f"/c/{new_id}", status_code=301)

    @app.get("/{course}", response_class=HTMLResponse)
    def index(request: Request, course: str) -> HTMLResponse:
        c = find_course(course)
        statuses = progress.all()
        next_chapter = next(
            (ch for ch in c.chapters() if not statuses.get(ch.id, Status()).complete), None
        )
        completed = {
            m.slug: sum(statuses.get(ch.id, Status()).complete for ch in m.chapters)
            for m in c.modules
        }
        return page(
            request,
            "index.html",
            c,
            {"statuses": statuses, "next_chapter": next_chapter, "completed": completed},
        )

    @app.get("/c/{course}/{module}/{chapter}", response_class=HTMLResponse, response_model=None)
    def chapter_page(
        request: Request, course: str, module: str, chapter: str
    ) -> HTMLResponse | RedirectResponse:
        cur = find_course(course)
        if cur.chapter(module, chapter) is None and (
            new := legacy_ids.translate_path(module, chapter)
        ):
            # Old Spanish URL: send it to the chapter's current address.
            return RedirectResponse(f"/c/{course}/{new[0]}/{new[1]}", status_code=301)
        cur, c = find(course, module, chapter)
        status = progress.status(c.id)
        previous, following = cur.neighbors(c)
        return page(
            request,
            "chapter.html",
            cur,
            {
                "chapter": c,
                "module": cur.module(c.module),
                "statuses": progress.all(),
                "status": status,
                "lesson": render.markdown(c.lesson()),
                "questions": c.questions(),
                "code": status.code if status.code is not None else c.starter_code(),
                "previous": previous,
                "following": following,
            },
        )

    @app.post("/c/{course}/{module}/{chapter}/read", response_class=HTMLResponse)
    def mark_read(request: Request, course: str, module: str, chapter: str) -> HTMLResponse:
        _, c = find(course, module, chapter)
        progress.mark_read(c.id, not progress.status(c.id).read)
        return templates.TemplateResponse(
            request, "_read.html", {"chapter": c, "status": progress.status(c.id)}
        )

    @app.post("/c/{course}/{module}/{chapter}/{step}/solved", response_class=HTMLResponse)
    def mark_solved(
        request: Request,
        course: str,
        module: str,
        chapter: str,
        step: Literal["quiz", "tests"],
    ) -> HTMLResponse:
        """Toggles a step by hand, to skip it without doing it. Counts the same as passing it."""
        _, c = find(course, module, chapter)
        current = progress.status(c.id)
        if step == "quiz":
            progress.mark_quiz(c.id, not current.quiz_ok)
        else:
            progress.mark_tests(c.id, not current.tests_ok)
        status = progress.status(c.id)
        ok = status.quiz_ok if step == "quiz" else status.tests_ok
        return templates.TemplateResponse(
            request, "_solved.html", {"chapter": c, "step": step, "ok": ok, "status": status}
        )

    @app.post("/c/{course}/{module}/{chapter}/quiz", response_class=HTMLResponse)
    async def answer_quiz(request: Request, course: str, module: str, chapter: str) -> HTMLResponse:
        _, c = find(course, module, chapter)
        questions = c.questions()
        form = await request.form()
        chosen: dict[int, int | None] = {}
        for i in range(len(questions)):
            value = form.get(f"q{i}")
            chosen[i] = int(value) if isinstance(value, str) and value.isdigit() else None
        result = grade(questions, chosen)
        progress.record_quiz(c.id, result.score, result.passed)
        return templates.TemplateResponse(
            request,
            "_quiz.html",
            {
                "chapter": c,
                "questions": questions,
                "result": result,
                "status": progress.status(c.id),
            },
        )

    @app.post("/c/{course}/{module}/{chapter}/code", status_code=204)
    def save_code(course: str, module: str, chapter: str, code: Annotated[str, Form()]) -> Response:
        _, c = find(course, module, chapter)
        progress.save_code(c.id, code)
        return Response(status_code=204)

    @app.post("/c/{course}/{module}/{chapter}/tests", response_class=HTMLResponse)
    async def run_tests(
        request: Request, course: str, module: str, chapter: str, code: Annotated[str, Form()]
    ) -> HTMLResponse:
        _, c = find(course, module, chapter)
        result = await run_in_threadpool(c.language.run, code, c.support_files())
        progress.record_tests(c.id, code, result.passed)
        return templates.TemplateResponse(
            request,
            "_tests_result.html",
            {"chapter": c, "result": result, "status": progress.status(c.id)},
        )

    @app.get("/c/{course}/{module}/{chapter}/solution", response_class=HTMLResponse)
    def show_solution(course: str, module: str, chapter: str) -> HTMLResponse:
        _, c = find(course, module, chapter)
        if not progress.status(c.id).tests_ok:
            return HTMLResponse(
                '<p class="notice">The solution unlocks once all the tests pass.</p>'
            )
        return HTMLResponse(str(render.code_html(c.solution(), c.language.lexer)))

    @app.get("/c/{course}/{module}/{chapter}/starter", response_class=PlainTextResponse)
    def starter_code(course: str, module: str, chapter: str) -> str:
        return find(course, module, chapter)[1].starter_code()

    return app


app = create_app()
