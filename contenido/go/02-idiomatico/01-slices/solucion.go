package ejercicio

import "slices"

func Filtrar(xs []int, f func(int) bool) []int {
	var res []int
	for _, x := range xs {
		if f(x) {
			res = append(res, x)
		}
	}
	return res
}

func Invertir(xs []int) {
	for i, j := 0, len(xs)-1; i < j; i, j = i+1, j-1 {
		xs[i], xs[j] = xs[j], xs[i]
	}
}

func EnLotes(xs []int, n int) [][]int {
	if n <= 0 {
		return nil
	}
	var lotes [][]int
	for inicio := 0; inicio < len(xs); inicio += n {
		fin := min(inicio+n, len(xs))
		lotes = append(lotes, xs[inicio:fin])
	}
	return lotes
}

func AgregarCopia(base []int, x int) []int {
	// Clone crea un array nuevo: el append ya no puede escribir en el de base.
	return append(slices.Clone(base), x)
}
