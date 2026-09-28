# Pipelines perezosos

Con generadores se puede construir un **pipeline**: una cadena de pasos (leer, parsear,
filtrar, transformar, agregar) en la que cada elemento atraviesa todas las etapas antes de
que se lea el siguiente. El resultado es código modular, fácil de testear por partes y que
procesa archivos de cualquier tamaño con **memoria constante**.

## La idea

```python
def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        yield from f

def parsear(lineas):
    for linea in lineas:
        ip, metodo, ruta, status, bytes_ = linea.split()
        yield {"ip": ip, "status": int(status), "bytes": int(bytes_)}

def solo_errores(registros):
    return (r for r in registros if r["status"] >= 500)

errores = solo_errores(parsear(leer("access.log")))
for e in errores:
    print(e)
```

Hasta que el `for` pide el primer elemento, **no se leyó ni una línea**. Después, el flujo es:

```
for pide → solo_errores pide → parsear pide → leer lee UNA línea
         ← filtra (o pide otra)  ← parsea          ←
```

En cada momento hay en memoria **un solo registro**, no el archivo entero. Un archivo de 50 GB
se procesa igual que uno de 50 KB.

## Comparado con la versión "ansiosa"

```python
lineas = open(ruta).readlines()                    # todo el archivo en memoria
registros = [parsear_linea(l) for l in lineas]     # otra copia, más grande
errores = [r for r in registros if r["status"] >= 500]
```

Cada paso materializa una lista completa. Funciona con archivos chicos y revienta con los
grandes. Además, no puede "cortar antes": si solo querés los primeros 10 errores, igual
procesa todo.

## Cortar antes: `islice`, `next`, `any`

Como el pipeline es perezoso, **pedir menos es trabajar menos**:

```python
from itertools import islice

primeros_10 = list(islice(errores, 10))            # lee solo lo necesario
hay_error = any(r["status"] >= 500 for r in regs)  # corta en el primero
primer_admin = next((u for u in usuarios if u.admin), None)
```

`islice(it, n)` es el "slicing" de los iteradores, que no admiten `it[:10]`.

## Etapas como funciones pequeñas

Cada etapa recibe un iterable y devuelve un iterable. Esto tiene varias ventajas:

- **Se testean solas**: `list(parsear(["1.2.3.4 GET / 200 512"]))`, sin archivos.
- **Se combinan** en el orden que haga falta.
- **Se reutilizan**: `solo_errores` sirve para registros que vengan de un archivo, de una API o
  de una base.

Una convención útil es que la **última** etapa sea la que materializa o agrega (`list`, `sum`,
`Counter`, `dict`, escribir a un archivo) y que todas las anteriores sean perezosas.

## Agrupar en lotes

Muchas veces el destino prefiere recibir de a muchos: inserts en una base, llamadas a una API
con límite de tamaño. El patrón clásico usa `islice` y el operador walrus:

```python
from itertools import islice

def en_lotes(iterable, n):
    it = iter(iterable)                     # ¡importante! un solo iterador compartido
    while lote := tuple(islice(it, n)):
        yield lote

for lote in en_lotes(registros, 1000):
    db.insert_many(lote)
```

El `iter()` del principio es clave: si `iterable` es una lista, cada `islice(lista, n)`
empezaría de nuevo desde el principio y el bucle sería infinito.

Desde Python 3.12 existe `itertools.batched(iterable, n)`, que hace lo mismo.

## Manejo de errores en una etapa

En datos reales siempre hay líneas mal formadas. Lo habitual es que la etapa de parseo las
**saltee y lleve la cuenta** (o las loguee), en lugar de romper todo el pipeline:

```python
def parsear(lineas):
    for n, linea in enumerate(lineas, start=1):
        try:
            ip, _, _, status, bytes_ = linea.split()
            yield ip, int(status), int(bytes_)
        except ValueError:
            log.warning("línea %d inválida: %r", n, linea)
```

## Cuidados

- **Un pipeline se consume una vez.** Si necesitás dos resultados (por ejemplo, total y top
  10), o hacés las dos cosas en una sola pasada o volvés a armar el pipeline.
- **El archivo tiene que seguir abierto** mientras se consume. Si `leer()` abre con `with`
  **dentro** del generador, está bien. Si abrís con `with` afuera y devolvés el generador
  fuera del bloque, vas a leer un archivo cerrado.
- **Los errores aparecen tarde**: una excepción en `parsear` recién salta cuando alguien
  consume, lejos de donde armaste el pipeline.

## Resumen

- Encadená generadores: cada etapa recibe un iterable y devuelve otro.
- Memoria constante y posibilidad de cortar temprano con `islice`, `next` o `any`.
- La última etapa materializa o agrega.
- Lotes con `iter()` + `islice` + walrus (o `itertools.batched` en 3.12+).
- Saltear y registrar los datos malos en lugar de romper el pipeline.

## Ejercicio

Un pipeline sobre una fuente infinita, lotes perezosos y un mini analizador de logs de
acceso armado por etapas.

**Para profundizar:** David Beazley, [Generator Tricks for Systems Programmers](https://www.dabeaz.com/generators/)
(clásico, sigue vigente).
