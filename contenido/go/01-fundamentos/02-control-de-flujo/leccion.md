# Control de flujo: if, for y switch

Go tiene muy pocas estructuras de control, y a propósito: `if`, `for` (el **único** bucle) y
`switch`. Lo que cambia respecto de Python son los detalles: no hay paréntesis, las llaves
son obligatorias, `if` y `switch` aceptan una sentencia de inicialización y `switch` no
"se cae" al siguiente caso.

## `if`

```go
if edad >= 18 {
    fmt.Println("mayor")
} else if edad >= 13 {
    fmt.Println("adolescente")
} else {
    fmt.Println("chico")
}
```

- Sin paréntesis alrededor de la condición; **llaves siempre**, aunque sea una línea.
- La llave de apertura va en la **misma línea**. `gofmt` lo impone, y el compilador también,
  por la inserción automática de punto y coma.
- La condición tiene que ser `bool`: no hay *truthiness*. `if len(xs)` no compila; se escribe
  `if len(xs) > 0`.

### `if` con inicialización

```go
if n, err := strconv.Atoi(texto); err != nil {
    return 0, err
} else if n < 0 {
    return 0, errors.New("negativo")
}
// n y err no existen acá: su scope es el if
```

Es el patrón que vas a ver en todo código Go para manejar errores sin ensuciar el scope de
la función.

## `for`: el único bucle, con cuatro formas

```go
// 1. Clásico, estilo C
for i := 0; i < 10; i++ { ... }

// 2. Como un while
for saldo > 0 { ... }

// 3. Infinito
for {
    if listo() {
        break
    }
}

// 4. range: recorrer colecciones
for i, v := range []string{"a", "b"} { ... }   // índice y valor
for _, v := range lista { ... }                 // solo el valor
for i := range lista { ... }                    // solo el índice
for clave, valor := range mapa { ... }          // ¡orden aleatorio en maps!
for i, r := range "hola" { ... }                // índice en bytes y rune
for i := range 10 { ... }                       // 0..9 (Go 1.22+)
```

`range` sobre un slice entrega el índice **y una copia** del elemento. Modificar `v` no
modifica el slice; para eso, `lista[i] = ...`.

Desde Go 1.22, **cada iteración tiene su propia variable**. Antes, las closures creadas en un
bucle compartían la variable, igual que el *late binding* de Python. Hoy ese problema ya no
existe en Go.

### `break`, `continue` y etiquetas

Para salir de bucles anidados se usa una **etiqueta**:

```go
buscar:
    for i, fila := range matriz {
        for j, v := range fila {
            if v == objetivo {
                fmt.Println("encontrado en", i, j)
                break buscar          // sale de los DOS bucles
            }
        }
    }
```

## `switch`: más potente que en C

```go
switch dia {
case "sábado", "domingo":         // varios valores en un caso
    fmt.Println("finde")
case "lunes":
    fmt.Println("uf")
default:
    fmt.Println("día de semana")
}
```

- **No hay fall-through**: se ejecuta un solo caso y no hace falta `break`. Si realmente
  querés continuar con el siguiente, está la palabra `fallthrough` (rara vez usada).
- Los casos pueden ser expresiones, no solo constantes.

### `switch` sin condición: un `if/else if` más limpio

```go
switch {
case temp < 10:
    return "frío"
case temp < 25:
    return "templado"
default:
    return "calor"
}
```

Es la forma idiomática de escribir cadenas de condiciones.

### `switch` con inicialización

```go
switch n := len(xs); {
case n == 0:
    ...
case n > 100:
    ...
}
```

Existe también el **type switch** (`switch v := x.(type)`), que vemos en el módulo de
interfaces.

## `defer`: un adelanto

`defer` programa una llamada para que se ejecute **al salir de la función**, pase lo que
pase. Es el equivalente idiomático del `with` de Python:

```go
f, err := os.Open(ruta)
if err != nil {
    return err
}
defer f.Close()     // se cierra al final, aunque haya un return antes
```

Lo profundizamos en el módulo de errores.

## Comparación con Python

| Python                          | Go                                   |
|---------------------------------|--------------------------------------|
| `while cond:`                   | `for cond { }`                       |
| `for i in range(n):`            | `for i := range n { }`               |
| `for i, x in enumerate(xs):`    | `for i, x := range xs { }`           |
| `for k, v in d.items():`        | `for k, v := range m { }` (sin orden) |
| `if xs:`                        | `if len(xs) > 0 { }`                 |
| `match`                         | `switch` (sin desempaquetar estructuras) |
| `for ... else`                  | no existe: función con `return` o una etiqueta |

## Resumen

- Sin paréntesis, llaves obligatorias y condiciones estrictamente `bool`.
- `if` y `switch` aceptan una sentencia de inicialización con su propio scope.
- `for` es el único bucle: clásico, tipo while, infinito o con `range`.
- `switch` no tiene fall-through; `switch {}` sin condición reemplaza a los `else if`.
- Etiquetas para `break`/`continue` en bucles anidados.

## Ejercicio

FizzBuzz, clasificación con `switch` sin condición, un primo con salida temprana y una
búsqueda en una matriz con `break` etiquetado.

**Para profundizar:** [A Tour of Go — Flow control](https://go.dev/tour/flowcontrol/1),
[Effective Go — Control structures](https://go.dev/doc/effective_go#control-structures).
