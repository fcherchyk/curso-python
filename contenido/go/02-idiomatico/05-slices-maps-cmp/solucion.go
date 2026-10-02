package ejercicio

import (
	"cmp"
	"maps"
	"slices"
)

type Persona struct {
	Nombre string
	Edad   int
}

func OrdenarPersonas(personas []Persona) {
	slices.SortFunc(personas, func(a, b Persona) int {
		return cmp.Or(
			cmp.Compare(b.Edad, a.Edad), // descendente: b antes que a
			cmp.Compare(a.Nombre, b.Nombre),
		)
	})
}

type Producto struct {
	Nombre string
	Precio float64
}

func MasCaro(productos []Producto) (Producto, bool) {
	if len(productos) == 0 {
		return Producto{}, false
	}
	return slices.MaxFunc(productos, func(a, b Producto) int {
		return cmp.Compare(a.Precio, b.Precio)
	}), true
}

func ClavesOrdenadas(m map[string]int) []string {
	return slices.Sorted(maps.Keys(m))
}

func TopN(xs []int, n int) []int {
	ordenados := slices.Clone(xs)
	slices.SortFunc(ordenados, func(a, b int) int { return cmp.Compare(b, a) })
	return ordenados[:min(n, len(ordenados))]
}
