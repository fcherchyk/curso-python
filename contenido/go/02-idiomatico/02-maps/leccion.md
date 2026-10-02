# Maps

El `map` es el diccionario de Go: una tabla hash de clave a valor, con búsqueda en O(1)
promedio. Funciona como el `dict` de Python, pero con tipos fijos para claves y valores,
**sin orden garantizado** y con un par de trampas que conviene conocer desde el principio.

## Crear y usar

```go
edades := map[string]int{"ana": 31, "beto": 27}   // literal
stock := make(map[string]int)                      // vacío, listo para usar
var nulo map[string]int                            // nil: se puede LEER, pero NO escribir

edades["caro"] = 40          // insertar o reemplazar
e := edades["ana"]           // 31
x := edades["zoe"]           // 0 ← clave inexistente: devuelve el ZERO VALUE, no falla
delete(edades, "beto")       // borrar (no falla si no existe)
len(edades)                  // cantidad de pares
```

### ⚠️ Escribir en un map `nil` es un panic

```go
var m map[string]int
m["a"] = 1           // panic: assignment to entry in nil map
```

Leer de un map `nil` devuelve zero values sin problema; escribir, no. Inicializá siempre con
`make` o con un literal.

## "Comma ok": ¿existe la clave?

Como leer una clave inexistente devuelve el zero value, no se puede distinguir "vale 0" de
"no está" sin el segundo resultado:

```go
edad, ok := edades["zoe"]
if !ok {
    fmt.Println("no está")
}

if _, existe := edades["ana"]; existe { ... }
```

Es el equivalente de `k in d` y de `d.get(k)` de Python.

## Aprovechar el zero value

Como una clave ausente da el zero value, muchos patrones salen sin `if`:

```go
// Contar (como Counter)
conteo := make(map[string]int)
for _, p := range palabras {
    conteo[p]++                    // si no existía, arranca en 0
}

// Agrupar (como defaultdict(list))
grupos := make(map[byte][]string)
for _, p := range palabras {
    grupos[p[0]] = append(grupos[p[0]], p)   // append sobre nil funciona
}
```

## Recorrer: el orden es aleatorio

```go
for clave, valor := range edades { ... }
for clave := range edades { ... }
```

El orden de iteración **no está definido y cambia entre ejecuciones**, a propósito: el
runtime lo aleatoriza para que nadie dependa de él. Si necesitás orden, ordená las claves:

```go
claves := slices.Sorted(maps.Keys(edades))    // Go 1.23+
for _, k := range claves {
    fmt.Println(k, edades[k])
}
```

## Sets: `map[T]struct{}` o `map[T]bool`

Go no tiene un tipo set. Se usa un map:

```go
vistos := make(map[string]struct{})    // struct{} no ocupa memoria
vistos["ana"] = struct{}{}
if _, ok := vistos["ana"]; ok { ... }

// Más legible, a costa de 1 byte por entrada:
activos := map[string]bool{"ana": true}
if activos["ana"] { ... }              // la clave ausente da false
```

## Qué puede ser clave

La clave tiene que ser **comparable** con `==`: números, strings, booleanos, punteros,
arrays y structs formados por campos comparables. **Los slices, los maps y las funciones no
pueden ser claves.** Un struct sirve como clave compuesta:

```go
type Coord struct{ X, Y int }
visitado := map[Coord]bool{{0, 0}: true}
```

## Los maps son referencias

Como los slices, un map se pasa "por valor", pero lo que se copia es un puntero a la tabla:
**una función que recibe un map puede modificarlo**, y el cambio se ve afuera. Para una copia
independiente, `maps.Clone(m)`.

## ⚠️ Los maps no son seguros para concurrencia

Leer y escribir un mismo map desde varias goroutines sin sincronizar es un error fatal
(`concurrent map writes`). Se protege con un `sync.Mutex` o se usa `sync.Map` (módulo de
concurrencia).

## Comparación con Python

| Python                         | Go                                              |
|--------------------------------|-------------------------------------------------|
| `d = {}`                       | `m := map[string]int{}` o `make(...)`           |
| `d[k]` con `KeyError`          | `m[k]` devuelve el zero value                   |
| `k in d`                       | `_, ok := m[k]`                                 |
| `d.get(k, 0)`                  | `m[k]` (si 0 es el default)                     |
| `Counter`, `defaultdict(list)` | el zero value lo resuelve: `m[k]++`, `append`   |
| dict ordenado por inserción    | orden aleatorio: ordená las claves              |
| `set()`                        | `map[T]struct{}`                                |
| `del d[k]`                     | `delete(m, k)`                                  |

## Resumen

- `make(map[K]V)` o un literal; escribir en un map nil hace panic.
- Una clave ausente devuelve el zero value; usá `v, ok := m[k]` para distinguir.
- `m[k]++` y `m[k] = append(m[k], v)` funcionan sin inicializar la clave.
- El orden de iteración es aleatorio: `slices.Sorted(maps.Keys(m))`.
- Sets con `map[T]struct{}`; claves compuestas con structs.
- No son seguros para concurrencia.

## Ejercicio

Contar palabras, agrupar, invertir un map ordenando los resultados y una intersección con un
set.

**Para profundizar:** [Go maps in action](https://go.dev/blog/maps),
[paquete maps](https://pkg.go.dev/maps).
