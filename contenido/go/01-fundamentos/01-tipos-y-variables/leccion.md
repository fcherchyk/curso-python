# Tipos, variables y zero values

Go es un lenguaje **compilado y de tipado estático**, diseñado en Google para que el código
sea simple de leer, rápido de compilar y fácil de mantener en equipos grandes. Si venís de
Python, el cambio más grande es que **el compilador conoce el tipo de cada variable** y te
frena antes de ejecutar. A cambio, la sintaxis es deliberadamente chica: hay pocas formas de
hacer cada cosa.

## Un programa completo

```go
package main

import "fmt"

func main() {
    fmt.Println("hola, mundo")
}
```

- Todo archivo pertenece a un **paquete**. El paquete `main` con una función `main` es un
  ejecutable.
- `import` trae otros paquetes. Un import **sin usar es un error de compilación**, no un
  warning.
- Se ejecuta con `go run .` y se compila con `go build`, que produce un único binario sin
  dependencias.

## Declarar variables

```go
var nombre string = "Ana"   // forma completa
var edad = 31               // el tipo se infiere: int
ciudad := "Rosario"         // declaración corta (solo dentro de funciones)
var a, b int = 1, 2
x, y := 10, "diez"          // varios a la vez, de distinto tipo
```

- `:=` **declara y asigna**; `=` solo asigna a una variable que ya existe.
- `:=` solo funciona **dentro de funciones**. A nivel de paquete hay que usar `var`.
- Una variable local declarada y **no usada es un error de compilación**. Si realmente no la
  necesitás, asignala a `_`.

## Zero values: no hay "sin inicializar"

Toda variable declarada sin valor recibe el **valor cero** de su tipo:

| Tipo                          | Zero value |
|-------------------------------|------------|
| `int`, `float64`, …           | `0`        |
| `bool`                        | `false`    |
| `string`                      | `""`       |
| punteros, slices, maps, funciones, interfaces, channels | `nil` |
| structs                       | cada campo en su zero value |

```go
var n int       // 0
var s string    // ""
var activo bool // false
```

Esto evita el "variable no inicializada" de C y el `None` sorpresa de Python. El diseño
idiomático de Go busca que **el zero value sea útil**: un `strings.Builder` o un
`sync.Mutex` recién declarados ya se pueden usar.

## Los tipos básicos

```go
bool
string                          // inmutable, UTF-8
int  int8  int16  int32  int64  // con signo; int es de 64 bits en plataformas de 64 bits
uint uint8 uint16 uint32 uint64 // sin signo
byte                            // alias de uint8
rune                            // alias de int32: un code point Unicode
float32 float64
complex64 complex128
```

En la práctica: `int` para enteros, `float64` para decimales, `string`, `bool`, y `byte`/`rune`
cuando trabajás con texto a bajo nivel.

A diferencia de Python, los enteros **tienen tamaño fijo y pueden desbordar**:

```go
var x int8 = 127
x++            // -128: overflow silencioso
```

## Conversiones: siempre explícitas

Go **no convierte tipos automáticamente**, ni siquiera entre `int` y `float64`:

```go
a := 10
b := 2.5
c := a * b                  // error: mismatched types int and float64
c := float64(a) * b         // ✓ 25.0
d := int(b)                 // 2: trunca hacia cero
```

Para convertir entre texto y números se usa el paquete `strconv`, no un cast:

```go
n, err := strconv.Atoi("42")        // string → int (puede fallar: devuelve error)
s := strconv.Itoa(42)               // int → string
s2 := string(rune(65))              // "A": ¡string(65) NO da "65"!
```

## Constantes e `iota`

```go
const Pi = 3.14159
const (
    KB = 1 << (10 * (iota + 1))   // 1024
    MB                            // 1048576
    GB
)
```

Las constantes se evalúan al compilar. Las constantes numéricas sin tipo explícito son
*untyped*: tienen precisión arbitraria y se adaptan al tipo donde se usan.

`iota` vale 0, 1, 2… dentro de un bloque `const`, y es la forma idiomática de hacer
**enumeraciones**:

```go
type Dia int

const (
    Lunes Dia = iota   // 0
    Martes             // 1
    Miercoles          // 2
)
```

Declarar `type Dia int` crea un **tipo nuevo** basado en `int`. No se puede mezclar con un
`int` común sin convertir, y se le pueden agregar métodos (por ejemplo `String()`, en el
módulo de tipos).

## Visibilidad: mayúscula = exportado

No hay `public` ni `private`. Un nombre que empieza con **mayúscula** se exporta fuera del
paquete; con **minúscula**, es privado del paquete:

```go
func Sumar(a, b int) int { ... }   // exportada
func sumar(a, b int) int { ... }   // privada del paquete
```

Por eso, en los ejercicios, las funciones empiezan con mayúscula: los tests las usan.

## Comparación rápida con Python

| Python                     | Go                                      |
|----------------------------|-----------------------------------------|
| `x = 5`                    | `x := 5`                                |
| `None`                     | `nil` (solo para punteros, slices, maps…) |
| `int` sin límite           | `int` de 64 bits con overflow           |
| `float(x)`                 | `float64(x)`                            |
| `int("42")`                | `strconv.Atoi("42")` → `(int, error)`   |
| `_privado` por convención  | minúscula = privado de verdad           |
| `Enum`                     | `type X int` + `const (... iota)`       |

## Resumen

- `:=` dentro de funciones; `var` a nivel de paquete o cuando querés el zero value.
- Todo tiene zero value: `0`, `""`, `false` o `nil`.
- Las conversiones son siempre explícitas (`float64(n)`, `strconv.Atoi`).
- `iota` + un tipo propio para enumeraciones.
- Mayúscula = exportado. Las variables e imports sin usar no compilan.

## Ejercicio

Conversiones numéricas, un promedio con conversión `int` → `float64` y una enumeración con
`iota`.

**Para profundizar:** [A Tour of Go — Basics](https://go.dev/tour/basics/1),
[Effective Go](https://go.dev/doc/effective_go), [The Go spec: Constants](https://go.dev/ref/spec#Constants).
