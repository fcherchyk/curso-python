# curso-python

A local web app for learning **Python**, in the spirit of [coddy.tech](https://coddy.tech/)
but without XP, streaks or animations. Every chapter has three steps:

**reading → quiz → coding exercise**, where the exercise is checked by real pytest tests
running on your machine.

The course content is written in Spanish; the code identifiers and file names are Spanish too
(`contenido` = content, `leccion` = lesson, `ejercicio` = exercise, `solucion` = solution,
`progreso` = progress).

## Course

**Python**: 75 chapters in 14 modules, aimed at people who already program. It covers
fundamentals, idiomatic Python, iterators and generators, advanced functions, data modeling,
modern Python, and tooling (uv, ruff, mypy, pytest, mutation testing). Then come the web
frameworks **Flask**, **FastAPI** (with Pydantic, async and SQLAlchemy 2.0) and **Django** (ORM,
forms, generic views, admin, DRF, auth). After those, data work with **NumPy**, **pandas** and
**matplotlib**, and **Python for finance** (returns, risk, Sharpe/beta, portfolios, efficient
frontier, backtesting) on reproducible synthetic prices. Coming next: stdlib, algorithms,
concurrency and a capstone project.

## Features

- Lessons written in Markdown, with syntax highlighting.
- 5-question multiple-choice quizzes with explanations; passing is ≥ 80 %.
- In-browser code editor (CodeMirror) whose contents are autosaved.
- Tests run locally in a temporary directory, with a timeout, and results are shown per test.
- **Mark as solved** on every step, to skip something and keep going; it counts as passed.
- The reference solution unlocks once the exercise's tests pass.
- Progress is stored in a local SQLite file. The app supports several courses (shown as tabs
  when there is more than one), though today there is only the Python course.

## Getting started

Requirements: [uv](https://docs.astral.sh/uv/) (`brew install uv` or
`curl -LsSf https://astral.sh/uv/install.sh | sh`). Nothing else is needed: no database server,
no `.env` file, no Docker and no Node.

```bash
uv sync                                   # installs Python 3.13 if needed and all dependencies
uv run uvicorn app.main:app --reload      # then open http://localhost:8000
```

Progress (read lessons, quiz scores, passed exercises and your code) is saved in `progreso.db`,
which git ignores. Delete it to start over, or point `CURSO_DB=/path/to/file.db` at another file.

## Running the tests

```bash
uv run pytest tests                        # the app and ALL course content
uv run ruff check app tests contenido      # lint
```

`tests/` checks the web app, the test runner and quiz grading. It also validates every chapter
of the course: all files are present, the lesson renders, the quiz is well formed, **the
reference solution passes** its tests and **the starter code fails** every one of them.

## Project layout

```
curso-python/
├── app/                      # FastAPI web app
│   ├── main.py               # app factory (crear_app) and HTTP routes
│   ├── contenido.py          # loads courses/modules/chapters from contenido/
│   ├── lenguajes.py          # per-language settings (Python)
│   ├── runner.py             # runs exercise tests with pytest in a temp dir
│   ├── progreso.py           # progress store (SQLite)
│   ├── quiz.py               # quiz grading
│   ├── render.py             # Markdown → HTML with Pygments
│   ├── templates/            # Jinja2 pages and HTMX fragments (_*.html)
│   └── static/               # app.css, app.js
├── contenido/                # course content (see below)
│   └── python/
├── tests/                    # tests for the app and the content
├── docs/ARCHITECTURE.md      # how it all fits together
├── semana1/, soluciones/     # legacy terminal-based exercises
└── pyproject.toml            # dependencies, pytest, ruff and mypy config
```

## Adding content

Content is just files; the app picks up changes on the next request.

```
contenido/<course>/
  curso.toml                  # titulo, lenguaje (python), orden, descripcion
  NN-module/
    modulo.toml               # titulo, descripcion
    NN-chapter/
      leccion.md              # first line "# Title" is the chapter title
      quiz.toml               # [[preguntas]] texto, opciones, correcta (0-based), explicacion
      ejercicio.py            # starter code shown in the editor
      test_ejercicio.py       # the exercise's tests
      solucion.py             # reference solution
      ...                     # optional support files or folders needed by the tests
```

Then run `uv run pytest tests -k <chapter>`: the solution must pass and the starter code must
fail. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#content-model) for the conventions.

## Legacy material

`semana1/` (with solutions in `soluciones/`) is the original format: daily lessons and
exercises solved in your editor and checked from the terminal, e.g.
`uv run pytest semana1/dia1_idiomatico`. It is still runnable, but the web app supersedes it.

## License

[MIT](LICENSE) © 2026 Federico Cherchyk
