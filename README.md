# curso-python

A local web app for learning **Python**, in the spirit of [coddy.tech](https://coddy.tech/)
but without XP, streaks or animations. Every chapter has three steps:

**reading → quiz → coding exercise**, where the exercise is checked by real pytest tests
running on your machine.

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

Progress (read lessons, quiz scores, passed exercises and your code) is saved in `progress.db`,
which git ignores. Delete it to start over, or point `COURSE_DB=/path/to/file.db` at another
file. If you used the app when it was still in Spanish, your old `progreso.db` is imported
automatically the first time the app starts with an empty `progress.db`.

## Running the tests

```bash
uv run pytest tests                        # the app and ALL course content
uv run ruff check app tests content        # lint
```

`tests/` checks the web app, the test runner and quiz grading. It also validates every chapter
of the course: all files are present, the lesson renders, the quiz is well formed, **the
reference solution passes** its tests and **the starter code fails** every one of them.

## Project layout

```
curso-python/
├── app/                      # FastAPI web app
│   ├── main.py               # app factory (create_app) and HTTP routes
│   ├── content.py            # loads courses/modules/chapters from content/
│   ├── languages.py          # per-language settings (Python)
│   ├── runner.py             # runs exercise tests with pytest in a temp dir
│   ├── progress.py           # progress store (SQLite)
│   ├── quiz.py               # quiz grading
│   ├── render.py             # Markdown → HTML with Pygments
│   ├── legacy_ids.py         # old Spanish slugs → current ones (progress import, old URLs)
│   ├── templates/            # Jinja2 pages and HTMX fragments (_*.html)
│   └── static/               # app.css, app.js, vendored HTMX and CodeMirror
├── content/                  # course content (see below)
│   └── python/
├── tests/                    # tests for the app and the content
├── docs/ARCHITECTURE.md      # how it all fits together
├── week1/, solutions/        # legacy terminal-based exercises
└── pyproject.toml            # dependencies, pytest, ruff and mypy config
```

## Adding content

Content is just files; the app picks up changes on the next request.

```
content/<course>/
  course.toml                 # title, language (python), order, description
  NN-module/
    module.toml               # title, description
    NN-chapter/
      lesson.md               # first line "# Title" is the chapter title
      quiz.toml               # [[questions]] text, options, correct (0-based), explanation
      exercise.py             # starter code shown in the editor
      test_exercise.py        # the exercise's tests (import from `exercise`)
      solution.py             # reference solution
      ...                     # optional support files or folders needed by the tests
```

Then run `uv run pytest tests -k <chapter>`: the solution must pass and the starter code must
fail. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#content-model) for the conventions.

## Roadmap

Planned features, roughly in order. None of them is implemented yet.

### 1. Learner dashboard: progress, quality and engagement metrics
A dashboard page per course that turns the stored history into metrics:

- **Progress**: chapters and modules completed, completion per step (reading / quiz / code),
  what is left, and progress over time.
- **Quality**: first-try pass rate for quizzes and exercises, average and best quiz scores,
  attempts needed to solve, how many steps were *marked as solved* instead of actually passed
  (today the database can't tell these apart, so this needs its own flag).
- **Engagement**: active days, time between sessions, last activity, chapters started but not
  finished. No streaks or gamification, just information.

Depends on the attempt history below as its data source.

### 2. Attempt history
Record every attempt instead of only the latest state:

- **Attempt counts** for every quiz and exercise, both for solved ones and for those that were
  *tried but are still unsolved*, visible on the chapter page and in the course index.
- **Code version history**: every test run stores the submitted code and its result (tests
  passed / failed, error). In the code tab you can browse earlier versions, see what each one
  scored, diff two versions, and restore one into the editor.

Sketch: new tables `quiz_attempts(chapter_id, at, score, passed)` and
`code_attempts(chapter_id, at, code, passed, passed_count, total)`, written by the existing
`/quiz` and `/tests` routes.

### 3. Content search
Search across the course, which the app can't do today: lesson text, quiz questions and
explanations, and exercise instructions. Results link to the chapter (and section) where the
match is, with a highlighted snippet. Sketch: an SQLite FTS5 index built from `content/` at
startup (and rebuilt when content changes), plus a search box in the top bar.

### 4. Failed-question review
Store the result of **each question** in every quiz attempt, not just the overall score, and
link every question to the lesson section it is about (e.g. a `section = "mutable-defaults"`
key in `quiz.toml` pointing at a heading anchor in `lesson.md`). After a failed quiz the app
builds a **review sheet**: the questions you missed, and links to exactly the parts of the
lesson to reread before retaking it. Missed questions also feed the quality metrics of the
dashboard.

### 5. Hints for code exercises
Optional hints per exercise (e.g. `[[hints]]` in a `hints.toml` next to the exercise), hidden
by default in the code tab and **revealed one at a time on demand** when you are stuck, going
from a gentle nudge to something close to the answer. How many hints were revealed is recorded
with the attempt, so the dashboard can tell "solved unaided" from "solved with hints".

## Legacy material

`week1/` (with solutions in `solutions/`) is the original format: daily lessons and
exercises solved in your editor and checked from the terminal, e.g.
`uv run pytest week1/day1_idiomatic`. It is still runnable, but the web app supersedes it.

## License

[MIT](LICENSE) © 2026 Federico Cherchyk
