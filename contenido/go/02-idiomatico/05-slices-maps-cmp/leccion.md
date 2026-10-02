# Los paquetes slices, maps y cmp

Durante años, en Go había que escribir a mano cada "buscar en un slice" u "obtener las
claves de un map", porque no había genéricos. Desde Go 1.21, los paquetes **`slices`**,
**`maps`** y **`cmp`** de la stdlib traen esas operaciones listas y tipadas. Son el
equivalente de `sorted`, `min`/`max` con `key` y los *builtins* de colecciones de Python.

## `slices`: operaciones sobre slices

```go
import "slices"

xs := []int{3, 1, 4, 1, 5}

slices.Contains(xs, 4)            // true
slices.Index(xs, 1)               // 1 (-1 si no está)
slices.Max(xs), slices.Min(xs)    // 5, 1 (panic si está vacío)
slices.Sort(xs)                   // ordena EN EL LUGAR: [1 1 3 4 5]
slices.BinarySearch(xs, 4)        // (3, true): búsqueda binaria en un slice ordenado
slices.Reverse(xs)                // en el lugar
slices.Equal(a, b)                // comparar elemento a elemento
slices.Compact(xs)                // saca los repetidos CONSECUTIVOS
c := slices.Clone(xs)             // copia independiente
```

Varias de estas funciones **modifican en el lugar** (`Sort`, `Reverse`) y otras **devuelven un
slice nuevo que hay que reasignar** (`Compact`, `Delete`, `Insert`), igual que `append`.

## Ordenar con criterio: `SortFunc` y `cmp.Compare`

`slices.SortFunc` recibe una función de comparación que devuelve un número **negativo**, cero
o **positivo**, como el viejo `cmp` de Python 2 (o `functools.cmp_to_key`):

```go
import "cmp"

type Persona struct {
    Nombre string
    Edad   int
}

// Por edad ascendente
slices.SortFunc(personas, func(a, b Persona) int {
    return cmp.Compare(a.Edad, b.Edad)
})

// Por edad DESCENDENTE y, a igual edad, por nombre ascendente
slices.SortFunc(personas, func(a, b Persona) int {
    return cmp.Or(
        cmp.Compare(b.Edad, a.Edad),        // invertir a/b = descendente
        cmp.Compare(a.Nombre, b.Nombre),
    )
})
```

- `cmp.Compare(x, y)` devuelve -1, 0 o 1 para cualquier tipo ordenable (`cmp.Ordered`).
- `cmp.Or(a, b, c)` devuelve el **primer valor distinto de cero**: el desempate por varios
  criterios queda en una línea, como una tupla en el `key=` de Python.
- `slices.SortStableFunc` es **estable**: los elementos iguales conservan su orden (el
  `sort` de Python siempre lo es; `SortFunc` no garantiza estabilidad).

## Máximos y mínimos con criterio

```go
masCaro := slices.MaxFunc(productos, func(a, b Producto) int {
    return cmp.Compare(a.Precio, b.Precio)
})
```

Ojo: `Max`, `Min`, `MaxFunc` y `MinFunc` **hacen panic con un slice vacío**. Chequeá
`len(xs) > 0` antes, o devolvé un `ok bool`. Ante empates, `MaxFunc` devuelve el **primero**.

## `maps`: claves, valores y clonado

```go
import "maps"

m := map[string]int{"b": 2, "a": 1}

claves := slices.Sorted(maps.Keys(m))      // ["a" "b"]: claves ordenadas (1.23+)
valores := slices.Collect(maps.Values(m))  // sin orden garantizado
c := maps.Clone(m)
maps.Equal(m, c)                           // true
maps.DeleteFunc(m, func(k string, v int) bool { return v < 2 })
```

`maps.Keys` y `maps.Values` devuelven **iteradores** (próximo capítulo), no slices. Por eso se
combinan con `slices.Sorted` o `slices.Collect`.

## `cmp.Or` para defaults

`cmp.Or` también sirve para "el primer valor no vacío", como `a or b or c` en Python:

```go
puerto := cmp.Or(os.Getenv("PORT"), config.Puerto, "8080")
```

## Los builtins `min` y `max` (1.21)

Para comparar pocos valores sueltos no hace falta ningún paquete:

```go
min(a, b, c)
max(x, 0)          // "al menos 0"
```

## Comparación con Python

| Python                                   | Go                                                  |
|------------------------------------------|-----------------------------------------------------|
| `x in xs`                                | `slices.Contains(xs, x)`                            |
| `xs.sort()`                              | `slices.Sort(xs)`                                   |
| `sorted(xs, key=lambda p: (-p.edad, p.nombre))` | `slices.SortFunc(xs, func(a, b P) int { return cmp.Or(...) })` |
| `max(xs, key=...)`                       | `slices.MaxFunc(xs, ...)` (panic si está vacío)     |
| `sorted(d)`                              | `slices.Sorted(maps.Keys(d))`                       |
| `dict(d)`                                | `maps.Clone(d)`                                     |
| `a or b or c`                            | `cmp.Or(a, b, c)`                                   |
| `min(a, b)`                              | `min(a, b)`                                         |

## Resumen

- `slices`: Contains, Index, Sort, SortFunc, BinarySearch, Max/Min, Equal, Clone, Compact…
- Cuidado con cuáles modifican en el lugar y cuáles devuelven un slice nuevo.
- `cmp.Compare` + `cmp.Or` para ordenar por varios criterios; invertí `a`/`b` para ordenar al
  revés.
- `SortStableFunc` si necesitás estabilidad.
- `slices.Sorted(maps.Keys(m))` para recorrer un map en orden.
- `MaxFunc`/`MinFunc` hacen panic con slices vacíos.

## Ejercicio

Ordenar por varios criterios, el máximo con criterio y un `ok`, claves ordenadas y un "top N".

**Para profundizar:** [paquete slices](https://pkg.go.dev/slices), [maps](https://pkg.go.dev/maps),
[cmp](https://pkg.go.dev/cmp).
