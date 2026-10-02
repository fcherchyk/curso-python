// Funciones: múltiples retornos, variádicas y closures.
package ejercicio

// MinMax devuelve el mínimo, el máximo y si había al menos un número.
// Con cero argumentos devuelve (0, 0, false).
func MinMax(nums ...int) (min, max int, ok bool) {
	// TODO
	return 0, 0, false
}

// Map aplica f a cada elemento y devuelve un slice NUEVO con los resultados.
func Map(xs []int, f func(int) int) []int {
	// TODO
	return nil
}

// NuevoContador devuelve una función que, en cada llamada, devuelve el siguiente
// entero empezando en `desde`. Cada contador es independiente.
func NuevoContador(desde int) func() int {
	// TODO
	return func() int { return 0 }
}

// Componer devuelve una función que calcula f(g(x)).
func Componer(f, g func(int) int) func(int) int {
	// TODO
	return func(x int) int { return 0 }
}
