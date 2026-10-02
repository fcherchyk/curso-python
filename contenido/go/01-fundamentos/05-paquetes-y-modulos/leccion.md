# Paquetes, módulos e imports

En Go, la unidad de organización es el **paquete** (una carpeta) y la unidad de distribución
es el **módulo** (un repositorio con un `go.mod`). El sistema es más simple que el de
Python: no hay `__init__.py` ni imports relativos, y la visibilidad la decide la mayúscula.
A cambio es estricto: un import sin usar o un ciclo de imports **no compilan**.

## Paquetes: una carpeta, un paquete

```
tienda/
├── go.mod                  ← module github.com/ana/tienda
├── main.go                 ← package main
├── pedidos/
│   ├── pedido.go           ← package pedidos
│   └── calculo.go          ← package pedidos (mismo paquete, otro archivo)
└── internal/
    └── db/
        └── db.go           ← package db (solo importable desde tienda/)
```

- Todos los archivos `.go` de una carpeta pertenecen al **mismo paquete** y comparten todo:
  un archivo usa funciones de otro sin importar nada.
- El nombre del paquete es corto, en minúscula y sin guiones bajos: `pedidos`, `http`, `json`.
- `package main` con `func main()` define un ejecutable.

## Visibilidad: la primera letra

```go
package pedidos

type Pedido struct {     // exportado: se ve desde otros paquetes
    ID    int            // campo exportado
    total float64        // campo privado del paquete
}

func Nuevo(id int) *Pedido { ... }   // exportada
func calcular() float64 { ... }      // privada
```

No hay niveles intermedios como `protected`. Para restringir un paquete a tu propio módulo,
la carpeta **`internal/`**: todo lo que esté debajo solo se puede importar desde el árbol que
la contiene.

## Módulos y `go.mod`

```bash
go mod init github.com/ana/tienda     # crea go.mod
go get github.com/go-chi/chi/v5       # agrega una dependencia
go mod tidy                           # agrega lo que falta y saca lo que no se usa
```

```
module github.com/ana/tienda

go 1.23

require github.com/go-chi/chi/v5 v5.2.1
```

- La ruta del módulo es el prefijo de todos sus imports: `github.com/ana/tienda/pedidos`.
- `go.sum` guarda los hashes de las dependencias (como `uv.lock`) y va a git.
- Las dependencias se descargan en un caché global (`$GOPATH/pkg/mod`). No hay virtualenvs:
  cada módulo declara sus versiones exactas.
- Versionado semántico estricto: una versión mayor ≥ 2 cambia la ruta (`.../v5`).

## Imports

```go
import (
    "fmt"                                  // stdlib
    "strings"

    "github.com/go-chi/chi/v5"             // terceros

    "github.com/ana/tienda/pedidos"        // tu propio módulo
)

func main() {
    p := pedidos.Nuevo(1)       // se usa con el nombre del paquete
    fmt.Println(strings.ToUpper("hola"))
}
```

- Siempre **rutas absolutas** (desde el módulo); no existen los imports relativos.
- Se accede con el **nombre del paquete** como prefijo: `strings.ToUpper`. No existe un
  `from x import *`.
- Import sin usar → **no compila**. Tu editor (con `gopls`/`goimports`) agrega y saca imports
  al guardar.
- Alias: `import str "strings"`. Import solo por efectos secundarios: `import _ "image/png"`.

**Los ciclos de imports están prohibidos**: si `a` importa `b`, `b` no puede importar `a`. Te
obliga a separar bien las capas. La solución suele ser una interfaz o un tercer paquete.

## `init()`

Cada archivo puede tener funciones `init()`, que corren automáticamente al importar el
paquete, antes de `main`. Usalas poco: son "magia" difícil de testear. Casi siempre es mejor
una inicialización explícita.

## La biblioteca estándar

Go trae una stdlib muy completa, y en proyectos Go es habitual usar pocas dependencias:

| Paquete        | Para qué                                  |
|----------------|-------------------------------------------|
| `fmt`          | formatear e imprimir                       |
| `strings`, `strconv`, `unicode` | texto y conversiones      |
| `math`         | funciones matemáticas                     |
| `slices`, `maps`, `cmp` | operaciones genéricas (1.21+)     |
| `errors`       | crear y examinar errores                  |
| `time`         | fechas y duraciones                       |
| `os`, `io`, `bufio`, `path/filepath` | archivos y E/S      |
| `encoding/json` | JSON                                     |
| `net/http`     | cliente y servidor HTTP de producción     |
| `log/slog`     | logging estructurado                      |
| `testing`      | tests, benchmarks y fuzzing               |

La documentación de cualquier paquete está en [pkg.go.dev](https://pkg.go.dev) o con
`go doc strings.ToUpper`.

## Comparación con Python

| Python                            | Go                                          |
|-----------------------------------|---------------------------------------------|
| módulo = archivo                  | paquete = carpeta (todos sus archivos)       |
| `pyproject.toml` + `uv.lock`      | `go.mod` + `go.sum`                          |
| `uv add httpx`                    | `go get github.com/...`                      |
| `from x import y`                 | `import "ruta/x"` y después `x.Y`            |
| `_privado` (convención)           | minúscula (el compilador lo hace cumplir)    |
| import circular (falla a veces)   | ciclo prohibido (no compila)                 |
| venv por proyecto                 | caché global de módulos con versiones fijadas |

## Resumen

- Paquete = carpeta; todos sus archivos comparten el scope.
- Mayúscula exporta; `internal/` limita a tu módulo.
- `go.mod`/`go.sum` definen el módulo y sus dependencias; `go mod tidy` las ordena.
- Imports con rutas absolutas y uso con prefijo (`strings.ToUpper`). Los imports sin usar y
  los ciclos no compilan.
- La stdlib cubre muchísimo: arrancá por ahí.

## Ejercicio

Resolver problemas usando paquetes de la stdlib (`strings`, `strconv`, `unicode`, `math`).
**El código inicial no importa nada: agregá vos los imports que necesites** (el compilador te
avisa si falta alguno o sobra otro).

**Para profundizar:** [How to Write Go Code](https://go.dev/doc/code),
[Go Modules Reference](https://go.dev/ref/mod), [pkg.go.dev/std](https://pkg.go.dev/std).
