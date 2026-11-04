# Architecture

This document describes how the course app is built: its components, how a request flows
through them, how data and content are modeled, and how to extend it.

Identifiers in the code are in Spanish. The ones that come up most often are `curso` (course),
`modulo` (module), `capitulo` (chapter), `leccion` (lesson), `pregunta` (question), `ejercicio`
(exercise), `solucion` (solution), `progreso` (progress), `leido` (read), `resuelto` (solved),
`correr` (run) and `lenguaje` (language).

## Overview and goals

- **Single user, local.** It runs on the learner's machine; there are no accounts and no
  multi-tenancy.
- **Server-rendered.** HTML comes from Jinja2 templates, and HTMX swaps in fragments for the
  interactive parts. There is no SPA and no frontend build step.
- **Content as files.** Courses live in `contenido/` as Markdown, TOML and source files.
  Content is versioned with git and validated by the test suite; it never lives in the database.
- **Real tests.** Exercises are graded by running the chapter's actual pytest suite against the
  learner's code.

## Components

```
 Browser
 ├─ Jinja2 pages (base.html, index.html, capitulo.html)
 ├─ HTMX 2 (hx-post / hx-get, out-of-band swaps)
 ├─ CodeMirror 5 editor (python mode)
 └─ app.js (tabs, autosave, "reset to starter code")
        │  HTTP (form posts, HTML fragments)
        ▼
 FastAPI app — app/main.py: crear_app()
 ├─ contenido.py  ── reads ──▶ contenido/<course>/<module>/<chapter>/
 ├─ render.py       Markdown → HTML (markdown-it-py + Pygments)
 ├─ quiz.py         grades quiz answers
 ├─ lenguajes.py    per-language config, including which runner to use
 ├─ runner.py   ── spawns ──▶ pytest in a temporary directory
 └─ progreso.py ── reads/writes ──▶ progreso.db (SQLite)
```

Front-end libraries (HTMX, CodeMirror) are loaded from CDNs; the only local static files are
`app/static/app.css` and `app/static/app.js`.

## Modules

### `app/main.py`: app factory and routes
`crear_app(raiz_contenido, ruta_db, recargar_contenido)` builds the FastAPI app. The
parameters exist so tests can inject a content folder and a temporary database. It:

- mounts `/static` and configures Jinja2. It registers the `markdown` filters, the pass
  threshold as a global, and a cache-busting version `V` taken from the newest static file's
  mtime.
- creates the `Progreso` store (path from `ruta_db`, else `$CURSO_DB`, else `progreso.db`) and
  runs the one-off id migration.
- reloads the content on every request when `recargar_contenido=True` (the default), so edits
  show up immediately.
- defines the routes (see [HTTP routes](#http-routes)). Every full page sets a `curso` cookie
  that remembers the last course viewed. The course tabs in `base.html` only render when there
  is more than one course.

The module-level `app = crear_app()` is what uvicorn serves.

### `app/contenido.py`: content model
Dataclasses `Curso` → `Modulo` → `Capitulo`, plus `Pregunta` for quiz questions.
`cargar_cursos()` scans `contenido/`:
- A directory is a course if it has `curso.toml`, a module if it has `modulo.toml`, and a
  chapter if it has `leccion.md`.
- Courses are sorted by `orden`; modules and chapters by directory name, so the `NN-` prefixes
  set the order.

`Capitulo` lazily reads its files (`leccion()`, `preguntas()`, `codigo_inicial()`, `solucion()`)
and exposes `archivos_de_soporte()`: everything in the chapter folder that the tests need. That
includes files and folders, but excludes the private files, hidden entries and `__pycache__`.

### `app/lenguajes.py`: language settings
A frozen `Lenguaje` dataclass holds what differs between languages:
- the exercise, test and solution file names
- the CodeMirror mode and Pygments lexer
- tabs vs. spaces
- a hint for where the instructions live
- `correr`: the runner function

`archivos_privados` lists the files that are **never** copied next to the tests: the lesson,
the quiz, the starter code and the solution. Today there is a single instance, `PYTHON`,
registered in `LENGUAJES`.

### `app/runner.py`: running exercise tests
`correr_tests` takes the learner's code and the chapter's support files and returns a
`ResultadoEjecucion` (a list of `ResultadoTest`, plus an optional global error and the raw
output):

1. Write the code as `ejercicio.py` in a fresh temp dir and copy the support files there.
2. Add an empty `pytest.ini` so the project's own config is ignored.
3. Run `python -m pytest --junitxml=…` as a subprocess, using the same interpreter, with
   colors disabled and a **15 s** timeout.
4. Parse the JUnit XML per test and clean the tracebacks, keeping the learner's frames.
   `NotImplementedError("TODO")` is reported as *pending* rather than as a failure.

### `app/progreso.py`: progress store
`Progreso` wraps SQLite with short-lived connections. `Estado` is an immutable view of one
chapter (`completo` means read, quiz passed and tests passed). Writes go through `_upsert`.
`registrar_quiz` and `registrar_tests` never move backwards: the best score is kept, and a
passed step stays passed.

### `app/quiz.py`: grading
`corregir(preguntas, elegidas)` returns a `ResultadoQuiz` with a per-question breakdown, a
score and `aprobado` (score ≥ `UMBRAL_APROBACION`, which is 0.8).

### `app/render.py`: Markdown rendering
markdown-it-py with Pygments highlighting for fenced code blocks. External links open in a new
tab. `codigo_html()` renders the reference solution, and `css_pygments()` is served at
`/pygments.css`.

## HTTP routes

`{cap}` below is short for `{curso}/{modulo}/{cap}`.

| Method | Path | Returns | Effect on progress |
|---|---|---|---|
| GET | `/` | redirect to the course in the `curso` cookie, or the first course | none |
| GET | `/{curso}` | course index page (modules, chapter status, "continue" link) | none |
| GET | `/c/{cap}` | chapter page with the lesson, quiz and editor tabs | none |
| POST | `/c/{cap}/leido` | `_leido.html` fragment | toggles `leido` |
| POST | `/c/{cap}/{quiz\|tests}/resuelto` | `_resuelto.html` fragment | toggles `quiz_ok` / `tests_ok` |
| POST | `/c/{cap}/quiz` | `_quiz.html` fragment with the graded answers | `registrar_quiz` |
| POST | `/c/{cap}/codigo` | 204 (autosave) | saves `codigo` |
| POST | `/c/{cap}/tests` | `_tests_resultado.html` fragment | `registrar_tests` (code and pass state) |
| GET | `/c/{cap}/solucion` | highlighted solution, or a notice if the tests haven't passed | none |
| GET | `/c/{cap}/inicial` | starter code as plain text ("reset" button) | none |
| GET | `/c/{modulo}/{cap}` | 301 to `/c/python/{modulo}/{cap}` (pre-multi-course URLs) | none |
| GET | `/pygments.css` | highlighting stylesheet | none |

The solution gate is enforced on the server, not just hidden in the UI. OpenAPI docs are
disabled (`docs_url=None`), since the endpoints return HTML rather than JSON.

## Request flows

### Running the tests
1. The editor form posts with `hx-post="/c/{cap}/tests"`. `app.js` injects the current editor
   contents as `codigo`. HTMX shows a spinner and disables the button.
2. `ejecutar_tests` looks up the chapter and calls `c.lenguaje.correr(codigo, c.archivos_de_soporte())`
   through `run_in_threadpool`, so the blocking subprocess doesn't stall the event loop.
3. The runner builds the temp dir, runs the suite, parses the results and deletes the temp dir.
4. `progreso.registrar_tests` stores the code and the pass state.
5. The response renders `_tests_resultado.html` into `#tests-resultado`. The same response
   carries out-of-band swaps (`hx-swap-oob`) that update the tab's check mark and the
   "mark as solved" button.

### Submitting the quiz
The form posts fields `p0…pN` holding option indexes. The server grades them, stores the best
score, and returns the graded quiz (correct/incorrect answers with explanations) plus an
out-of-band update of the quiz tab mark.

### Autosave
`app.js` debounces editor changes (800 ms) and posts them to `/codigo`. When rendering a
chapter page, the server fills the editor with the saved code if there is any, or the starter
code otherwise.

## Data model

A single table, created with `CREATE TABLE IF NOT EXISTS` on **every** connection, so deleting
`progreso.db` while the app is running is harmless:

```sql
CREATE TABLE capitulos (
    id          TEXT PRIMARY KEY,               -- "course/module/chapter", e.g. "python/02-idiomatico/01-comprehensions"
    leido       INTEGER NOT NULL DEFAULT 0,     -- lesson read
    quiz_ok     INTEGER NOT NULL DEFAULT 0,     -- quiz passed or marked as solved
    quiz_mejor  REAL    NOT NULL DEFAULT 0,     -- best quiz score (0..1)
    tests_ok    INTEGER NOT NULL DEFAULT 0,     -- tests passed or marked as solved
    codigo      TEXT,                           -- learner's latest code
    actualizado TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

- Ids used to be `module/chapter` before there were several courses.
  `migrar_ids_sin_curso("python")` prefixes the old ids at startup; it is idempotent.
- "Mark as solved" writes the **same** columns as actually passing, so the database cannot tell
  the two apart. That is a known limitation.

## Content model

```
contenido/<course>/curso.toml          titulo, lenguaje = "python", orden, descripcion
contenido/<course>/NN-module/modulo.toml   titulo, descripcion
contenido/<course>/NN-module/NN-chapter/
    leccion.md        first line "# Title"; the rest is the lesson body
    quiz.toml         [[preguntas]] texto, opciones = [...], correcta = <0-based index>, explicacion
    exercise / tests / solution files, named by the course's Lenguaje
    support files     data (CSV…), helper modules, folders such as templates/
```

Conventions that the content tests enforce or rely on:

- **The starter code must fail every test, and the solution must pass them all.**
  `tests/test_contenido.py` runs both through the real runner.
- Python starters raise `NotImplementedError("TODO")`, which the UI shows as *pending*.
- Tests must not depend on the network. For example, the finance chapters ship a synthetic
  `precios.csv`, and matplotlib tests select the `Agg` backend before importing `pyplot`.
- Where it matters, tests compute their reference values independently of the library being
  taught (e.g. with `csv`/`statistics` instead of pandas).
- Lessons are plain Markdown: there is no LaTeX rendering, so formulas go in `text` code blocks.

## Extending

- **New chapter**: add a numbered folder with the files above, then run
  `uv run pytest tests -k <chapter-slug>`.
- **New module**: add a numbered folder with `modulo.toml`.
- **New course**: add `contenido/<slug>/curso.toml` with an existing `lenguaje`; with two or
  more courses, each one shows up as a tab.
- **New language**:
  1. Write a runner in `runner.py` returning `ResultadoEjecucion`.
  2. Add a `Lenguaje` instance to `LENGUAJES`.
  3. Make sure `capitulo.html` can load its CodeMirror mode (the mode name comes from
     `modo_editor`).

## Testing

| File | Covers |
|---|---|
| `tests/test_app.py` | Routes via FastAPI's `TestClient`: course tabs, cookie redirect, legacy 301s, id migration, per-course progress, mark as solved, solution gate |
| `tests/test_runner.py` | The pytest runner: pass/fail, pending, syntax errors, cleaned tracebacks, timeouts, support files and folders |
| `tests/test_quiz.py` | Quiz grading and the pass threshold |
| `tests/test_contenido.py` | Every chapter of every course: files present, lesson renders, quiz valid, solution passes, starter fails |

## Security and limitations

- **Learner code runs unsandboxed** as the current OS user, limited only by a timeout. This is
  acceptable for a local, single-user tool; **do not expose the app on a network.**
- There is no concurrency limit on test runs: each request spawns a subprocess.
- Single user: progress is global to the database file.
- Content is re-read from disk on every request. That is convenient while writing content and
  fine at this scale; `crear_app(recargar_contenido=False)` caches it instead.
- Pages need internet access to load HTMX and CodeMirror from their CDNs.
