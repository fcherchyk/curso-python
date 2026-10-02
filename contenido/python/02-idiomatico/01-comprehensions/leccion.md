# Comprehensions

Una *comprehension* construye una colección nueva a partir de un iterable en una sola
expresión. Es la forma idiomática de hacer "map + filter" en Python. Bien usada, reemplaza
bucles de cuatro o cinco líneas por una que se lee casi como la definición matemática
de un conjunto.

## La idea: de bucle a expresión

El patrón que las comprehensions reemplazan es este:

```python
resultado = []
for x in nums:
    if x % 2 == 0:
        resultado.append(x * x)
```

La versión con comprehension se lee en el mismo orden: *qué* se produce, *de dónde* sale
y *con qué condición*:

```python
resultado = [x * x for x in nums if x % 2 == 0]
#            ^^^^^ ^^^^^^^^^^^^^^ ^^^^^^^^^^^^^^
#            expr  iteración      filtro (opcional)
```

Además de ser más corta, tiene tres ventajas concretas:

1. **Intención explícita.** Un `for` con `append` puede hacer cualquier cosa y lo tenés que
   leer entero. Una comprehension siempre construye una colección, y eso se ve de entrada.
2. **Sin estado intermedio.** No hay una lista vacía que después se va llenando: el resultado
   existe completo o no existe.
3. **Es más rápida.** Se ejecuta con bytecode especializado y evita buscar `resultado.append`
   en cada vuelta. Esto no suele ser lo decisivo, pero suma.

## Los cuatro sabores

```python
nums = [3, 1, 4, 1, 5, 9, 2, 6]

cuadrados = [x * x for x in nums]                 # list
unicos    = {x for x in nums}                     # set  -> {1, 2, 3, 4, 5, 6, 9}
por_nombre = {u.nombre: u for u in usuarios}      # dict
total     = sum(x * x for x in nums)              # generator expression
```

- **List** `[...]`: el caso general. Respeta el orden y admite repetidos.
- **Set** `{...}`: elimina duplicados. Sirve para preguntas como "¿qué dominios aparecen?".
- **Dict** `{k: v ...}`: arma índices y mapeos. Si una clave se repite, **gana la última**.
- **Generator expression** `(...)`: no construye nada en memoria. Produce los valores de a uno
  cuando alguien los pide. Si es el único argumento de una función, los paréntesis extra se
  omiten: `sum(x for x in xs)`, `any(...)`, `max(...)`, `"".join(...)`.

> No existe la "tuple comprehension". `(x for x in xs)` es un generador; si necesitás una
> tupla, usá `tuple(x for x in xs)`.

## Filtrar vs. transformar condicionalmente

Hay dos lugares donde puede ir un `if`, y hacen cosas distintas:

```python
# Filtro: el if va AL FINAL. Descarta elementos.
[x for x in nums if x > 2]              # [3, 4, 5, 9, 6]

# Expresión condicional: el if/else va AL PRINCIPIO. Transforma todos.
["par" if x % 2 == 0 else "impar" for x in nums]
```

El filtro no lleva `else`; la expresión condicional lo necesita siempre. Se pueden combinar
los dos, pero a esa altura conviene preguntarse si no se lee mejor con un bucle.

## Comprehensions anidadas

Los `for` se escriben **en el mismo orden en que los anidarías** con bucles:

```python
matriz = [[1, 2, 3], [4, 5, 6]]

# for fila in matriz:
#     for x in fila:
#         ...
plano = [x for fila in matriz for x in fila]      # [1, 2, 3, 4, 5, 6]

# Una comprehension DENTRO de otra construye estructuras anidadas:
transpuesta = [[fila[i] for fila in matriz] for i in range(3)]
# [[1, 4], [2, 5], [3, 6]]
```

La primera forma (dos `for` seguidos) **aplana**. La segunda (una comprehension como
expresión de otra) **anida**. Es fácil confundirlas: si dudás, escribí los bucles en un papel.

## Dict comprehensions: patrones típicos

```python
precios = {"pan": 1200, "leche": 1500, "café": 9800}

# Invertir un dict (solo si los valores son únicos y hashables)
por_precio = {v: k for k, v in precios.items()}

# Filtrar un dict
caros = {k: v for k, v in precios.items() if v > 1400}

# Transformar valores
con_iva = {k: round(v * 1.21) for k, v in precios.items()}

# Índice por id a partir de una lista de objetos
por_id = {p.id: p for p in productos}
```

Para construir un dict a partir de **pares** que ya tenés, no hace falta comprehension:
`dict(zip(claves, valores))` es más directo.

## Alcance de la variable

Desde Python 3, la variable de una comprehension es **local** a la comprehension y no
"se filtra" afuera:

```python
x = "afuera"
cuadrados = [x * x for x in range(3)]
print(x)   # "afuera"
```

Un bucle `for` común, en cambio, deja la variable definida con el último valor. Es una
diferencia más a favor de las comprehensions.

## Cuándo NO usarlas

- **Para efectos secundarios.** `[print(x) for x in xs]` crea una lista de `None` que se tira.
  Si lo que querés es *hacer* algo, usá un `for`.
- **Cuando la lógica no entra en una línea legible.** Como regla práctica, más de un `if` o más
  de dos `for` es señal de que conviene un bucle o una función auxiliar con nombre.
- **Cuando necesitás cortar antes.** Una comprehension recorre todo. Para "el primer elemento
  que cumple X" usá `next((x for x in xs if cond(x)), None)`.
- **Con datos enormes que vas a recorrer una sola vez.** Ahí conviene un generator expression:
  `sum(len(l) for l in archivo)` no carga el archivo entero en memoria.

## Trampas comunes

```python
# 1. El orden de los for anidados al revés -> NameError o resultado incorrecto
[x for x in fila for fila in matriz]      # ✗ `fila` todavía no existe

# 2. Olvidar que el set pierde el orden
{x for x in [3, 1, 2]}                    # el orden de iteración no está garantizado

# 3. Claves repetidas en dict comprehensions: la última pisa
{len(p): p for p in ["ab", "cd"]}         # {2: 'cd'}

# 4. Consumir dos veces un generator expression
gen = (x * 2 for x in range(3))
list(gen)   # [0, 2, 4]
list(gen)   # []  <- ya se agotó
```

## Resumen

| Querés…                              | Usá                                   |
|--------------------------------------|---------------------------------------|
| transformar y/o filtrar una lista    | `[f(x) for x in xs if cond(x)]`       |
| valores únicos                       | `{f(x) for x in xs}`                  |
| índice o mapeo                       | `{k(x): v(x) for x in xs}`            |
| agregar (suma, máximo, all/any)      | `sum(f(x) for x in xs)`               |
| aplanar un nivel                     | `[y for x in xs for y in x]`          |
| el primero que cumple algo           | `next((x for x in xs if c(x)), None)` |

## Ejercicio

En la pestaña **Código** vas a implementar cuatro funciones, cada una con una sola
comprehension: filtrar y transformar, aplanar, invertir un dict y extraer valores únicos.

**Para profundizar:** [Python Tutorial — List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions),
*Fluent Python* (2.ª ed.), cap. 2.
