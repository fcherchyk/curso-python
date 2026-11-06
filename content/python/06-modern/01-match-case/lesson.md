# Pattern matching: `match` / `case`

`match` (3.10) **no es un `switch`**. Es *pattern matching estructural*: compara un valor
contra **patrones** que describen su forma y, en el mismo paso, **desarma** la estructura y
captura sus partes en variables. Brilla cuando procesás comandos, eventos, JSON, árboles de
sintaxis o mensajes con distintas formas.

## Anatomía

```python
match sujeto:
    case patron_1:
        ...
    case patron_2 if condicion:     # guarda opcional
        ...
    case _:                         # comodín: todo lo demás
        ...
```

Los `case` se prueban **en orden** y se ejecuta **solo el primero** que coincide (no hay
*fall-through* ni `break`). Si ninguno coincide y no hay `case _`, no pasa nada.

## Los tipos de patrones

### Literales y alternativas

```python
match status:
    case 200 | 201 | 204:
        return "ok"
    case 404:
        return "no encontrado"
    case 500 | 502 | 503:
        return "error del servidor"
```

### Capturas

Un **nombre suelto** captura el valor, cualquiera sea:

```python
match punto:
    case (0, 0):
        return "origen"
    case (x, 0):                  # captura x; exige y == 0
        return f"sobre el eje X en {x}"
    case (x, y):
        return f"({x}, {y})"
```

### ⚠️ La trampa: un nombre suelto **captura**, no compara

```python
ROJO = "rojo"
match color:
    case ROJO:            # ✗ ¡NO compara con "rojo"! captura cualquier cosa en ROJO
        ...
```

Para comparar contra constantes, usá un **nombre con punto** (`Color.ROJO`,
`config.MODO_DEBUG`) o un literal. Python sabe que un nombre con punto es un valor y no una
captura.

### Secuencias

```python
match comando.split():
    case []:
        return "vacío"
    case ["salir" | "quit"]:
        return "chau"
    case ["ir", direccion]:                     # exactamente 2 elementos
        return f"yendo a {direccion}"
    case ["tomar", *objetos] if objetos:        # 1 o más: *resto como en el unpacking
        return f"tomaste {', '.join(objetos)}"
    case ["tomar", primero, *_]:                # _ descarta
        ...
```

Los patrones de secuencia matchean listas y tuplas, pero **no** strings (un `str` no se
desarma carácter por carácter, por diseño).

### Captura con `as`

```python
case ["ir", ("norte" | "sur" | "este" | "oeste") as direccion]:
    ...
```

### Mapeos (dicts)

```python
match evento:
    case {"tipo": "click", "x": x, "y": y}:
        return f"click en ({x}, {y})"
    case {"tipo": "tecla", "tecla": "enter"}:
        return "confirmar"
    case {"tipo": "tecla", "tecla": tecla}:
        return f"tecla {tecla}"
```

Las **claves extra se ignoran**: `{"tipo": "click", "x": 1, "y": 2, "boton": "izq"}` matchea
el primer caso. Es justo lo que querés con JSON, donde siempre pueden aparecer campos nuevos.
Para capturar el resto, `**resto`.

### Clases (con validación de tipo)

```python
match figura:
    case Circulo(radio=0):
        return "degenerada"
    case Circulo(radio=r):
        return f"círculo de radio {r}"
    case Rectangulo(ancho=a, alto=b) if a == b:
        return f"cuadrado de lado {a}"
    case Rectangulo(ancho=a, alto=b):
        return f"rectángulo {a} x {b}"
```

`Circulo(radio=r)` significa: "es instancia de `Circulo` y su atributo `radio` va a `r`".
Las dataclasses permiten además la forma posicional, `Circulo(r)`, porque generan
`__match_args__`.

Con tipos built-in, `int(x)` o `str(s)` **verifica el tipo y captura**:

```python
case {"x": int(x), "y": int(y)}:     # solo si x e y son enteros
```

## Guardas

`if` después del patrón agrega una condición. Si el patrón coincide pero la guarda es falsa,
se sigue con el próximo `case`:

```python
case {"tipo": "scroll", "delta": d} if d < 0:
    return "abajo"
case {"tipo": "scroll", "delta": d} if d > 0:
    return "arriba"
```

## ¿`match` o `if/elif`?

- **`match`** cuando ramificás según la **forma** de los datos (qué claves hay, cuántos
  elementos, de qué clase es) y querés extraer partes.
- **`if/elif`** para condiciones booleanas simples o rangos (`if edad < 18`). Un `match` con
  puros literales tampoco agrega mucho frente a un dict de despacho.

## Resumen

- `match` compara **forma** y **desarma** en un paso; gana el primer `case` que coincide.
- Literales, `|`, capturas, secuencias con `*resto`, mapeos (claves extra ignoradas), clases
  con atributos y `int(x)` para validar tipo.
- **Un nombre suelto captura.** Para constantes, usá un nombre con punto.
- `case _` como comodín; `if` como guarda; `as` para capturar un sub-patrón.

## Ejercicio

Un intérprete de comandos, un procesador de eventos tipo JSON y un descriptor de figuras,
todos con `match`.

**Para profundizar:** [PEP 636 — tutorial de pattern matching](https://peps.python.org/pep-0636/)
(el mejor recurso para aprenderlo).
