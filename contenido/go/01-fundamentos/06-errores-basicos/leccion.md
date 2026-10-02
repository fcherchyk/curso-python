# Errores: valores, no excepciones

Go **no tiene excepciones**. Un error es un **valor** que la función devuelve, normalmente
como último resultado, y quien llama decide qué hacer con él en la línea siguiente. Es la
característica más discutida del lenguaje y la que más define su estilo: el flujo de error
queda siempre **a la vista**.

## El tipo `error`

`error` es una interfaz de la stdlib con un solo método:

```go
type error interface {
    Error() string
}
```

Cualquier tipo con un método `Error() string` es un error. Un error `nil` significa "no hubo
error".

## El patrón

```go
func Dividir(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("división por cero")
    }
    return a / b, nil
}

resultado, err := Dividir(10, 0)
if err != nil {
    fmt.Println("falló:", err)
    return
}
fmt.Println(resultado)
```

Convenciones:

- El `error` va **último** en los resultados.
- Si hay error, los demás valores suelen ser zero values y **no hay que usarlos**.
- Chequeá **inmediatamente**: `if err != nil { ... }`.
- El camino feliz queda sin indentar y los errores se manejan y retornan temprano, igual que
  las cláusulas de guarda.

## Crear errores

```go
errors.New("mensaje fijo")
fmt.Errorf("usuario %d no encontrado", id)         // con formato
```

Estilo de los mensajes: **en minúscula y sin punto final**, porque suelen terminar
concatenados en otros mensajes: `"cargando config: abriendo archivo: no such file"`.

## Agregar contexto: `%w`

Cuando un error sube por varias capas, cada una le agrega contexto **envolviéndolo**:

```go
func CargarConfig(ruta string) (Config, error) {
    datos, err := os.ReadFile(ruta)
    if err != nil {
        return Config{}, fmt.Errorf("cargando config %s: %w", ruta, err)
    }
    ...
}
```

`%w` (*wrap*) crea un error nuevo con el mensaje y **conserva el original** adentro, para que
se pueda inspeccionar con `errors.Is` y `errors.As`. Es el equivalente de `raise ... from e`.
Lo vemos a fondo en el módulo de errores.

## Errores centinela: `errors.Is`

Para errores "conocidos" que quien llama quiere distinguir, se declaran variables a nivel de
paquete:

```go
var ErrNoEncontrado = errors.New("no encontrado")

func Buscar(id int) (Usuario, error) {
    ...
    return Usuario{}, ErrNoEncontrado
}

u, err := Buscar(7)
if errors.Is(err, ErrNoEncontrado) {     // funciona aunque esté envuelto con %w
    ...
}
```

Usá `errors.Is(err, X)` y no `err == X`: la comparación directa falla si el error vino
envuelto. La stdlib está llena de centinelas: `io.EOF`, `os.ErrNotExist`, `sql.ErrNoRows`.

## ¿Y `panic`?

`panic` existe, pero **no es el mecanismo de errores**. Se usa para situaciones que no
deberían ocurrir nunca (bugs, invariantes rotas o una inicialización imposible). Un índice
fuera de rango o un puntero `nil` también producen un panic. La regla: **las funciones de
una librería devuelven `error`, no hacen panic**.

## Comparación con Python

```python
try:
    n = int(texto)
except ValueError as e:
    raise ConfigError(f"edad inválida: {texto}") from e
```

```go
n, err := strconv.Atoi(texto)
if err != nil {
    return 0, fmt.Errorf("edad inválida %q: %w", texto, err)
}
```

| Python                                  | Go                                        |
|-----------------------------------------|-------------------------------------------|
| excepciones que "vuelan" por la pila     | valores `error` que se devuelven explícitamente |
| `try/except`                             | `if err != nil`                           |
| `raise X from e`                         | `fmt.Errorf("...: %w", err)`              |
| `except FileNotFoundError`               | `errors.Is(err, fs.ErrNotExist)`          |
| clase de excepción propia                | variable centinela o tipo con `Error()`   |

## Errores comunes

```go
v, _ := strconv.Atoi(s)     // ✗ ignorar el error: si falla, v vale 0 en silencio

if err != nil {
    log.Println(err)        // ✗ loguear Y devolver: el error termina logueado varias veces
    return err
}
```

Regla: cada error se **maneja una sola vez**. O lo resolvés (default, reintento), o lo
devolvés con contexto, o lo logueás en el borde del programa (en `main`, o en el handler
HTTP).

## Resumen

- Un error es un valor (`error`), devuelto último; `nil` significa que salió bien.
- `if err != nil` inmediatamente después de la llamada; camino feliz sin indentar.
- `errors.New` y `fmt.Errorf`, con mensajes en minúscula y sin punto final.
- `%w` para envolver con contexto; `errors.Is` para comparar con centinelas.
- `panic` es para bugs, no para errores esperados.

## Ejercicio

Funciones que devuelven errores, un error centinela, errores con contexto envuelto y
procesamiento que corta en el primer error.

**Para profundizar:** [Error handling and Go](https://go.dev/blog/error-handling-and-go),
[Working with Errors in Go 1.13](https://go.dev/blog/go1.13-errors).
