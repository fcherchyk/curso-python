# Curso de refresco de Python

Para quien ya programa (y programó en Python) y quiere ponerse al día con sintaxis moderna,
código idiomático y el ecosistema actual. **Formato:** cada día tiene una lección corta y
ejercicios con tests que tenés que hacer pasar.

## App web (nuevo)

El curso se está migrando a una app web local: cada capítulo tiene **lectura → cuestionario →
ejercicio de código** que tiene que pasar los tests (se corren con pytest en tu máquina).

```bash
uv sync
uv run uvicorn app.main:app --reload     # abrí http://localhost:8000
```

- Cada paso (lectura, quiz, código) tiene un botón **Marcar como resuelto** para saltearlo:
  cuenta igual que aprobarlo y, en el código, habilita la solución de referencia.
- El progreso (qué leíste, quizzes aprobados, tests en verde y tu código) se guarda en
  `progreso.db` (SQLite, ignorado por git). Borralo para empezar de cero.
- El contenido vive en `contenido/NN-modulo/NN-capitulo/` (`leccion.md`, `quiz.toml`,
  `ejercicio.py`, `test_ejercicio.py`, `solucion.py`). La app lo relee en cada request.
- `uv run pytest tests` valida la app y **todo** el contenido: cada solución pasa sus tests,
  cada ejercicio inicial no pasa y cada quiz está bien formado.

Temario previsto: fundamentos rápidos → Python idiomático → iteradores → funciones avanzadas →
modelado → Python moderno → herramientas → stdlib → algoritmos → concurrencia → Pydantic →
FastAPI → SQLAlchemy 2.0 → Django → pandas → proyecto integrador. Hoy están cargados los
módulos **01 · Fundamentos rápidos**, **02 · Python idiomático**, **03 · Iteradores y
generadores** y **04 · Funciones avanzadas** (22 capítulos).

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
