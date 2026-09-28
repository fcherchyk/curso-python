# Proyecto: un analizador de logs con CLI

Llegó el momento de juntar todo en un programa real: una herramienta de línea de comandos
que lee un log de accesos, lo parsea de forma tolerante a errores, calcula métricas y
muestra un reporte. Es chica, pero tiene la forma de cualquier herramienta profesional:
modelos inmutables, parseo con validación, un pipeline perezoso, agregaciones, formato de
salida y una CLI testeable.

```
$ python ejercicio.py access.log --top 3
Requests: 120 (inválidas: 2)
Errores 5xx: 6 (5.0%)
Latencia p50: 113.5 ms | p95: 365.4 ms
Ruta más lenta: /api/report
Status:
  200: 95
  201: 15
  404: 4
  500: 6
Top rutas:
  /api/orders      40
  /api/users       37
  /api/products    20
```

## El diseño por piezas

| Pieza                     | Qué practica                                              |
|---------------------------|-----------------------------------------------------------|
| `Metodo(StrEnum)`         | enums (módulo 05)                                         |
| `Registro` frozen + `es_error` | dataclasses y `@property`                            |
| `LineaInvalida(ValueError)` | excepciones propias encadenadas con `from`              |
| `parsear_linea`           | regex con grupos nombrados, walrus y validación           |
| `parsear`                 | generador tolerante a errores (módulo 03)                 |
| `resumir`                 | `Counter`, `statistics`, agrupar y `max(key=...)`          |
| `formatear`               | f-strings con format spec y unpacking en listas           |
| `main`                    | `argparse`, `pathlib`, `with`, stderr y códigos de salida |

La regla de oro del diseño: **la lógica no sabe nada de la consola**. `parsear`, `resumir` y
`formatear` reciben y devuelven datos. Solo `main` lee argumentos, abre archivos e imprime.
Por eso todo se puede testear sin archivos ni subprocesos.

## Regex con grupos nombrados

```python
import re

PATRON = re.compile(
    r"^(?P<momento>\S+) (?P<metodo>[A-Z]+) (?P<ruta>/\S*) (?P<status>\d{3}) (?P<ms>\d+)ms$"
)

if m := PATRON.match(linea.strip()):
    m["status"], m["ms"]          # o m.group("status")
```

- Compilá la regex **una vez**, a nivel de módulo.
- `(?P<nombre>...)` hace legible el código que usa el match.
- `^` y `$` anclan el patrón: sin ellos, una línea con basura al final podría pasar.
- Usá strings crudos (`r"..."`) para que `\d` y `\S` lleguen intactos a la regex.

## Traducir errores: excepciones propias encadenadas

```python
class LineaInvalida(ValueError):      # heredá de la excepción estándar más cercana
    """La línea no respeta el formato esperado."""

try:
    momento = datetime.fromisoformat(m["momento"])
    metodo = Metodo(m["metodo"])
except ValueError as e:
    raise LineaInvalida(linea) from e
```

Quien llama maneja **un solo tipo** de error (`LineaInvalida`) sin perder la causa original
(`__cause__`). Como hereda de `ValueError`, el código que ya atrapaba `ValueError` sigue
funcionando.

## Estadística sin numpy: `statistics`

```python
import statistics

statistics.fmean([100, 120, 900])                          # promedio (float, rápido)
statistics.median(duraciones)
q = statistics.quantiles(duraciones, n=100, method="inclusive")
p50, p95 = q[49], q[94]                                    # percentiles
```

Los **percentiles** son mejores que el promedio para latencias: un solo request de 10
segundos arruina el promedio, pero el p95 te dice "el 95 % de los requests tardó menos de
X".

## CLI con `argparse`

```python
import argparse
from pathlib import Path

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analiza logs de acceso")
    parser.add_argument("archivo", type=Path)                   # posicional
    parser.add_argument("--top", type=int, default=5, help="cantidad de rutas")
    args = parser.parse_args(argv)          # argv=None → usa sys.argv[1:]
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

Claves de una CLI bien hecha:

- **`main(argv)` recibe los argumentos**, así los tests llaman a `main(["x.log", "--top", "2"])`
  sin subprocesos.
- **Devuelve un código de salida**: 0 si salió bien, distinto de 0 si hubo error. Así se puede
  encadenar en scripts de shell (`&&`).
- **Los errores van a stderr** (`print(..., file=sys.stderr)`) y la salida útil a stdout: así
  `analizar log > reporte.txt` no mezcla los errores con el reporte.
- `argparse` genera `--help` y valida tipos gratis.

Para CLIs más grandes, **Typer** (del autor de FastAPI, basado en type hints) o **Click**.

## Instalarla como comando

Con un `pyproject.toml` y la sección `[project.scripts]`, uv crea un ejecutable:

```toml
[project.scripts]
analizar-logs = "logs.cli:main"
```

```bash
uv tool install .            # queda disponible como `analizar-logs` en tu PATH
```

## Pasos sugeridos

1. `Registro.es_error` y `parsear_linea` (tests `test_parsear_linea*`).
2. `parsear` (generador que junta las inválidas).
3. `Resumen.tasa_error`, `resumir` y `top_rutas`.
4. `formatear` (formato exacto: mirá el test).
5. `main`, y probala de verdad: el test final la ejecuta sobre `access.log`.

## Resumen

- Separá la lógica pura (parsear, resumir, formatear) de la entrada y salida (`main`).
- Regex compiladas, ancladas y con grupos nombrados.
- Traducí errores a una excepción propia encadenada con `from`.
- Percentiles con `statistics.quantiles` para las latencias.
- `main(argv) -> int`, errores a stderr, `raise SystemExit(main())`.

## Ejercicio

Implementá el analizador completo: modelos, parseo, métricas, reporte y CLI.

**Retos extra** (no tienen test): `--desde`/`--hasta` para filtrar por fecha, `--json` para
emitir el resumen con `asdict` + `json.dumps`, y aceptar `-` como archivo para leer de stdin.

**Para profundizar:** [argparse tutorial](https://docs.python.org/3/howto/argparse.html),
[re](https://docs.python.org/3/library/re.html),
[statistics](https://docs.python.org/3/library/statistics.html), [Typer](https://typer.tiangolo.com/).
