# Curso de refresco de Python

Para quien ya programa (y programó en Python) y quiere ponerse al día con sintaxis moderna,
código idiomático y el ecosistema actual. **Formato:** cada día tiene una lección corta y
ejercicios con tests que tenés que hacer pasar.

## App web

Una app web local con **dos cursos en solapas: Python y Go**. Cada capítulo tiene
**lectura → cuestionario → ejercicio de código** que tiene que pasar los tests, que corren en
tu máquina con pytest o con `go test`.

```bash
uv sync
brew install go                          # solo para el curso de Go
uv run uvicorn app.main:app --reload     # abrí http://localhost:8000
```

- El progreso de los dos cursos (lecturas, quizzes, tests y tu código) se guarda en
  `progreso.db` (SQLite, ignorado por git). Borralo para empezar de cero.
- Cada paso tiene **Marcar como resuelto** para saltearlo.
- El contenido vive en `contenido/<curso>/NN-modulo/NN-capitulo/`:
  - `leccion.md` y `quiz.toml`;
  - Python: `ejercicio.py`, `test_ejercicio.py` y `solucion.py`;
  - Go: `ejercicio.go`, `ejercicio_test.go` y `solucion.go`.
  Cada curso tiene su `curso.toml` (título, lenguaje, orden).
- `uv run pytest tests` valida la app y **todo** el contenido de los dos cursos: cada solución
  pasa sus tests, cada ejercicio inicial no pasa y cada quiz está bien formado.

**Python** (37 capítulos): fundamentos, idiomático, iteradores, funciones avanzadas, modelado,
Python moderno y herramientas. Siguen stdlib, algoritmos, concurrencia y frameworks
(Pydantic, FastAPI, SQLAlchemy, Django, pandas).

**Go** (12 capítulos): fundamentos rápidos y Go idiomático. Siguen tipos y métodos,
interfaces, errores, genéricos, concurrencia, testing, stdlib, HTTP (net/http, chi/Gin),
datos (database/sql, pgx, sqlc), GORM y un proyecto integrador.

## Puesta en marcha (una sola vez)

Necesitás [uv](https://docs.astral.sh/uv/). En Mac: `brew install uv`, o
`curl -LsSf https://astral.sh/uv/install.sh | sh`.

```bash
cd curso-python
uv sync                 # descarga Python 3.13 si hace falta, crea .venv e instala pytest/ruff/mypy
uv run pytest           # vas a ver todo en rojo: es el punto de partida
```

En PyCharm o VS Code, elegí como intérprete `curso-python/.venv/bin/python`.

## Cómo se trabaja cada día

1. Leé `semana1/diaN_.../leccion.md` (15–20 min).
2. Abrí `ejercicios.py`: cada función tiene docstring con la consigna, ejemplos y una pista.
   Reemplazá el `raise NotImplementedError("TODO")`.
3. Corré los tests de ese día hasta que estén en verde:

```bash
uv run pytest semana1/dia1_idiomatico          # un día
uv run pytest semana1/dia1_idiomatico -x       # parar en el primer fallo
uv run pytest -k construir_url                 # un ejercicio
uv run pytest --lf                             # solo los que fallaron la última vez
```

4. Recién cuando pasen, compará con `soluciones/`. Muchas veces hay más de una forma
   idiomática; lo importante es entender por qué la solución de referencia elige esa.
5. Si te queda tiempo, hacé el **Reto extra** al final de cada lección.

## Plan general

| Semana | Tema                                                     | Estado     |
|--------|----------------------------------------------------------|------------|
| 1      | Sintaxis moderna e idiomática + herramientas (uv, ruff, mypy) | ✅ lista |
| 2      | Estructuras de datos y algoritmos (collections, heapq, bisect, patrones NeetCode) | pendiente |
| 3      | Desarrollo serio: OOP avanzada, pytest a fondo, asyncio, empaquetado | pendiente |
| 4      | Frameworks: FastAPI + Pydantic, SQLAlchemy 2.0, pandas, httpx + proyecto final | pendiente |

Detalle y checklist de la semana 1: [semana1/README.md](semana1/README.md).

## Estructura

```
curso-python/
├── pyproject.toml          # config de pytest, ruff y mypy
├── semana1/
│   ├── README.md           # checklist
│   └── diaN_tema/
│       ├── leccion.md
│       ├── ejercicios.py   # ← acá trabajás
│       └── test_ejercicios.py
└── soluciones/semana1/     # no espiar antes de tiempo 🙂
```

**Tip:** hacé `git init` y un commit por día. Así ves tu progreso y podés volver atrás.
