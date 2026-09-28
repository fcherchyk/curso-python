# ruff y mypy: calidad automática

Dos herramientas se encargan de casi todo el control de calidad automático en un proyecto
Python moderno. **ruff** es un linter y formateador ultrarrápido que reemplaza a flake8, isort,
black, pyupgrade y decenas de plugins. **mypy** es el type checker que verifica que tus type
hints sean coherentes. Configurados una vez, te avisan de bugs y de código viejo antes de
ejecutar nada.

## ruff: linter

```bash
uv run ruff check                  # analiza todo el proyecto
uv run ruff check --fix            # corrige lo que se puede corregir solo
uv run ruff check app/main.py      # un archivo
uv run ruff rule E711              # explica una regla
```

Las reglas se agrupan por **prefijo**, heredado de la herramienta original:

| Prefijo | Origen        | Qué detecta                                              |
|---------|---------------|----------------------------------------------------------|
| `E`/`W` | pycodestyle   | estilo: líneas largas, espacios, `== None`               |
| `F`     | pyflakes      | imports sin usar, nombres indefinidos, variables sin usar |
| `I`     | isort         | orden de los imports                                     |
| `UP`    | pyupgrade     | sintaxis vieja: `List[int]`, `Optional`, `%` formatting  |
| `B`     | bugbear       | trampas: defaults mutables, `except:` a secas            |
| `SIM`   | simplify      | código que se puede simplificar                          |
| `N`     | pep8-naming   | convenciones de nombres                                  |
| `RUF`   | ruff          | reglas propias                                           |

Configuración en `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py312"          # para UP: qué sintaxis moderna podés usar

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
ignore = ["E501"]                 # si querés ignorar alguna

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]              # por ejemplo, permitir assert en tests
```

Para ignorar un caso puntual, un comentario en la línea (con el código de la regla, nunca a
secas):

```python
from modulo import *  # noqa: F403
```

### Ejemplos de lo que encuentra

```python
import os, sys                   # E401: varios imports en una línea; F401: sin usar
from typing import List, Optional   # UP035: import deprecado
def f(x: List[int]) -> Optional[str]:   # UP006/UP045: usá list[int] y str | None
    if x == None:                # E711: comparar con None usando `is`
        return None
    try: ...
    except: ...                  # E722/B001: except a secas
```

## ruff: formateador

```bash
uv run ruff format               # formatea todo (compatible con black)
uv run ruff format --check       # solo verifica, para el CI
```

Un formateador termina con las discusiones de estilo: comillas, espacios y cortes de línea.
No se configura casi nada, y justamente eso es lo bueno.

## mypy: type checker

```bash
uv run mypy app                  # verifica un paquete
uv run mypy --strict archivo.py  # modo estricto
```

mypy lee las anotaciones y **razona** sobre el código:

```python
def buscar(ids: dict[int, str], id: int) -> str:
    return ids.get(id)       # error: Incompatible return value type (got "str | None", expected "str")
```

El error es real: `.get` puede devolver `None`. La solución es manejar el caso o cambiar el
tipo de retorno a `str | None`.

### `--strict`

El modo estricto activa un conjunto de chequeos, entre ellos:

- todas las funciones tienen que estar **completamente anotadas**
  (`--disallow-untyped-defs`);
- no se permite `Any` implícito;
- avisa si un `# type: ignore` no hace falta.

Para proyectos nuevos, arrancá en `strict`. Para código viejo, activalo de a poco, módulo por
módulo:

```toml
[tool.mypy]
python_version = "3.12"
strict = true

[[tool.mypy.overrides]]
module = ["legacy.*"]
disallow_untyped_defs = false
```

### Herramientas útiles

```python
reveal_type(x)           # mypy te dice qué tipo infirió (se usa solo al chequear)
x = f()  # type: ignore[arg-type]   # silenciar UN error concreto, con su código
from typing import cast
y = cast(int, valor)     # "confiá en mí" (sin efecto al ejecutar)
```

Alternativas a mypy: **pyright** (el que usa VS Code con Pylance, muy rápido) y **ty** (de
Astral, en desarrollo). Los conceptos son los mismos.

## Integrarlo al flujo

- **En el editor**: la extensión de ruff marca los problemas mientras escribís y puede formatear
  al guardar.
- **Antes del commit**: `pre-commit` con los hooks de ruff.
- **En el CI**: `ruff check`, `ruff format --check`, `mypy` y `pytest`. Si alguno falla, no se
  mergea.

```bash
uv run ruff check && uv run ruff format --check && uv run mypy . && uv run pytest
```

## Resumen

- `ruff check [--fix]` como linter, con reglas por prefijo (`E`, `F`, `I`, `UP`, `B`, `SIM`) y
  configuración en `pyproject.toml`.
- `ruff format` como formateador sin discusiones.
- `mypy --strict` para proyectos nuevos; activación gradual con `overrides` en código viejo.
- `# noqa: CODIGO` y `# type: ignore[codigo]` siempre con el código específico.
- Todo corre en el CI.

## Ejercicio

El archivo tiene código **viejo**: imports mal hechos, sintaxis de tipos anterior a 3.10 y
funciones sin anotar. Implementá las funciones y dejalo **limpio para ruff** (`E, F, I, UP, B,
SIM`) **y para `mypy --strict`**. Los tests corren las dos herramientas sobre tu archivo.

**Para profundizar:** [reglas de ruff](https://docs.astral.sh/ruff/rules/),
[mypy: getting started](https://mypy.readthedocs.io/en/stable/getting_started.html).
