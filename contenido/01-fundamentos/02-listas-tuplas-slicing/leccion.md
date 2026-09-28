# Listas, tuplas y slicing

Listas y tuplas son las dos secuencias de uso general. Se parecen mucho en la sintaxis, pero
cumplen roles distintos. En este capítulo repasamos cuándo usar cada una, las operaciones
que conviene tener a mano (con su costo) y el *slicing*, que funciona igual en listas,
tuplas, strings y `range`.

## Lista vs. tupla: no es solo "mutable vs. inmutable"

```python
precios = [1200, 1500, 980]          # lista: colección HOMOGÉNEA de largo variable
punto   = (3.5, -1.2)                # tupla: registro HETEROGÉNEO de largo fijo
persona = ("Ana", 31, "Rosario")     # cada posición tiene un significado
```

- Usá una **lista** cuando tenés "muchos de lo mismo" y vas a agregar, sacar u ordenar.
- Usá una **tupla** cuando cada posición significa algo distinto, como una fila, un par
  clave-valor o un punto. Que sea inmutable es un beneficio: se puede usar como clave de
  dict o elemento de un set, y nadie te la cambia.

```python
distancias = {("BA", "Rosario"): 300}     # tupla como clave: ✓
distancias = {["BA", "Rosario"]: 300}     # TypeError: unhashable type: 'list'
```

Detalles de sintaxis de las tuplas:

```python
t = 1, 2          # los paréntesis son opcionales; lo que crea la tupla es la coma
uno = (42,)       # tupla de un elemento: la coma es obligatoria
(42)              # esto es solo el int 42
vacia = ()
```

## Operaciones de lista y su costo

| Operación                      | Costo     | Nota                                   |
|--------------------------------|-----------|----------------------------------------|
| `xs[i]`, `xs[i] = v`           | O(1)      |                                        |
| `xs.append(x)`                 | O(1)*     | amortizado                             |
| `xs.pop()`                     | O(1)      | saca del final                         |
| `xs.pop(0)`, `xs.insert(0, x)` | **O(n)**  | corre todos los elementos: usá `deque` |
| `x in xs`                      | **O(n)**  | búsqueda lineal: usá un `set`          |
| `xs.extend(ys)` / `xs += ys`   | O(len ys) |                                        |
| `xs.sort()`                    | O(n log n)|                                        |
| `len(xs)`                      | O(1)      |                                        |

Las listas de Python son **arrays dinámicos**, no listas enlazadas. Operar al final es barato;
al principio es caro. Si necesitás una cola, `collections.deque` tiene `appendleft` y
`popleft` en O(1).

```python
xs = [3, 1, 2]
xs.append(4)          # [3, 1, 2, 4]
xs.extend([5, 6])     # agrega cada elemento (append agregaría la lista entera)
xs.insert(1, 9)       # inserta en la posición 1
xs.remove(9)          # saca la PRIMERA aparición del valor (ValueError si no está)
xs.pop()              # saca y devuelve el último
xs.index(2)           # posición de la primera aparición
xs.count(1)
del xs[0]             # borrar por índice
```

## Indexado negativo

```python
xs = ["a", "b", "c", "d"]
xs[-1]    # 'd'  último
xs[-2]    # 'c'  anteúltimo
```

`xs[-k]` equivale a `xs[len(xs) - k]`.

## Slicing: `[inicio:fin:paso]`

Un slice devuelve una **nueva** secuencia del mismo tipo. `inicio` es inclusivo y `fin`
exclusivo, igual que `range`:

```python
xs = [0, 1, 2, 3, 4, 5]

xs[1:4]     # [1, 2, 3]
xs[:3]      # [0, 1, 2]       los primeros 3
xs[3:]      # [3, 4, 5]       desde el 3 hasta el final
xs[-2:]     # [4, 5]          los últimos 2
xs[:-2]     # [0, 1, 2, 3]    todos menos los últimos 2
xs[::2]     # [0, 2, 4]       uno sí, uno no
xs[::-1]    # [5, 4, 3, 2, 1, 0]  invertido
xs[:]       # copia superficial
```

Una ventaja es que el slicing **nunca levanta `IndexError`**: si los límites se pasan, se
recortan.

```python
xs[10:20]   # []
xs[:100]    # toda la lista
```

Una buena forma de pensar los índices es que marcan los **bordes entre elementos**, no los
elementos:

```
 +---+---+---+---+
 | a | b | c | d |
 +---+---+---+---+
 0   1   2   3   4
-4  -3  -2  -1
```

Así `xs[1:3]` son los elementos entre el borde 1 y el borde 3: `b, c`. Y `xs[:k] + xs[k:]`
siempre reconstruye la lista completa.

### La trampa de `xs[-n:]` con `n = 0`

```python
n = 0
xs[-n:]     # ¡toda la lista! porque -0 == 0 y xs[0:] es todo
```

Si `n` puede ser 0, escribilo como `xs[len(xs) - n:]`.

### Asignar a un slice (solo listas)

```python
xs = [0, 1, 2, 3, 4]
xs[1:3] = ["a", "b", "c"]   # reemplaza (el largo puede cambiar): [0, 'a', 'b', 'c', 3, 4]
xs[:] = []                  # vacía la lista EN EL LUGAR (otros nombres ven el cambio)
del xs[::2]                 # borra uno sí, uno no
```

## Operadores sobre secuencias

```python
[1, 2] + [3]         # [1, 2, 3]   concatena (crea una nueva)
[0] * 3              # [0, 0, 0]   repite (ojo con repetir listas, ver capítulo anterior)
(1, 2) < (1, 3)      # True        comparación lexicográfica
3 in (1, 2, 3)       # True
min(xs), max(xs), sum(xs), len(xs)
```

## `range`: una secuencia perezosa

`range(inicio, fin, paso)` no crea una lista: calcula los valores a demanda. `range(10**12)`
ocupa lo mismo que `range(10)`. Soporta `len`, `in` (en O(1) para enteros), indexado y
slicing.

## Resumen

- Lista para colecciones homogéneas que cambian; tupla para registros de largo fijo (y como
  clave de dict).
- Operar al final de una lista es O(1); al principio, O(n) (para eso está `deque`).
- `x in lista` es O(n): si buscás mucho, usá un `set`.
- Slicing: `[inicio:fin:paso]`, fin exclusivo, nunca falla por rango y devuelve una copia.
- `xs[::-1]` invierte; `xs[:]` copia; `xs[-n:]` falla con `n = 0`.

## Ejercicio

Cuatro funciones que se resuelven con slicing, sin bucles.

**Para profundizar:** [Sequence types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range),
[TimeComplexity (wiki de Python)](https://wiki.python.org/moin/TimeComplexity).
