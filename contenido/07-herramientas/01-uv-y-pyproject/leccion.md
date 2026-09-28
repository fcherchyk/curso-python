# uv y pyproject.toml

Durante años, armar un proyecto Python implicaba combinar varias herramientas: `pyenv` para
la versión de Python, `venv` o `virtualenv` para el entorno, `pip` para instalar,
`pip-tools` o `poetry` para fijar versiones y `pipx` para las herramientas globales. **uv**
(de Astral, los creadores de ruff) reemplaza todo eso con un solo binario, escrito en Rust
y entre 10 y 100 veces más rápido. Hoy es el estándar de facto para proyectos nuevos, y
es el que usa este curso.

## `pyproject.toml`: el archivo central

Todo proyecto moderno se describe en un único archivo, `pyproject.toml` (PEP 518/621):

```toml
[project]
name = "curso-python"
version = "0.1.0"
description = "Curso de Python"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "httpx[http2]>=0.27",           # [extras]: dependencias opcionales del paquete
    "pydantic>=2,<3",
]

[project.scripts]
analizar = "mi_paquete.cli:main"     # crea el comando `analizar` al instalar

[dependency-groups]
dev = ["pytest>=8", "ruff>=0.6", "mypy>=1.11"]     # solo para desarrollo

[tool.ruff]                          # cada herramienta lee su sección [tool.X]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- **`[project]`**: metadatos estándar. `dependencies` son las dependencias **de ejecución**,
  con restricciones de versión (`>=`, `<`, `~=`, `==`).
- **`[dependency-groups]`** (PEP 735): dependencias de desarrollo (tests, linters) que no
  viajan con tu paquete.
- **`[tool.*]`**: configuración de cada herramienta. Así desaparecen `setup.cfg`, `.flake8`,
  `pytest.ini`, `mypy.ini`…

## `uv.lock`: versiones exactas y reproducibles

`pyproject.toml` dice **qué rangos** aceptás (`fastapi>=0.115`). `uv.lock` registra **qué
versiones exactas** se instalaron, incluidas todas las dependencias transitivas y sus hashes.
Así, cualquier persona (o el CI) que haga `uv sync` obtiene exactamente el mismo entorno.

**`uv.lock` va al control de versiones.** No se edita a mano.

## Los comandos que vas a usar

```bash
uv init mi-proyecto            # crea pyproject.toml, .python-version, README y main.py
uv add fastapi                 # agrega a dependencies, instala y actualiza el lock
uv add --dev pytest ruff       # al grupo dev
uv remove httpx
uv sync                        # deja el .venv exactamente como dice el lock
uv lock --upgrade-package fastapi   # actualiza una dependencia dentro de su rango

uv run pytest                  # ejecuta DENTRO del entorno del proyecto
uv run python -m mi_paquete
uv run uvicorn app.main:app --reload

uv python install 3.13         # instala versiones de Python (chau pyenv)
uv python pin 3.13             # fija la versión del proyecto en .python-version

uvx ruff check                 # corre una herramienta sin instalarla (como pipx run)
uv tool install ruff           # instala una herramienta global
```

`uv run` es la clave: asegura que el entorno esté sincronizado y ejecuta el comando con él,
**sin activar** el virtualenv a mano. Si preferís activarlo, sigue ahí: `.venv/bin/activate`.

## Scripts sueltos con dependencias (PEP 723)

Para un script de un solo archivo no hace falta un proyecto: las dependencias se declaran en
un comentario especial y `uv run` crea un entorno temporal:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["httpx", "rich"]
# ///
import httpx, rich
...
```

```bash
uv run script.py
```

## Especificadores de versión

| Especificador    | Significa                                         |
|------------------|---------------------------------------------------|
| `>=2.0`          | 2.0 o mayor                                       |
| `>=2,<3`         | cualquier 2.x                                     |
| `~=2.4`          | compatible: `>=2.4, <3.0`                         |
| `~=2.4.1`        | `>=2.4.1, <2.5`                                   |
| `==2.4.*`        | cualquier 2.4.x                                   |

Para **aplicaciones**, rangos amplios en `pyproject.toml` más el lock. Para **librerías**, que
otros van a instalar, solo rangos amplios: nunca fijes versiones exactas, porque generan
conflictos en los proyectos que te usan.

## Estructura de proyecto recomendada

```
mi-proyecto/
├── pyproject.toml
├── uv.lock
├── .python-version
├── src/
│   └── mi_paquete/        # layout "src": evita importar el código sin instalarlo
│       ├── __init__.py
│       └── cli.py
└── tests/
    └── test_cli.py
```

`uv init --package` o `uv init --lib` crean este layout.

## Resumen

- `pyproject.toml` describe el proyecto: dependencias, grupos de desarrollo y configuración de
  herramientas.
- `uv.lock` fija las versiones exactas y va a git.
- `uv add`, `uv sync`, `uv run`; `uv python install/pin`; `uvx` para herramientas sueltas.
- Scripts de un archivo con dependencias inline (PEP 723).
- Aplicaciones: rangos más lock. Librerías: solo rangos.

## Ejercicio

Funciones que leen un `pyproject.toml` (con `tomllib`) y extraen información: dependencias
sin versión, el Python requerido y los grupos de dependencias.

**Para profundizar:** [documentación de uv](https://docs.astral.sh/uv/),
[Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/),
[PEP 723](https://peps.python.org/pep-0723/).
