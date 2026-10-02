# El operador walrus `:=`

El operador `:=` (3.8), apodado *walrus* ("morsa") por su forma, **asigna y devuelve** el
valor dentro de una expresión. Su objetivo no es ahorrar una línea, sino **eliminar
duplicación**: evitar calcular dos veces lo mismo o repetir una lectura antes y dentro de un
bucle.

## La diferencia con `=`

`=` es una **sentencia**: no se puede usar dentro de un `if`, de un `while` o de una
comprehension. `:=` es una **expresión**: produce un valor y, de paso, lo guarda en un nombre.

```python
if (n := len(datos)) > 10:
    print(f"demasiados datos: {n}")
```

Sin walrus habría que calcular `len(datos)` dos veces o agregar una línea antes del `if`.

## Caso 1: leer hasta que no haya más

El patrón clásico de "leer, chequear, procesar, volver a leer":

```python
# Sin walrus: la lectura está duplicada
bloque = archivo.read(4096)
while bloque:
    procesar(bloque)
    bloque = archivo.read(4096)

# Con walrus: una sola lectura
while bloque := archivo.read(4096):
    procesar(bloque)
```

Funciona con cualquier fuente que devuelva algo falsy al terminar: `readline()`, `queue.get()`
con centinela, `socket.recv()` o `tuple(islice(it, n))` para lotes.

## Caso 2: regex

```python
import re

if m := re.match(r"(\d{4})-(\d{2})", texto):
    anio, mes = m.groups()
```

`re.match` devuelve un `Match` o `None`. Con walrus, el chequeo y el uso quedan juntos.

Encadenado con `elif`:

```python
if m := PATRON_FECHA.match(linea):
    ...
elif m := PATRON_HORA.match(linea):
    ...
```

## Caso 3: comprehensions que filtran por un valor calculado

```python
# Sin walrus: parsear() se llama DOS veces por elemento
resultados = [parsear(x) for x in datos if parsear(x) is not None]

# Con walrus: una sola vez
resultados = [r for x in datos if (r := parsear(x)) is not None]
```

Esto importa cuando la función es cara o tiene efectos secundarios.

## Caso 4: `any()` y "¿cuál fue?"

```python
if any((largo := len(linea)) > 80 for linea in lineas):
    print(f"hay una línea de {largo} caracteres")
```

Como `any` corta en el primer verdadero, la variable queda con el valor que lo disparó. El
nombre asignado dentro de una comprehension o generador queda disponible **afuera** (a
diferencia de la variable del `for`), justamente para permitir este patrón.

## Reglas y paréntesis

- En una sentencia suelta, `x := 5` es un error de sintaxis (usá `=`). En argumentos y
  comparaciones suelen hacer falta paréntesis: `if (n := len(xs)) > 10`.
- Sin paréntesis, `if n := len(xs) > 10` asigna a `n` el **booleano** `len(xs) > 10`. Es un
  bug clásico.
- No se puede usar para asignar atributos ni índices: `self.x := 1` no es válido.

## Cuándo **no** usarlo

```python
# ✗ No aporta nada: es un = disfrazado
print(total := calcular())

# ✗ Varias asignaciones en una línea: difícil de leer
if (a := f()) and (b := g(a)) and (c := h(b)): ...
```

Regla práctica: usalo si **quita** una duplicación o una línea que solo servía para preparar
un `if` o un `while`. Si hay que pensar para leerlo, escribilo en dos líneas.

## Resumen

- `:=` asigna y devuelve el valor dentro de una expresión.
- Casos típicos: `while x := leer()`, `if m := re.match(...)` y filtrar por un valor
  calculado en una comprehension.
- Paréntesis: `if (n := len(xs)) > 10`. Sin ellos, `n` recibe el booleano.
- Usalo para eliminar duplicación, no para compactar.

## Ejercicio

Leer en bloques, filtrar calculando una sola vez, extraer datos con regex y un bucle de
reintentos, todo con walrus.

**Para profundizar:** [PEP 572 — Assignment Expressions](https://peps.python.org/pep-0572/).
