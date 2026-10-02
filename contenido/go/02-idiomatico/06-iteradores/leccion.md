# Iteradores: range sobre funciones

Hasta Go 1.22, `range` solo recorría slices, arrays, strings, maps y channels. Desde **Go
1.23**, también recorre **funciones iteradoras**. Es el equivalente de los generadores de
Python: secuencias perezosas, potencialmente infinitas, que se consumen con un `for` común.
La stdlib ya los usa (`maps.Keys`, `slices.All`, `strings.SplitSeq`).

## `range` sobre enteros (1.22)

Primero, lo más simple:

```go
for i := range 5 {      // 0, 1, 2, 3, 4
    fmt.Println(i)
}
```

## Qué es un iterador en Go

Un iterador es una **función que recibe una función `yield`** y la llama con cada valor:

```go
// paquete iter
type Seq[V any]     func(yield func(V) bool)
type Seq2[K, V any] func(yield func(K, V) bool)
```

```go
func Contar(desde, hasta int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := desde; i < hasta; i++ {
            if !yield(i) {       // quien consume hizo break → cortamos
                return
            }
        }
    }
}

for n := range Contar(1, 4) {    // 1, 2, 3
    fmt.Println(n)
}
```

Cómo funciona:

- El `for ... range` le pasa al iterador una función `yield` que ejecuta **el cuerpo del
  bucle**.
- `yield(v)` devuelve `true` si hay que seguir y `false` si el bucle hizo `break` (o
  `return`).
- **Hay que respetar ese `false`**: si seguís llamando a `yield` después de que devolvió
  `false`, el runtime hace panic.

Comparalo con Python:

```python
def contar(desde, hasta):
    for i in range(desde, hasta):
        yield i
```

La idea es la misma, con una diferencia de modelo: en Go el iterador **empuja** los valores
(*push*) llamando al cuerpo del bucle, mientras que el generador de Python los entrega cuando
se le piden (*pull*). En la práctica, se usan igual.

## Iteradores infinitos y perezosos

```go
func Naturales() iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := 0; ; i++ {
            if !yield(i) {
                return
            }
        }
    }
}

for n := range Naturales() {
    if n > 5 {
        break          // yield devuelve false y el iterador termina
    }
}
```

Nada se calcula de más: el iterador produce un valor por vez, **solo mientras el bucle lo
pide**.

## `Seq2`: pares clave-valor

```go
func Enumerar[T any](xs []T) iter.Seq2[int, T] {
    return func(yield func(int, T) bool) {
        for i, x := range xs {
            if !yield(i, x) {
                return
            }
        }
    }
}

for i, x := range Enumerar([]string{"a", "b"}) { ... }
```

## Componer: adaptadores

Como en los pipelines de Python, se pueden encadenar iteradores que transforman otros:

```go
func Filtrar[T any](seq iter.Seq[T], f func(T) bool) iter.Seq[T] {
    return func(yield func(T) bool) {
        for v := range seq {
            if f(v) && !yield(v) {
                return
            }
        }
    }
}

pares := Filtrar(Naturales(), func(n int) bool { return n%2 == 0 })
```

(El `[T any]` es un **genérico**: la función sirve para cualquier tipo. Los vemos en su
propio módulo; por ahora, leelo como "para cualquier T".)

## Iteradores de la stdlib

```go
slices.All(xs)          // Seq2[índice, valor]
slices.Values(xs)       // Seq[valor]
slices.Collect(seq)     // iterador → slice (como list(gen))
slices.Sorted(seq)      // iterador → slice ordenado
maps.Keys(m), maps.Values(m), maps.All(m)
strings.SplitSeq(s, ",")   // 1.24: partir sin crear el slice completo
strings.Lines(s)           // 1.24: recorrer líneas
```

## Cuándo usarlos

- **Sí**: secuencias grandes o infinitas, pipelines de transformación, recorrer estructuras
  propias (árboles, listas enlazadas) con un `for range`, y exponer datos sin alocar un slice.
- **No**: si ya tenés un slice chico y lo vas a recorrer varias veces, un slice es más simple
  y más rápido.

## Comparación con Python

| Python                               | Go                                                   |
|--------------------------------------|------------------------------------------------------|
| `def gen(): yield x`                 | `func() iter.Seq[T] { return func(yield func(T) bool) {...} }` |
| `for x in gen():`                    | `for x := range gen() {}`                            |
| `list(gen)`                          | `slices.Collect(seq)`                                |
| `enumerate(xs)`                      | `slices.All(xs)` o un `Seq2` propio                  |
| `itertools.islice(gen, n)`           | un contador y `break`, o un adaptador `Tomar(seq, n)` |
| el generador se pausa en `yield`     | el iterador llama a `yield`, que ejecuta el cuerpo del bucle |

## Resumen

- `for i := range n` recorre de 0 a n-1 (1.22).
- Un iterador es `func(yield func(V) bool)`; `iter.Seq[V]` e `iter.Seq2[K, V]` son sus tipos.
- **Siempre cortá cuando `yield` devuelve `false`.**
- Son perezosos y pueden ser infinitos; se componen con adaptadores.
- `slices.Collect`, `slices.Sorted`, `maps.Keys` y compañía conectan iteradores con slices.

## Ejercicio

Un rango como iterador, Fibonacci infinito, un adaptador para tomar los primeros N y un
`Seq2` que enumera.

**Para profundizar:** [Range Over Function Types](https://go.dev/blog/range-functions),
[paquete iter](https://pkg.go.dev/iter).
