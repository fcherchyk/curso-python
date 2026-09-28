# Día 6: Proyecto integrador y herramientas modernas

**Objetivo:** juntar todo lo de la semana en un programa real (un analizador de logs con
CLI) y trabajar como en un proyecto profesional: tests, linter, formateador y type checker.

## 1. El stack de herramientas en 2026

| Herramienta | Reemplaza a                          | Uso                                      |
|-------------|--------------------------------------|------------------------------------------|
| **uv**      | pip, venv, pip-tools, pyenv, pipx    | `uv init`, `uv add httpx`, `uv run ...`, `uv python install 3.13` |
| **ruff**    | flake8, isort, black, pyupgrade      | `uv run ruff check --fix` / `uv run ruff format` |
| **mypy** o **pyright** | —                         | `uv run mypy semana1`                    |
| **pytest**  | unittest                             | `uv run pytest -x -k patrón`             |

Todo se configura en **`pyproject.toml`**; mirá el de este repo. `uv.lock` fija las versiones
exactas y va al control de versiones.

```bash
uv init mi-proyecto && cd mi-proyecto
uv add fastapi                 # dependencia
uv add --dev pytest ruff       # dependencia de desarrollo
uv run pytest
uvx ruff check                 # ejecutar una herramienta sin instalarla
```

## 2. Lo que vas a practicar en el proyecto

| Pieza                  | Concepto de la semana                                    |
|------------------------|----------------------------------------------------------|
| `Metodo(StrEnum)`      | enums (día 4)                                            |
| `Registro` frozen + `es_error` | dataclasses y `@property` (día 4)                |
| `parsear_linea`        | regex con grupos nombrados, walrus, `raise ... from e` (día 5) |
| `parsear`              | generador perezoso con errores tolerados (día 2)         |
| `resumir`              | `Counter`, `statistics`, `max(key=...)`, dict ordenado (día 1) |
| `formatear`            | f-strings con format spec, unpacking en listas (días 1 y 5) |
| `main`                 | `argparse`, `pathlib`, `with open`, exit codes (día 3)   |

### Excepciones propias y encadenadas

```python
class LineaInvalida(ValueError): ...  # heredá de la excepción estándar más cercana


try:
    fecha = datetime.fromisoformat(texto)
except ValueError as e:
    raise LineaInvalida(linea) from e  # conserva la causa original en el traceback
```

### Regex con grupos nombrados

```python
PATRON = re.compile(r"(?P<status>\d{3}) (?P<ms>\d+)ms$")
if m := PATRON.search(linea):
    m["status"], m["ms"]  # o m.group("status")
```

### CLI con argparse

```python
def main(argv=None) -> int:  # argv=None usa sys.argv; en tests pasás una lista
    parser = argparse.ArgumentParser()
    parser.add_argument("archivo", type=Path)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)
    ...
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Recibir `argv` como parámetro hace que la CLI sea testeable sin subprocess (mirá `test_main`).
Para CLIs más grandes, **Typer** (del autor de FastAPI) o **Click**.

## 3. Pasos sugeridos

1. `Registro.es_error` y `parsear_linea`. Hacé pasar los tests `test_parsear_linea*`.
2. `parsear`
3. `resumir`, `Resumen.tasa_error` y `top_rutas`
4. `formatear`
5. `main`. Después probalo de verdad:

```bash
uv run python -m semana1.dia6_proyecto.ejercicios semana1/dia6_proyecto/access.log --top 3
```

6. Pasá las herramientas y corregí lo que marquen:

```bash
uv run ruff check semana1/dia6_proyecto
uv run ruff format semana1/dia6_proyecto
uv run mypy semana1/dia6_proyecto/ejercicios.py --strict
```

## Reto extra

- Agregá `--desde` y `--hasta` (fechas ISO) para filtrar registros por rango.
- Agregá `--json` para emitir el resumen como JSON (`dataclasses.asdict` + `json.dumps`).
- Hacé que acepte `-` como archivo para leer de stdin (`cat access.log | ...`).

## Para profundizar

- [Documentación de uv](https://docs.astral.sh/uv/) y [reglas de ruff](https://docs.astral.sh/ruff/rules/)
- [Doc de pytest: fixtures y parametrize](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [argparse tutorial](https://docs.python.org/3/howto/argparse.html)
