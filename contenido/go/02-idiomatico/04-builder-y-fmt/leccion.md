# Formatear texto: fmt y strings.Builder

Go no tiene f-strings. Para formatear se usa la familia `fmt.Printf`/`Sprintf` con **verbos**
al estilo de C (`%d`, `%s`, `%v`…), y para construir strings largos de forma eficiente,
`strings.Builder`. Dominar los verbos de `fmt` también te ayuda a depurar: `%+v` y `%#v`
muestran cualquier valor con detalle.

## Las funciones de `fmt`

```go
fmt.Println("total:", 42)              // separa con espacios y agrega \n
fmt.Printf("total: %d\n", 42)          // formatea e imprime (el \n lo ponés vos)
s := fmt.Sprintf("total: %d", 42)      // formatea y DEVUELVE el string
fmt.Fprintf(w, "total: %d", 42)        // escribe en un io.Writer (archivo, HTTP, buffer)
err := fmt.Errorf("falló %s: %w", x, e)
```

## Los verbos que vas a usar

| Verbo    | Para qué                           | Ejemplo → salida                         |
|----------|------------------------------------|------------------------------------------|
| `%v`     | valor en formato por defecto       | `{Ana 31}`                               |
| `%+v`    | structs con nombres de campo       | `{Nombre:Ana Edad:31}`                   |
| `%#v`    | sintaxis Go (ideal para depurar)   | `main.Persona{Nombre:"Ana", Edad:31}`    |
| `%T`     | el tipo                            | `main.Persona`                           |
| `%d`     | entero                             | `42`                                     |
| `%s`     | string                             | `hola`                                   |
| `%q`     | string entre comillas y escapado   | `"hola\n"`                               |
| `%f`, `%.2f` | float, con decimales           | `3.14`                                   |
| `%e`, `%g` | notación científica / compacta   |                                          |
| `%x`     | hexadecimal                        | `ff`                                     |
| `%c`, `%U` | rune como carácter / como Unicode | `ñ`, `U+00F1`                           |
| `%t`     | bool                               | `true`                                   |
| `%p`     | puntero                            | `0xc000012345`                           |
| `%%`     | un `%` literal                     |                                          |

### Ancho, precisión y alineación

```go
fmt.Sprintf("%6d|", 42)        // "    42|"   derecha en 6
fmt.Sprintf("%-6d|", 42)       // "42    |"   izquierda (el -)
fmt.Sprintf("%06d", 42)        // "000042"    relleno con ceros
fmt.Sprintf("%8.2f|", 3.14159) // "    3.14|" ancho 8, 2 decimales
fmt.Sprintf("%-10s|", "go")    // "go        |"
fmt.Sprintf("%*d", 5, 42)      // ancho desde un argumento
```

**Ojo:** el ancho de `%s` cuenta **runes**, así que funciona bien con acentos. `fmt` **no**
tiene separador de miles: para `1.234,50` hay que armarlo a mano o usar
`golang.org/x/text/message`.

`go vet` (que corre con `go test`) **verifica** que los verbos coincidan con los tipos de los
argumentos: `Printf("%d", "texto")` no pasa el vet.

## `Stringer`: cómo se imprime tu tipo

Si un tipo tiene un método `String() string`, `fmt` lo usa para `%v` y `%s`:

```go
type Dinero int64    // en centavos

func (d Dinero) String() string {
    return fmt.Sprintf("$%d,%02d", d/100, d%100)
}

fmt.Println(Dinero(12345))    // $123,45
```

Es el equivalente de `__str__`. (Los métodos se ven en detalle en el módulo de tipos.)

## `strings.Builder`: concatenar sin copiar de más

Como los strings son inmutables, `s += "x"` en un bucle crea un string nuevo en cada vuelta:
es cuadrático, igual que en Python. `strings.Builder` acumula en un buffer que crece:

```go
var b strings.Builder          // el zero value ya sirve
for i, item := range items {
    if i > 0 {
        b.WriteString(", ")
    }
    b.WriteString(item)
}
fmt.Fprintf(&b, " (%d items)", len(items))   // Builder es un io.Writer
resultado := b.String()
```

Métodos: `WriteString`, `WriteByte`, `WriteRune`, `Write` y `Grow(n)` para reservar espacio.
Para unir un slice con un separador, `strings.Join` es más simple.

## `strconv` frente a `fmt`

Para convertir un número suelto a texto, `strconv` es más rápido y más explícito que
`Sprintf`:

```go
strconv.Itoa(42)                          // "42"
strconv.FormatFloat(3.14159, 'f', 2, 64)  // "3.14"
strconv.Quote("hola\n")                   // "\"hola\\n\""
```

## Comparación con Python

| Python                     | Go                                          |
|----------------------------|---------------------------------------------|
| `f"{x}"`                   | `fmt.Sprintf("%v", x)`                      |
| `f"{x:>10.2f}"`            | `fmt.Sprintf("%10.2f", x)`                  |
| `f"{x:<12}"`               | `fmt.Sprintf("%-12s", x)`                   |
| `f"{x!r}"`                 | `%q` (strings) o `%#v`                      |
| `f"{x:,}"`                 | no existe: armarlo a mano                    |
| `__str__`                  | método `String() string`                    |
| `"".join(partes)`          | `strings.Join` o `strings.Builder`          |
| `print(a, b)`              | `fmt.Println(a, b)`                         |

## Resumen

- `Sprintf` para armar strings, `Printf` para imprimir y `Fprintf` para escribir en un Writer.
- `%v`, `%+v`, `%#v` y `%T` para depurar; `%d`, `%s`, `%q`, `%.2f` y `%x` para formatear.
- Ancho y alineación: `%10s`, `%-10s`, `%08.2f`.
- `String() string` define cómo se imprime tu tipo.
- `strings.Builder` para concatenar en bucles; `strconv` para conversiones sueltas.

## Ejercicio

Una lista "a, b y c" con Builder, una tabla de precios de ancho fijo, dinero en formato
argentino y un tipo con `String()`.

**Para profundizar:** [paquete fmt](https://pkg.go.dev/fmt),
[strings.Builder](https://pkg.go.dev/strings#Builder).
