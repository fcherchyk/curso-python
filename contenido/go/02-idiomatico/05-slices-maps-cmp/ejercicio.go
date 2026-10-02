// Los paquetes slices, maps y cmp.
//
// Agregá los imports que necesites (slices, maps, cmp).
package ejercicio

type Persona struct {
	Nombre string
	Edad   int
}

// OrdenarPersonas ordena EN EL LUGAR por edad descendente y, a igual edad, por nombre
// ascendente. Pista: slices.SortFunc + cmp.Or + cmp.Compare.
func OrdenarPersonas(personas []Persona) {
	// TODO
}

type Producto struct {
	Nombre string
	Precio float64
}

// MasCaro devuelve el producto de mayor precio (ante empate, el primero) y true;
// con el slice vacío, el zero value y false (¡MaxFunc hace panic con vacíos!).
func MasCaro(productos []Producto) (Producto, bool) {
	// TODO
	return Producto{}, false
}

// ClavesOrdenadas devuelve las claves del map ordenadas alfabéticamente.
func ClavesOrdenadas(m map[string]int) []string {
	// TODO
	return nil
}

// TopN devuelve los n números más grandes, de mayor a menor, sin modificar xs.
// Si hay menos de n, devuelve todos.
func TopN(xs []int, n int) []int {
	// TODO
	return nil
}
