# Día 5: Lo que cambió de 3.8 a 3.14

**Objetivo:** ponerte al día con la sintaxis nueva que vas a ver en código actual (y en
entrevistas).

## Resumen por versión

| Versión | Lo importante                                                               |
|---------|-----------------------------------------------------------------------------|
| 3.8     | walrus `:=`, `f"{x=}"`, parámetros solo posicionales `/`                    |
| 3.9     | `dict \| dict`, `list[int]` sin `typing`, `str.removeprefix/removesuffix`, `zoneinfo` |
| 3.10    | **`match`/`case`**, `X \| Y` en tipos, `zip(strict=True)`, mejores mensajes de error |
| 3.11    | **10–60% más rápido**, `ExceptionGroup` + `except*`, `tomllib`, `Self`, `StrEnum`, `asyncio.TaskGroup` |
| 3.12    | **genéricos `class C[T]`**, `type Alias = ...`, f-strings sin límites de comillas, `itertools.batched`, `@override` |
| 3.13    | REPL nuevo (colores, multilínea), build **free-threaded** (sin GIL, experimental), JIT experimental |
| 3.14    | **t-strings** `t"..."` (templates), anotaciones con evaluación diferida, free-threading con soporte oficial |

## 1. `match` / `case`

No es un `switch`: es **pattern matching estructural**. Desarma estructuras y captura
variables.

```python
match comando.split():
    case ["ir", direccion]:  # secuencia de 2, captura
        ...
    case ["tomar", *objetos] if objetos:  # resto + guarda
        ...
    case ["salir" | "quit"]:  # alternativas
        ...
    case _:  # comodín
        ...

match evento:  # mapeos: claves extra se ignoran
    case {"tipo": "click", "x": int(x), "y": int(y)}:
        ...

match figura:  # clases (usa atributos)
    case Circulo(radio=0):
        ...
    case Rectangulo(ancho=a, alto=b) if a == b:
        ...
```

**Trampa:** un nombre suelto en un `case` **captura**, no compara.
`case ROJO:` captura cualquier cosa en la variable `ROJO`. Para comparar contra constantes
usá nombres con punto: `case Color.ROJO:`.

## 2. Walrus `:=`

Asigna y devuelve el valor dentro de una expresión.

```python
while linea := f.readline():
    ...
if m := re.match(patron, texto):
    print(m.group(1))
[y for x in datos if (y := f(x)) is not None]  # calcula f(x) una sola vez
```

Usalo cuando elimina duplicación, no para ahorrar una línea.

## 3. `ExceptionGroup` y `except*`

Sirven para reportar **varios errores a la vez**: validaciones o tareas concurrentes
(`asyncio.TaskGroup` los levanta así).

```python
raise ExceptionGroup("validación", [ValueError("a"), TypeError("b")])

try:
    ...
except* ValueError as eg:  # eg es un ExceptionGroup solo con los ValueError
    for e in eg.exceptions:
        ...
except* TypeError as eg:  # ¡se pueden ejecutar varias ramas!
    ...
```

## 4. f-strings

```python
f"{nombre:<12}"  # izquierda en 12
f"{precio:>10,.2f}"  # derecha en 10, miles con coma, 2 decimales
f"{n:08.3f}"  # relleno con ceros
f"{pct:.1%}"  # 0.256 -> '25.6%'
f"{fecha:%Y-%m-%d}"  # datetime
f"{x=}"  # 'x=42'
f"{d['clave']}"  # 3.12+: mismas comillas adentro
```

## 5. t-strings (3.14, opcional)

`t"Hola {nombre}"` **no** devuelve un `str` sino un objeto `Template` con las partes
separadas. Sirve para que librerías hagan interpolación segura (SQL, HTML, logs) sin
inyección. Todavía es muy nuevo; alcanza con reconocerlo.

## 6. Otros que vas a ver

- `tomllib.loads()` / `tomllib.load(f)` (binario): leer `pyproject.toml` y configs.
- `from typing import Self, override`.
- `asyncio.TaskGroup` (se ve en la semana 3).
- `pathlib.Path` en todos lados en vez de `os.path`: `Path("a") / "b" / "c.txt"`,
  `.read_text()`, `.glob("*.py")`.

## Ejercicios

```bash
uv run pytest semana1/dia5_novedades
```

**Reto extra:** reescribí `procesar_evento` del ejercicio con una cadena de `if/elif` y
compará la legibilidad.

## Para profundizar

- [PEP 636: tutorial de pattern matching](https://peps.python.org/pep-0636/). Es el mejor
  recurso para `match`.
- "What's New in Python 3.X" en docs.python.org. Leé al menos 3.10, 3.11 y 3.12.
