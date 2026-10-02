# Punteros y paso por valor

En Python nunca pensás en punteros: todo nombre es una referencia a un objeto. En Go, en
cambio, **todo se pasa por valor** (se copia), y cuando querés compartir o modificar algo
usás explícitamente un **puntero**. Por suerte, los punteros de Go son mucho más simples que
los de C: no hay aritmética de punteros y la memoria la maneja el garbage collector.

## `&` y `*`

```go
x := 10
p := &x          // p es un *int: la dirección de x
fmt.Println(*p)  // 10: "desreferenciar", leer lo apuntado
*p = 20          // escribir a través del puntero
fmt.Println(x)   // 20
```

- `&v` toma la dirección de `v`.
- `*T` es el tipo "puntero a T".
- `*p` accede al valor apuntado.
- El zero value de un puntero es `nil`. Desreferenciar `nil` produce un **panic**.

## Todo se pasa por valor

```go
func incrementar(n int) {
    n++                    // modifica la copia
}

func incrementarPtr(n *int) {
    *n++                   // modifica el original
}

x := 1
incrementar(x)             // x sigue en 1
incrementarPtr(&x)         // x vale 2
```

Con structs es igual: pasar un struct **copia todos sus campos**.

```go
type Cuenta struct{ Saldo int }

func depositar(c Cuenta, monto int)   { c.Saldo += monto }   // ✗ modifica la copia
func depositarP(c *Cuenta, monto int) { c.Saldo += monto }   // ✓ (Go desreferencia solo)

c := Cuenta{}
depositarP(&c, 100)
```

Con un puntero a struct, `c.Saldo` funciona directamente: Go hace `(*c).Saldo` por vos.

## Crear valores apuntados

```go
c := &Cuenta{Saldo: 50}    // lo más común: literal con &
p := new(int)              // puntero a un int en cero (menos usado)
```

Y a diferencia de C, es seguro **devolver un puntero a una variable local**: el compilador
detecta que "escapa" y la ubica en el heap.

```go
func NuevaCuenta() *Cuenta {
    c := Cuenta{Saldo: 0}
    return &c              // ✓ perfectamente válido en Go
}
```

## Slices y maps: "referencias" que se copian

Un slice es un pequeño struct (puntero al array, largo y capacidad), y un map es un puntero a
una tabla interna. Al pasarlos por valor se copia **esa cabecera**, pero los datos son los
mismos:

```go
func ponerCero(xs []int) {
    xs[0] = 0              // ✓ se ve afuera: comparten el array
}

func agregar(xs []int) {
    xs = append(xs, 99)    // ✗ el append puede crear un array nuevo; afuera no se ve
}
```

Por eso las funciones que agregan elementos **devuelven** el slice nuevo, como `append`:
`xs = agregar(xs)`. Lo vemos a fondo en el capítulo de slices.

## ¿Cuándo usar puntero?

Usá **puntero** cuando:

1. La función tiene que **modificar** el valor de quien llama.
2. El struct es **grande** y copiarlo es caro (decenas de campos).
3. Necesitás representar "**ausencia**" (`nil`), por ejemplo un campo opcional.
4. El tipo tiene estado que no debe copiarse, como un `sync.Mutex`.

Usá **valor** cuando:

- el dato es chico e inmutable en la práctica (un punto, un rango de fechas, dinero);
- querés garantizar que nadie te lo modifique.

Los **receptores de métodos** siguen las mismas reglas; lo vemos en el módulo de tipos.

## Comparación con Python

| Python                                      | Go                                     |
|---------------------------------------------|----------------------------------------|
| todo es una referencia                      | todo es un valor; las referencias son explícitas (`*T`) |
| `def f(lista): lista.append(1)` se ve afuera | `append` en un slice recibido **no** necesariamente se ve |
| `None`                                      | `nil` (solo para punteros, slices, maps…) |
| `AttributeError: 'NoneType'`                | `panic: nil pointer dereference`       |

## Resumen

- `&v` es la dirección, `*T` el tipo puntero y `*p` el valor apuntado; el zero value es `nil`.
- Todo se pasa por valor: para modificar, pasá un puntero.
- `p.Campo` funciona directamente con punteros a struct.
- Devolver `&local` es seguro: el compilador lo mueve al heap.
- Slices y maps copian su cabecera: se comparten los elementos, pero `append` puede no
  verse afuera.

## Ejercicio

Intercambiar con punteros, modificar un struct, devolver un puntero opcional y ver la
diferencia entre modificar elementos de un slice y agregarle elementos.

**Para profundizar:** [A Tour of Go — Pointers](https://go.dev/tour/moretypes/1),
[Go FAQ: pass by value](https://go.dev/doc/faq#pass_by_value).
