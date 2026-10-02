// Iteradores: range sobre funciones (Go 1.23+).
//
// Hoy cada función devuelve un iterador VACÍO. Completalas respetando siempre el
// valor que devuelve yield (si es false, hay que cortar).
package ejercicio

import "iter"

// Rango produce desde, desde+paso, ... mientras sea menor que hasta.
// Con paso <= 0 no produce nada.
func Rango(desde, hasta, paso int) iter.Seq[int] {
	return func(yield func(int) bool) {
		// TODO
	}
}

// Fibonacci produce 0, 1, 1, 2, 3, 5, ... infinitamente.
func Fibonacci() iter.Seq[int] {
	return func(yield func(int) bool) {
		// TODO
	}
}

// Tomar produce como máximo los primeros n valores de seq (como itertools.islice).
func Tomar(seq iter.Seq[int], n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		// TODO
	}
}

// Enumerar produce pares (posición, valor) empezando la posición en `inicio`.
func Enumerar(xs []string, inicio int) iter.Seq2[int, string] {
	return func(yield func(int, string) bool) {
		// TODO
	}
}
