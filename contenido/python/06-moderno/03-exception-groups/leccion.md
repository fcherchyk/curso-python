# ExceptionGroup, `except*` y notas

Hasta 3.10, una excepción representaba **un** error. Pero hay situaciones en las que ocurren
**varios a la vez** y querés reportarlos todos juntos: validar un formulario completo, correr
tareas en paralelo donde fallan dos o procesar un lote con errores en distintas filas. Para
eso, 3.11 agregó `ExceptionGroup`, la sintaxis `except*` y las notas en las excepciones.

## `ExceptionGroup`: varias excepciones en una

```python
errores = [ValueError("nombre vacío"), TypeError("edad no es int")]
raise ExceptionGroup("usuario inválido", errores)
```

El traceback muestra un árbol con todos los errores:

```
  | ExceptionGroup: usuario inválido (2 sub-exceptions)
  +-+---------------- 1 ----------------
    | ValueError: nombre vacío
    +---------------- 2 ----------------
    | TypeError: edad no es int
    +------------------------------------
```

- El primer argumento es un mensaje; el segundo, una **secuencia no vacía** de excepciones.
- `.exceptions` da la tupla de sub-excepciones.
- Los grupos se pueden **anidar**: un grupo puede contener otros grupos.
- Si todas las sub-excepciones heredan de `Exception`, se crea un `ExceptionGroup`; si alguna
  es un `BaseException` (como `KeyboardInterrupt`), un `BaseExceptionGroup`.

### El patrón: acumular y levantar al final

```python
def validar(datos: dict) -> None:
    errores: list[Exception] = []
    if not datos.get("nombre"):
        errores.append(ValueError("nombre"))
    if not isinstance(datos.get("edad"), int):
        errores.append(TypeError("edad"))
    if errores:
        raise ExceptionGroup("datos inválidos", errores)
```

A quien completa un formulario le sirve mucho más recibir **todos** los problemas juntos que
corregirlos de a uno por intento.

## `except*`: manejar por tipo dentro del grupo

Un `except ValueError` común **no** atrapa un `ExceptionGroup` que contiene `ValueError`s.
Para eso está `except*`:

```python
try:
    validar(datos)
except* ValueError as grupo:          # grupo es un ExceptionGroup SOLO con los ValueError
    for e in grupo.exceptions:
        print("valor inválido:", e)
except* TypeError as grupo:           # ¡esta rama TAMBIÉN se ejecuta si hay TypeErrors!
    for e in grupo.exceptions:
        print("tipo inválido:", e)
```

Diferencias con el `except` clásico:

- **Se pueden ejecutar varias ramas**: cada una se queda con "su parte" del grupo.
- En cada rama, la variable es **un grupo** (filtrado), no una excepción suelta.
- Lo que no manejó ninguna rama se **re-levanta** automáticamente como un grupo con lo que
  sobró.
- No se puede mezclar `except` y `except*` en el mismo `try`.
- `except*` también atrapa una excepción común (no agrupada): la envuelve en un grupo.

### Filtrar a mano: `split` y `subgroup`

```python
valores, resto = grupo.split(ValueError)      # (grupo con ValueError, grupo con el resto)
solo_valores = grupo.subgroup(ValueError)     # o None si no hay
```

## Dónde vas a verlos: `asyncio.TaskGroup`

El caso de uso más frecuente es la concurrencia. Si en un `TaskGroup` fallan dos tareas, se
levanta un `ExceptionGroup` con las dos (lo vemos en el módulo de concurrencia):

```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(descargar(url1))
        tg.create_task(descargar(url2))
except* TimeoutError:
    ...
except* ConnectionError:
    ...
```

## Notas: contexto extra en cualquier excepción

`add_note` (3.11) agrega texto que aparece en el traceback, **sin cambiar el tipo ni el
mensaje** de la excepción. Es ideal para decir *dónde* ocurrió el error:

```python
for n, fila in enumerate(filas, start=1):
    try:
        procesar(fila)
    except ValueError as e:
        e.add_note(f"en la fila {n}: {fila!r}")
        raise
```

```
ValueError: invalid literal for int() with base 10: 'x'
en la fila 3: 'ana,x'
```

Las notas quedan en `e.__notes__` (una lista). Son mejores que envolver en otra excepción
cuando solo querés agregar contexto.

## Resumen

- `ExceptionGroup(mensaje, [excepciones])` para reportar varios errores juntos.
- Acumulá en una lista y levantá el grupo al final si no está vacía.
- `except* Tipo as grupo`: pueden correr varias ramas; lo no manejado se re-levanta.
- `split` y `subgroup` para filtrar a mano.
- `e.add_note(...)` para agregar contexto sin cambiar la excepción.

## Ejercicio

Una validación que reporta todos los errores, una clasificación con `except*` y un ejecutor
de tareas que junta los fallos con notas.

**Para profundizar:** [PEP 654 — Exception Groups and except*](https://peps.python.org/pep-0654/),
[PEP 678 — add_note](https://peps.python.org/pep-0678/).
