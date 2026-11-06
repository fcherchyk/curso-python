# Architecture

This document describes how the course app is built: its components, how a request flows
through them, how data and content are modeled, and how to extend it.

## Overview and goals

- **Single user, local.** It runs on the learner's machine; there are no accounts and no
  multi-tenancy.
- **Server-rendered.** HTML comes from Jinja2 templates, and HTMX swaps in fragments for the
  interactive parts. There is no SPA and no frontend build step.
- **Content as files.** Courses live in `content/` as Markdown, TOML and source files.
  Content is versioned with git and validated by the test suite; it never lives in the database.
- **Real tests.** Exercises are graded by running the chapter's actual pytest suite against the
  learner's code.

## Components

```
 Browser
 ├─ Jinja2 pages (base.html, index.html, chapter.html)
 ├─ HTMX 2 (hx-post / hx-get, out-of-band swaps)
 ├─ CodeMirror 5 editor (python mode)
 └─ app.js (tabs, autosave, "reset to starter")
        │  HTTP (form posts, HTML fragments)
        ▼
 FastAPI app — app/main.py: create_app()
 ├─ content.py   ── reads ──▶ content/<course>/<module>/<chapter>/
 ├─ render.py       Markdown → HTML (markdown-it-py + Pygments)
 ├─ quiz.py         grades quiz answers
 ├─ languages.py    per-language config, including which runner to use
 ├─ runner.py    ── spawns ──▶ pytest in a temporary directory
 ├─ progress.py  ── reads/writes ──▶ progress.db (SQLite)
 └─ legacy_ids.py   old Spanish slugs → current ones (progress import, old URLs)
```

Front-end libraries (HTMX 2.0.4 and CodeMirror 5.65.18) are vendored in `app/static/vendor/`
(pinned versions and licenses; see its README), next to the app's own `app.css` and `app.js`.
The only external resource is the Google Fonts stylesheet, and the CSS falls back to system
fonts without it, so the app works offline.

## Modules

### `app/main.py`: app factory and routes
`create_app(content_root, db_path, reload_content, legacy_db_path)` builds the FastAPI app.
The parameters exist so tests can inject a content folder and temporary databases. It:

- mounts `/static` and configures Jinja2. It registers the `markdown` filters, the pass
  threshold as a global (`THRESHOLD`), and a cache-busting version `V` taken from the newest
  static file's mtime.
- creates the `Progress` store (path from `db_path`, else `$COURSE_DB`, else `progress.db`) and
  imports the legacy `progreso.db` if there is one (see [Data model](#data-model)).
- reloads the content on every request when `reload_content=True` (the default), so edits
  show up immediately.
- defines the routes (see [HTTP routes](#http-routes)). Every full page sets a `course` cookie
  that remembers the last course viewed. The course tabs in `base.html` only render when there
  is more than one course.

The module-level `app = create_app()` is what uvicorn serves.

### `app/content.py`: content model
Dataclasses `Course` → `Module` → `Chapter`, plus `Question` for quiz questions.
`load_courses()` scans `content/`:
- A directory is a course if it has `course.toml`, a module if it has `module.toml`, and a
  chapter if it has `lesson.md`.
- Courses are sorted by `order`; modules and chapters by directory name, so the `NN-` prefixes
  set the order.

`Chapter` lazily reads its files (`lesson()`, `questions()`, `starter_code()`, `solution()`)
and exposes `support_files()`: everything in the chapter folder that the tests need. That
includes files and folders, but excludes the private files, hidden entries and `__pycache__`.

### `app/languages.py`: language settings
A frozen `Language` dataclass holds what differs between languages:
- the exercise, test and solution file names
- the CodeMirror mode and Pygments lexer
- tabs vs. spaces
- a hint for where the instructions live
- `run`: the runner function

`private_files` lists the files that are **never** copied next to the tests: the lesson,
the quiz, the starter code and the solution. Today there is a single instance, `PYTHON`,
registered in `LANGUAGES`.

### `app/runner.py`: running exercise tests
`run_tests` takes the learner's code and the chapter's support files and returns a
`RunResult` (a list of `TestResult`, plus an optional global error and the raw output):

1. Write the code as `exercise.py` in a fresh temp dir and copy the support files there.
2. Add an empty `pytest.ini` so the project's own config is ignored.
3. Run `python -m pytest --junitxml=…` as a subprocess, using the same interpreter, with
   colors disabled and a **15 s** timeout.
4. Parse the JUnit XML per test and clean the tracebacks, keeping the learner's frames.
   `NotImplementedError("TODO")` is reported as *pending* rather than as a failure.

### `app/progress.py`: progress store
`Progress` wraps SQLite with short-lived connections. `Status` is an immutable view of one
chapter (`complete` means read, quiz passed and tests passed). Writes go through `_upsert`.
`record_quiz` and `record_tests` never move backwards: the best score is kept, and a
passed step stays passed.

### `app/quiz.py`: grading
`grade(questions, chosen)` returns a `QuizResult` with a per-question breakdown, a
score and `passed` (score ≥ `PASS_THRESHOLD`, which is 0.8).

### `app/render.py`: Markdown rendering
markdown-it-py with Pygments highlighting for fenced code blocks. External links open in a new
tab. `code_html()` renders the reference solution, and `pygments_css()` is served at
`/pygments.css`.

### `app/legacy_ids.py`: old slugs
Until November 2026 the course used Spanish module and chapter slugs (`01-fundamentos/…`).
`MODULES` and `CHAPTERS` map them to the current English slugs; `translate_id()` and
`translate_path()` are used by the progress import and the redirects for old URLs.

## HTTP routes

`{ch}` below is short for `{course}/{module}/{chapter}`.

| Method | Path | Returns | Effect on progress |
|---|---|---|---|
| GET | `/` | redirect to the course in the `course` cookie, or the first course | none |
| GET | `/{course}` | course index page (modules, chapter status, "continue" link) | none |
| GET | `/c/{ch}` | chapter page with the lesson, quiz and editor tabs (301 to the new URL for an old Spanish slug) | none |
| POST | `/c/{ch}/read` | `_read.html` fragment | toggles `read` |
| POST | `/c/{ch}/{quiz\|tests}/solved` | `_solved.html` fragment | toggles `quiz_ok` / `tests_ok` |
| POST | `/c/{ch}/quiz` | `_quiz.html` fragment with the graded answers | `record_quiz` |
| POST | `/c/{ch}/code` | 204 (autosave) | saves `code` |
| POST | `/c/{ch}/tests` | `_tests_result.html` fragment | `record_tests` (code and pass state) |
| GET | `/c/{ch}/solution` | highlighted solution, or a notice if the tests haven't passed | none |
| GET | `/c/{ch}/starter` | starter code as plain text ("reset" button) | none |
| GET | `/c/{module}/{chapter}` | 301 to `/c/python/…` (pre-multi-course URLs, old slugs translated) | none |
| GET | `/pygments.css` | highlighting stylesheet | none |

The solution gate is enforced on the server, not just hidden in the UI. OpenAPI docs are
disabled (`docs_url=None`), since the endpoints return HTML rather than JSON.

## Request flows

### Running the tests
1. The editor form posts with `hx-post="/c/{ch}/tests"`. `app.js` injects the current editor
   contents as `code`. HTMX shows a spinner and disables the button.
2. `run_tests` (the route) looks up the chapter and calls
   `c.language.run(code, c.support_files())` through `run_in_threadpool`, so the blocking
   subprocess doesn't stall the event loop.
3. The runner builds the temp dir, runs the suite, parses the results and deletes the temp dir.
4. `progress.record_tests` stores the code and the pass state.
5. The response renders `_tests_result.html` into `#tests-result`. The same response
   carries out-of-band swaps (`hx-swap-oob`) that update the tab's check mark and the
   "mark as solved" button.

### Submitting the quiz
The form posts fields `q0…qN` holding option indexes. The server grades them, stores the best
score, and returns the graded quiz (correct/incorrect answers with explanations) plus an
out-of-band update of the quiz tab mark.

### Autosave
`app.js` debounces editor changes (800 ms) and posts them to `/code`. When rendering a
chapter page, the server fills the editor with the saved code if there is any, or the starter
code otherwise.

## Data model

A single table, created with `CREATE TABLE IF NOT EXISTS` on **every** connection, so deleting
`progress.db` while the app is running is harmless:

```sql
CREATE TABLE chapters (
    id        TEXT PRIMARY KEY,               -- "course/module/chapter", e.g. "python/02-idiomatic/01-comprehensions"
    read      INTEGER NOT NULL DEFAULT 0,     -- lesson read
    quiz_ok   INTEGER NOT NULL DEFAULT 0,     -- quiz passed or marked as solved
    quiz_best REAL    NOT NULL DEFAULT 0,     -- best quiz score (0..1)
    tests_ok  INTEGER NOT NULL DEFAULT 0,     -- tests passed or marked as solved
    code      TEXT,                           -- learner's latest code
    updated   TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

- **Legacy import.** Older installs stored progress in `progreso.db` (table `capitulos`, Spanish
  column names and slugs, and before multi-course support, ids without the course prefix). On
  startup, `Progress.import_legacy()` copies those rows into `progress.db`, translating the ids
  through `legacy_ids`. It only runs while `progress.db` is empty and never modifies the old
  file, so it is safe on every start.
- "Mark as solved" writes the **same** columns as actually passing, so the database cannot tell
  the two apart. That is a known limitation (see the roadmap in the README).

## Content model

```
content/<course>/course.toml               title, language = "python", order, description
content/<course>/NN-module/module.toml     title, description
content/<course>/NN-module/NN-chapter/
    lesson.md         first line "# Title"; the rest is the lesson body
    quiz.toml         [[questions]] text, options = [...], correct = <0-based index>, explanation
    exercise / tests / solution files, named by the course's Language
                      (Python: exercise.py, test_exercise.py, solution.py)
    support files     data (CSV…), helper modules, folders such as templates/
```

Conventions that the content tests enforce or rely on:

- **The starter code must fail every test, and the solution must pass them all.**
  `tests/test_content.py` runs both through the real runner.
- Python starters raise `NotImplementedError("TODO")`, which the UI shows as *pending*.
- Tests import the learner's code from the `exercise` module.
- Tests must not depend on the network. For example, the finance chapters ship a synthetic
  `prices.csv`, and matplotlib tests select the `Agg` backend before importing `pyplot`.
- Where it matters, tests compute their reference values independently of the library being
  taught (e.g. with `csv`/`statistics` instead of pandas).
- Lessons are plain Markdown: there is no LaTeX rendering, so formulas go in `text` code blocks.

## Extending

- **New chapter**: add a numbered folder with the files above, then run
  `uv run pytest tests -k <chapter-slug>`.
- **New module**: add a numbered folder with `module.toml`.
- **New course**: add `content/<slug>/course.toml` with an existing `language`; with two or
  more courses, each one shows up as a tab.
- **New language**:
  1. Write a runner in `runner.py` returning `RunResult`.
  2. Add a `Language` instance to `LANGUAGES`.
  3. Make sure `chapter.html` can load its CodeMirror mode (the mode name comes from
     `editor_mode`).
- **Renaming a slug**: add the old → new pair to `app/legacy_ids.py` so saved progress and old
  links keep working.

## Testing

| File | Covers |
|---|---|
| `tests/test_app.py` | Routes via FastAPI's `TestClient`: course tabs, cookie redirect, legacy 301s, legacy progress import, per-course progress, mark as solved, solution gate, no CDN dependencies |
| `tests/test_runner.py` | The pytest runner: pass/fail, pending, syntax errors, cleaned tracebacks, timeouts, support files and folders |
| `tests/test_quiz.py` | Quiz grading and the pass threshold |
| `tests/test_content.py` | Every chapter of every course: files present, lesson renders, quiz valid, solution passes, starter fails |

## Security and limitations

- **Learner code runs unsandboxed** as the current OS user, limited only by a timeout. This is
  acceptable for a local, single-user tool; **do not expose the app on a network.**
- There is no concurrency limit on test runs: each request spawns a subprocess.
- Single user: progress is global to the database file.
- Content is re-read from disk on every request. That is convenient while writing content and
  fine at this scale; `create_app(reload_content=False)` caches it instead.
