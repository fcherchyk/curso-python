# Slices a fondo

El slice es la estructura de datos más usada de Go: es la "lista" del lenguaje. Se ve simple,
pero para usarlo bien hay que entender qué es por dentro, porque de eso dependen el
rendimiento y un bug clásico: el **aliasing** (dos slices que comparten memoria sin que te
des cuenta).

## Arrays: la base (casi nunca los usás directo)

```go
var a [3]int            // [0 0 0]: el tamaño es parte del TIPO
b := [...]int{1, 2, 3}  // el compilador cuenta
```

Un array tiene tamaño fijo, y `[3]int` y `[4]int` son tipos distintos. Se copian enteros al
asignarlos o pasarlos. En el día a día se usan slices.

## Qué es un slice

Un slice es una **ventana** sobre un array. Por dentro es un struct de tres campos:

```
slice = { puntero al array, len, cap }
```

- `len(s)`: cuántos elementos ves.
- `cap(s)`: cuántos entran desde el inicio de la ventana hasta el final del array.

```go
s := []int{1, 2, 3}          // literal: crea el array y el slice
v := make([]int, 3)          // [0 0 0], len 3
w := make([]int, 0, 100)     // vacío, pero con lugar para 100 sin realocar
var nulo []int               // nil: len 0, se puede usar igual (append, range, len)
```

Un slice `nil` y uno vacío (`[]int{}`) se comportan igual para casi todo. Para preguntar
"¿está vacío?", usá `len(s) == 0`, nunca `s == nil`.

## `append`: la operación central

```go
s = append(s, 4)
s = append(s, 5, 6, 7)
s = append(s, otro...)       // concatenar
```

**Siempre** reasigná el resultado: `s = append(s, x)`. El motivo:

- si hay capacidad libre, `append` escribe en el mismo array y devuelve un slice con `len+1`;
- si no hay, **aloca un array nuevo** (más o menos del doble de tamaño), copia todo y
  devuelve un slice que apunta al nuevo.

El `s` viejo no se entera del cambio. Por eso `append` devuelve el slice.

Si sabés cuántos elementos vas a agregar, reservá capacidad de antemano con
`make([]T, 0, n)`: evitás realocaciones y copias.

## Rebanar: `s[i:j]`

```go
s := []int{0, 1, 2, 3, 4, 5}
a := s[1:4]       // [1 2 3]  len 3, cap 5  ← comparte el array con s
b := s[:2]        // [0 1]
c := s[3:]        // [3 4 5]
```

Igual que en Python, `i` es inclusivo y `j` exclusivo, pero con una diferencia enorme:
**rebanar NO copia**. `a` y `s` ven la misma memoria:

```go
a[0] = 100
fmt.Println(s)    // [0 100 2 3 4 5]  ← ¡s también cambió!
```

(En Go no hay índices negativos: `s[len(s)-1]` es el último.)

## La trampa del aliasing con `append`

```go
base := make([]int, 3, 10)      // [0 0 0], cap 10
x := append(base, 1)            // escribe en base[3]: hay capacidad
y := append(base, 2)            // ¡escribe en el MISMO lugar!
fmt.Println(x[3])               // 2  ← x cambió "sola"
```

`x` e `y` comparten el array de `base`. Es uno de los bugs más confusos de Go. Cuando
necesites un slice **independiente**, copiá:

```go
copia := slices.Clone(s)                     // Go 1.21+
copia := append([]int(nil), s...)            // forma clásica
n := copy(destino, origen)                   // copia min(len) elementos
```

Otra opción es limitar la capacidad con el *full slice expression* `s[i:j:k]`, así el próximo
`append` se ve obligado a realocar:

```go
sub := s[0:2:2]        // len 2, cap 2
sub = append(sub, 9)   // aloca: ya no toca s
```

## Operaciones comunes (con el paquete `slices`, 1.21+)

```go
slices.Contains(s, 3)
slices.Index(s, 3)                 // -1 si no está
slices.Reverse(s)                  // en el lugar
slices.Sort(s)
slices.Equal(a, b)
s = slices.Delete(s, i, j)         // borra s[i:j]
s = slices.Insert(s, i, v)
```

Sin el paquete, el idioma clásico para **filtrar en el lugar** reutiliza el mismo array:

```go
res := s[:0]
for _, v := range s {
    if v%2 == 0 {
        res = append(res, v)
    }
}
```

## Slices de slices

```go
matriz := make([][]int, filas)
for i := range matriz {
    matriz[i] = make([]int, columnas)
}
```

Cada fila es un slice independiente, y las filas pueden tener largos distintos.

## Comparación con Python

| Python                 | Go                                             |
|------------------------|------------------------------------------------|
| `xs = []`              | `var xs []int` o `xs := []int{}`               |
| `xs.append(x)`         | `xs = append(xs, x)` (¡reasignar!)             |
| `xs[1:3]` (copia)      | `xs[1:3]` (NO copia: comparte memoria)         |
| `xs[-1]`               | `xs[len(xs)-1]`                                |
| `list(xs)`, `xs[:]`    | `slices.Clone(xs)`                             |
| `x in xs`              | `slices.Contains(xs, x)`                       |
| `len(xs)`              | `len(xs)` (y además `cap(xs)`)                 |

## Resumen

- Un slice es `{puntero, len, cap}` sobre un array.
- `s = append(s, ...)` siempre: puede realocar.
- Rebanar no copia. Si necesitás independencia, `slices.Clone`/`copy` o `s[i:j:k]`.
- `make([]T, 0, n)` si conocés el tamaño.
- Vacío se pregunta con `len(s) == 0`; un slice nil se puede usar como vacío.

## Ejercicio

Filtrar, invertir en el lugar, partir en lotes y agregar **sin aliasing**.

**Para profundizar:** [Go Slices: usage and internals](https://go.dev/blog/slices-intro),
[Arrays, slices (and strings): the mechanics of append](https://go.dev/blog/slices),
[paquete slices](https://pkg.go.dev/slices).
