# Funciones: múltiples retornos, variádicas y closures

Las funciones de Go son simples: sin argumentos por nombre, sin defaults y sin sobrecarga.
A cambio tienen dos rasgos que marcan el estilo del lenguaje: **devuelven varios valores**
(así se manejan los errores) y **son valores de primera clase** (closures, callbacks,
middlewares).

## Anatomía

```go
func sumar(a int, b int) int {
    return a + b
}

func sumar2(a, b int) int {      // parámetros consecutivos del mismo tipo
    return a + b
}
```

El tipo va **después** del nombre. Los argumentos se pasan **por valor**: la función recibe
una copia. Con slices, maps y punteros, la copia es de la referencia y comparte los datos
(capítulo de punteros).

## Múltiples valores de retorno

```go
func dividir(a, b int) (int, int) {
    return a / b, a % b
}

cociente, resto := dividir(17, 5)
_, resto2 := dividir(9, 2)        // _ descarta un valor
```

Es el mecanismo central de Go para los **errores**:

```go
func buscar(id int) (Usuario, error) { ... }

u, err := buscar(42)
if err != nil {
    return err
}
```

También el idioma **"comma ok"**, que devuelve un valor y un `bool` que indica si existía:

```go
v, ok := mapa["clave"]
```

### Retornos con nombre

```go
func minMax(xs []int) (min, max int) {
    min, max = xs[0], xs[0]
    for _, x := range xs {
        if x < min { min = x }
        if x > max { max = x }
    }
    return          // "naked return": devuelve min y max
}
```

Los retornos con nombre documentan qué devuelve la función y arrancan en su zero value.
Evitá el `return` "desnudo" en funciones largas: es difícil ver qué se devuelve.

## Funciones variádicas

```go
func sumarTodos(nums ...int) int {   // nums es un []int
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

sumarTodos(1, 2, 3)
xs := []int{4, 5}
sumarTodos(xs...)                    // expandir un slice (como *xs en Python)
```

Solo el **último** parámetro puede ser variádico. `fmt.Println(a ...any)` es el ejemplo más
conocido.

## Funciones como valores

```go
doble := func(x int) int { return x * 2 }    // función anónima
fmt.Println(doble(21))

func aplicar(xs []int, f func(int) int) []int {
    res := make([]int, len(xs))
    for i, x := range xs {
        res[i] = f(x)
    }
    return res
}

aplicar([]int{1, 2}, doble)
aplicar([]int{1, 2}, func(x int) int { return x * x })
```

El tipo de una función incluye sus parámetros y sus retornos: `func(int) int`. Se le puede
dar nombre: `type Transformacion func(int) int`.

## Closures

Una función anónima captura las variables del scope donde se define, igual que en Python,
pero **sin necesidad de `nonlocal`**: puede leerlas y modificarlas.

```go
func contador() func() int {
    n := 0
    return func() int {
        n++          // modifica la variable capturada
        return n
    }
}

c := contador()
c(), c(), c()        // 1, 2, 3
```

`n` sobrevive a `contador()` porque la closure la referencia: el compilador la ubica en el
heap. Así se implementan los middlewares HTTP y los generadores de handlers.

## `defer`

`defer f()` posterga la llamada hasta que la función actual **retorna**, en orden LIFO:

```go
func procesar() {
    defer fmt.Println("tercero")
    defer fmt.Println("segundo")
    fmt.Println("primero")
}
```

Los argumentos de una llamada diferida se **evalúan en el momento del `defer`**, no al
final. Se usa para liberar recursos (`defer f.Close()`, `defer mu.Unlock()`) justo al lado de
donde se adquieren.

## Lo que Go no tiene (y qué se usa en su lugar)

| Python                      | Go                                                  |
|-----------------------------|-----------------------------------------------------|
| argumentos con default      | varias funciones, un struct de opciones o *functional options* |
| argumentos por nombre       | un struct de configuración: `Conectar(Config{Host: "x"})` |
| `*args`                     | `...T` (un solo tipo)                               |
| `**kwargs`                  | un struct o un `map[string]any`                     |
| decoradores con `@`         | funciones que envuelven funciones (middlewares)    |
| excepciones                 | múltiples retornos con `error`                      |

## Resumen

- Los tipos van después del nombre y los argumentos se pasan por valor.
- Múltiples retornos: `(valor, error)` y `(valor, ok)` son los idiomas centrales.
- Variádicas con `...T`, y `xs...` para expandir.
- Las funciones son valores; las closures capturan y modifican variables sin `nonlocal`.
- `defer` ejecuta al salir, en orden LIFO, y evalúa los argumentos en el momento.

## Ejercicio

Un mínimo y máximo variádico con retornos múltiples, `Map` con una función como parámetro, un
contador con closure y la composición de funciones.

**Para profundizar:** [A Tour of Go — Functions](https://go.dev/tour/basics/4),
[Function values and closures](https://go.dev/tour/moretypes/24).
