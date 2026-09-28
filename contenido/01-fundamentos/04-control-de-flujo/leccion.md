# Control de flujo

La mayoría de las estructuras de control de Python funcionan como en cualquier lenguaje.
Este capítulo se concentra en lo que es **propio de Python**: comparaciones encadenadas,
el `else` de los bucles, la expresión condicional y algunos patrones que evitan anidar.

## `if` / `elif` / `else`

```python
if temperatura < 10:
    estado = "frío"
elif temperatura < 25:
    estado = "templado"
else:
    estado = "calor"
```

No hay `switch` clásico. Para ramificar según la forma de los datos existe `match`, que vemos
en el módulo de Python moderno. Para mapear valores simples, muchas veces alcanza con un dict:

```python
PRECIOS = {"chico": 100, "mediano": 150, "grande": 200}
precio = PRECIOS.get(tamaño, 0)
```

### Comparaciones encadenadas

```python
if 0 <= indice < len(xs): ...     # equivale a 0 <= indice and indice < len(xs)
if a == b == c: ...
```

Cada expresión intermedia se evalúa **una sola vez**. Es más legible y evita repetir la
variable.

### Operadores lógicos: devuelven operandos, no `bool`

`and` y `or` cortocircuitan y **devuelven uno de los operandos**:

```python
0 or "default"         # 'default'
"valor" or "default"   # 'valor'
[] and "nunca"         # []
usuario and usuario.nombre     # None si usuario es None, sin AttributeError
```

`not` sí devuelve siempre `True` o `False`.

### Expresión condicional (ternario)

```python
etiqueta = "par" if n % 2 == 0 else "impar"
```

Usala para valores simples. Si alguna de las ramas necesita lógica, volvé al `if`.

## Cláusulas de guarda: salir temprano

En lugar de anidar condiciones, conviene resolver los casos especiales al principio y
retornar:

```python
# ✗ Pirámide
def procesar(pedido):
    if pedido is not None:
        if pedido.items:
            if pedido.pagado:
                return enviar(pedido)
    return None

# ✓ Guardas
def procesar(pedido):
    if pedido is None or not pedido.items:
        return None
    if not pedido.pagado:
        return None
    return enviar(pedido)
```

El camino "feliz" queda sin indentar y cada condición se lee por separado.

## `for`: recorre iterables

```python
for x in [1, 2, 3]: ...
for i in range(5): ...              # 0..4
for i in range(10, 0, -2): ...      # 10, 8, 6, 4, 2
for c in "hola": ...
for linea in open("datos.txt"): ...
```

`break` sale del bucle; `continue` pasa a la siguiente vuelta.

### `for ... else`: el `else` que casi nadie conoce

El bloque `else` de un bucle se ejecuta **si el bucle terminó sin `break`**:

```python
for usuario in usuarios:
    if usuario.es_admin:
        print("hay admin:", usuario)
        break
else:
    print("no hay ningún admin")
```

Es el patrón de "buscar y actuar si no se encontró", sin una variable `encontrado = False`.
Pensalo como "si no hubo break". Como a mucha gente le resulta confuso, dejalo para
búsquedas cortas y, si lo usás, agregá un comentario. A veces es más claro extraer una
función y usar `return`, o `any()` o `next(...)`.

## `while`

```python
intentos = 0
while intentos < 3:
    if conectar():
        break
    intentos += 1
else:
    raise ConnectionError("no se pudo conectar")   # también existe while/else
```

Usá `while` cuando **no sabés de antemano** cuántas vueltas vas a dar: reintentos, lectura
hasta un centinela o algoritmos que convergen. Para recorrer colecciones, siempre `for`.

Con el operador walrus (`:=`, 3.8+) se evita duplicar la lectura:

```python
while (linea := archivo.readline()):
    procesar(linea)
```

## `pass`, `...` y bloques vacíos

Python no permite bloques vacíos. Para un bloque que todavía no tiene código, se usa `pass`
(o `...`, muy común en stubs y protocolos):

```python
def todo_implementar():
    ...

class MiError(Exception):
    pass
```

## Scopes: los bloques no crean ámbito

A diferencia de C o Java, **`if`, `for` y `while` no crean un scope nuevo**. Las variables
definidas adentro siguen existiendo afuera:

```python
for i in range(3):
    ultimo = i
print(i, ultimo)     # 2 2
```

Los scopes en Python son solo cuatro: local (función), enclosing (funciones externas),
global (módulo) y built-in, la regla **LEGB** que retomamos con closures.

## Resumen

- Comparaciones encadenadas: `0 <= i < n`.
- `and`/`or` devuelven operandos: `x or default`.
- Guardas con retorno temprano en lugar de `if` anidados.
- `for/else` y `while/else`: el `else` corre si no hubo `break`.
- `while` solo cuando no sabés cuántas vueltas; walrus para "leer mientras haya".
- Los bloques no crean scope.

## Ejercicio

Cuatro funciones clásicas de control de flujo, escritas de forma idiomática.

**Para profundizar:** [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
(tutorial oficial).
