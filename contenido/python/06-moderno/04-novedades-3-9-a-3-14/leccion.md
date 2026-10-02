# Novedades de 3.9 a 3.14

Si aprendiste Python hace unos años, hay bastante sintaxis y biblioteca estándar nueva que
aparece en cualquier código actual. Este capítulo es un mapa por versión y un repaso práctico
de lo que más se usa y todavía no vimos: `tomllib`, `zoneinfo`, las mejoras de las f-strings
y las t-strings.

## El mapa

| Versión | Lo importante                                                                 |
|---------|-------------------------------------------------------------------------------|
| 3.8     | walrus `:=`, `f"{x=}"`, parámetros solo posicionales `/`                      |
| 3.9     | `dict \| dict`, `list[int]` sin `typing`, `str.removeprefix/removesuffix`, **`zoneinfo`** |
| 3.10    | **`match`/`case`**, `X \| Y` en tipos, `zip(strict=True)`, `pairwise`, mejores mensajes de error |
| 3.11    | **entre 10 % y 60 % más rápido**, `ExceptionGroup`/`except*`, `add_note`, **`tomllib`**, `Self`, `StrEnum`, `TaskGroup` |
| 3.12    | **genéricos `class C[T]`**, `type Alias = …`, f-strings sin límites, `itertools.batched`, `@override` |
| 3.13    | REPL nuevo (colores, edición multilínea), build **free-threaded** (sin GIL, experimental), JIT experimental |
| 3.14    | **t-strings** `t"…"`, anotaciones evaluadas de forma diferida, free-threading con soporte oficial, `compression.zstd` |

Leer las páginas "What's New in Python 3.X" de las últimas versiones es una muy buena forma de
ponerse al día.

## `tomllib` (3.11): leer TOML

TOML es el formato de `pyproject.toml` y de muchas configuraciones. La stdlib lo **lee**
(para escribirlo hace falta un paquete como `tomli-w`):

```python
import tomllib

with open("pyproject.toml", "rb") as f:        # ¡en modo binario!
    datos = tomllib.load(f)

config = tomllib.loads('[server]\nport = 8000')   # desde un string
config["server"]["port"]                          # 8000 (ya es int)
```

TOML tiene tipos (`int`, `float`, `bool`, fechas, arrays y tablas), así que no hace falta
convertir a mano como con los `.ini`.

Un patrón muy común es fusionar la configuración leída sobre los defaults con `|`:

```python
DEFAULTS = {"host": "localhost", "port": 8000, "debug": False}
config = DEFAULTS | datos.get("server", {})     # no muta DEFAULTS
```

## `zoneinfo` (3.9): zonas horarias sin librerías externas

```python
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

ahora_utc = datetime.now(UTC)                          # siempre guardá en UTC
ba = ahora_utc.astimezone(ZoneInfo("America/Argentina/Buenos_Aires"))
madrid = ahora_utc.astimezone(ZoneInfo("Europe/Madrid"))   # sabe del horario de verano
```

Reglas de oro con fechas:

- Trabajá con datetimes **aware** (con zona). Los *naive* (sin zona) son ambiguos.
- **Guardá y compará en UTC**; convertí a la zona local solo para mostrar.
- `datetime.utcnow()` está deprecado: usá `datetime.now(UTC)`.
- `datetime.fromisoformat()` parsea casi cualquier ISO 8601 desde 3.11, incluido el sufijo `Z`.

Profundizamos en el módulo de stdlib esencial.

## f-strings: lo nuevo

```python
f"{x=}"                        # 3.8: 'x=42'
f"{x = :.2f}"                  # combinable con formato: 'x = 42.00'
f"{usuario['nombre']}"         # 3.12: mismas comillas adentro
f"{'\n'.join(lineas)}"         # 3.12: barras invertidas permitidas
f"{
    precio      # 3.12: expresiones multilínea y comentarios
    * cantidad
}"
```

Y el mini-lenguaje de formato de siempre, que conviene tener a mano para tablas:

```python
f"{nombre:<12}"          # izquierda, ancho 12
f"{precio:>10,.2f}"      # derecha, ancho 10, miles, 2 decimales
f"{'TOTAL':^20}"         # centrado
f"{n:08.3f}"             # relleno con ceros
```

## t-strings (3.14): plantillas seguras

`t"Hola {nombre}"` se parece a una f-string, pero **no devuelve un `str`**: devuelve un objeto
`Template` que conserva por separado las partes literales y los valores interpolados. La idea
es que una librería decida **cómo** combinarlos de forma segura:

```python
from string.templatelib import Template

nombre = "<script>"
t = t"<p>Hola {nombre}</p>"
t.strings        # ('<p>Hola ', '</p>')
t.values         # ('<script>',)
html(t)          # una función que escapa los valores → '<p>Hola &lt;script&gt;</p>'
```

Resuelven el problema de las inyecciones (SQL, HTML, comandos de shell) sin renunciar a la
comodidad de la sintaxis de interpolación. Todavía son muy nuevas: alcanza con reconocerlas.
(El entorno de este curso usa 3.13, así que no las vas a poder ejecutar acá.)

## Otras que vas a ver

```python
from typing import override            # 3.12: marca que un método sobrescribe al padre
from itertools import batched          # 3.12: lotes de n
import tomllib, zoneinfo
"archivo.tar.gz".removesuffix(".gz")   # 3.9
sorted(d.items(), key=...)             # dicts ordenados (3.7) → dict(sorted(...))
```

Y en herramientas: `uv` reemplazó a pip, venv y pyenv, y `ruff` a flake8, isort y black
(próximo módulo).

## Resumen

- 3.10 trajo `match` y `X | Y`; 3.11, velocidad, `ExceptionGroup` y `tomllib`; 3.12,
  genéricos nuevos y f-strings sin límites; 3.14, t-strings.
- `tomllib.load` en modo binario; fusioná sobre los defaults con `|`.
- `zoneinfo` + `datetime.now(UTC)`: guardá en UTC y mostrá en la zona local.
- f-strings: `=`, comillas anidadas y el mini-lenguaje de formato para tablas.

## Ejercicio

Una tabla con f-strings de ancho fijo, una configuración TOML fusionada sobre defaults y una
conversión de zonas horarias con `zoneinfo`.

**Para profundizar:** "What's New" de [3.11](https://docs.python.org/3/whatsnew/3.11.html),
[3.12](https://docs.python.org/3/whatsnew/3.12.html),
[3.13](https://docs.python.org/3/whatsnew/3.13.html) y
[3.14](https://docs.python.org/3/whatsnew/3.14.html).
