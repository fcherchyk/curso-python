# Generadores

Un **generador** es una función que, en lugar de calcular todo y devolverlo, **produce los
valores de a uno**, cuando alguien los pide. Es la forma más simple de escribir un iterador:
nada de clases con `__next__`, solo `yield`.

## `yield` convierte una función en generador

```python
def cuenta_regresiva(n):
    print("arranca")
    while n > 0:
        yield n
        n -= 1
    print("terminó")

g = cuenta_regresiva(3)    # ¡no imprime nada! solo crea el generador
next(g)                    # imprime "arranca", devuelve 3
next(g)                    # 2
next(g)                    # 1
next(g)                    # imprime "terminó" y levanta StopIteration
```

Qué conviene observar:

1. Llamar a la función **no ejecuta el cuerpo**: devuelve un objeto generador.
2. Cada `next()` ejecuta hasta el siguiente `yield`, entrega ese valor y **se pausa**,
   conservando las variables locales y la posición.
3. Cuando la función termina (o hace `return`), el generador levanta `StopIteration`.

Por eso los generadores son **perezosos** (*lazy*): no calculan nada que nadie haya pedido.

## Por qué importa: memoria y composición

```python
def cuadrados_lista(n):
    return [i * i for i in range(n)]      # construye n elementos en memoria

def cuadrados_gen(n):
    for i in range(n):
        yield i * i                        # un elemento a la vez

sum(cuadrados_lista(10**8))   # ~4 GB de RAM
sum(cuadrados_gen(10**8))     # memoria constante
```

Además, un generador puede ser **infinito**, porque solo produce lo que se consume:

```python
def naturales():
    n = 0
    while True:
        yield n
        n += 1

from itertools import islice
list(islice(naturales(), 5))   # [0, 1, 2, 3, 4]
```

## Generator expressions

Para casos simples, la sintaxis de comprehension con paréntesis crea un generador sin
escribir una función:

```python
cuadrados = (i * i for i in range(10))
total = sum(len(linea) for linea in archivo)       # sin paréntesis extra si es el único argumento
```

Regla práctica: si entra en una línea legible, usá una generator expression; si necesita
estado, varios pasos o `try`, escribí una función con `yield`.

## `yield from`: delegar en otro iterable

`yield from iterable` produce todos los elementos de `iterable`, uno por uno. Es ideal para
**recursión**:

```python
def recorrer(nodo):
    yield nodo.valor
    for hijo in nodo.hijos:
        yield from recorrer(hijo)
```

Sin `yield from`, habría que escribir `for x in recorrer(hijo): yield x`.

## Generadores con estado

Un generador es una forma muy natural de expresar algoritmos que "recuerdan" algo entre
un paso y el siguiente:

```python
def promedios_moviles(valores):
    total = 0
    for i, v in enumerate(valores, start=1):
        total += v
        yield total / i

list(promedios_moviles([10, 20, 30]))   # [10.0, 15.0, 20.0]
```

## Limpieza: `try/finally` y `with` adentro de un generador

Si el generador abre un recurso, usá `with` adentro. Cuando el generador termina, o cuando
se destruye sin terminar (por ejemplo, al salir de un `for` con `break`), Python llama a
`gen.close()` y el recurso se libera:

```python
def lineas(ruta):
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            yield linea.rstrip("\n")
```

## Lo avanzado (para reconocerlo)

- `return valor` dentro de un generador termina la iteración; el valor viaja en
  `StopIteration.value` y es lo que devuelve `yield from`.
- `gen.send(x)` le manda un valor al generador (el `yield` lo recibe como resultado). Es la
  base histórica de las corrutinas; hoy, para concurrencia, se usa `async`/`await`.
- `gen.throw(exc)` y `gen.close()` inyectan una excepción o lo cierran.

No los vas a necesitar seguido, pero aparecen en librerías y en entrevistas.

## Cuándo **no** usar un generador

- Si vas a recorrer el resultado varias veces, o necesitás `len()`, índices o slicing:
  devolvé una lista.
- Si el conjunto es chico y lo vas a usar entero: una lista es más simple de depurar.
- Si la función tiene efectos secundarios que tienen que ocurrir **ya**: recordá que el cuerpo
  no corre hasta que alguien itera. Un generador que nadie consume no hace nada.

## Resumen

- `yield` pausa la función y entrega un valor; el cuerpo corre recién al iterar.
- Los generadores usan memoria constante y pueden ser infinitos.
- `(expr for x in xs)` para casos de una línea; `def` con `yield` para lógica con estado.
- `yield from` delega, ideal para recursión.
- Son iteradores: se consumen una sola vez.

## Ejercicio

Cuatro generadores: uno infinito, un filtro de líneas, un aplanado recursivo con `yield from`
y un `range` para decimales.

**Para profundizar:** [PEP 255 — Simple Generators](https://peps.python.org/pep-0255/),
[PEP 380 — yield from](https://peps.python.org/pep-0380/), *Fluent Python*, cap. 17.
