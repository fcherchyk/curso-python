# Closures y scopes

Una **closure** es una función que recuerda variables del lugar donde se definió, aunque ese
lugar ya haya terminado de ejecutarse. Es el mecanismo que hace posibles los decoradores,
las fábricas de funciones y buena parte del estado "privado" en Python sin escribir clases.

## La regla LEGB

Cuando Python encuentra un nombre, lo busca en este orden:

1. **L**ocal: la función actual.
2. **E**nclosing: las funciones que la contienen, de adentro hacia afuera.
3. **G**lobal: el módulo.
4. **B**uilt-in: `len`, `print`, `range`…

```python
x = "global"

def externa():
    x = "enclosing"
    def interna():
        return x            # no está en local → la encuentra en enclosing
    return interna

externa()()                 # 'enclosing'
```

## Qué es una closure

```python
def crear_multiplicador(k):
    def multiplicar(x):
        return x * k        # k es una variable "libre": viene de afuera
    return multiplicar

doble = crear_multiplicador(2)
triple = crear_multiplicador(3)
doble(5), triple(5)         # (10, 15)
```

Cuando `crear_multiplicador` termina, su variable `k` debería desaparecer. Pero `multiplicar`
la usa, así que Python la conserva en una **celda** asociada a la función:

```python
doble.__closure__[0].cell_contents   # 2
```

Cada llamada a `crear_multiplicador` crea un scope nuevo, así que `doble` y `triple` tienen
cada una su propio `k`.

## Modificar variables de afuera: `nonlocal`

Leer una variable del scope externo funciona solo. **Asignarla** no, porque cualquier
asignación dentro de una función crea una variable **local**:

```python
def crear_contador():
    total = 0
    def incrementar():
        total += 1          # UnboundLocalError: `total` es local y se lee antes de asignarse
        return total
    return incrementar
```

`nonlocal` le avisa a Python que el nombre pertenece al scope que la contiene:

```python
def crear_contador():
    total = 0
    def incrementar():
        nonlocal total
        total += 1
        return total
    return incrementar

c = crear_contador()
c(), c(), c()               # (1, 2, 3)
```

Si lo que capturás es un objeto **mutable** y solo lo modificás (sin reasignar el nombre),
no hace falta `nonlocal`:

```python
def crear_historial():
    eventos = []
    def registrar(e):
        eventos.append(e)   # muta el objeto, no reasigna el nombre
        return list(eventos)
    return registrar
```

Su pariente `global` hace lo mismo con variables del módulo. Casi nunca es buena idea: el
estado global complica los tests y el razonamiento sobre el código.

## La trampa clásica: *late binding*

Las closures capturan **variables, no valores**. El valor se busca **cuando se llama** a la
función, no cuando se crea:

```python
funciones = [lambda: i for i in range(3)]
[f() for f in funciones]    # [2, 2, 2]  ← ¡no [0, 1, 2]!
```

Las tres lambdas comparten la misma variable `i`, que al final del bucle vale 2. Dos
soluciones:

```python
# 1. Default argument: se evalúa al DEFINIR, así que congela el valor actual
funciones = [lambda i=i: i for i in range(3)]

# 2. Una fábrica: cada llamada crea un scope nuevo con su propio valor
def crear(i):
    return lambda: i
funciones = [crear(i) for i in range(3)]
```

Esta trampa aparece también con callbacks creados en un bucle (botones de una interfaz,
tareas programadas, etc.).

## Closure o clase

Una closure con estado es, en el fondo, un objeto con un solo método:

```python
# Closure
def crear_promediador():
    valores = []
    def agregar(x):
        valores.append(x)
        return sum(valores) / len(valores)
    return agregar

# Clase equivalente
class Promediador:
    def __init__(self):
        self.valores = []
    def __call__(self, x):
        self.valores.append(x)
        return sum(self.valores) / len(self.valores)
```

Usá una **closure** cuando hay una sola operación y poco estado. Pasá a una **clase** cuando
hacen falta varios métodos, cuando querés inspeccionar el estado desde afuera o cuando el
estado crece.

## Resumen

- LEGB: local → enclosing → global → built-in.
- Una closure conserva las variables del scope donde se definió.
- Para **reasignar** una variable externa hace falta `nonlocal`; para mutar un objeto, no.
- *Late binding*: las closures ven el valor al momento de **llamarse**. Solución: un default
  argument o una fábrica.
- Una closure con estado es un objeto con un solo método; si crece, usá una clase.

## Ejercicio

Un contador con `nonlocal`, multiplicadores creados en un bucle (esquivando la trampa del
*late binding*) y un promediador acumulativo.

**Para profundizar:** [Naming and binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding),
*Fluent Python*, cap. 9.
