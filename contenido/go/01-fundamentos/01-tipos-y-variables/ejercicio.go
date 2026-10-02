// Tipos, variables y zero values.
//
// Completá cada función (hoy devuelven el zero value de su tipo).
package ejercicio

// CelsiusAFahrenheit convierte grados Celsius a Fahrenheit: F = C * 9 / 5 + 32.
func CelsiusAFahrenheit(c float64) float64 {
	// TODO
	return 0
}

// Promedio devuelve el promedio de los enteros como float64 (0 si no hay números).
// Ojo: la división entre ints trunca; convertí antes de dividir.
func Promedio(nums []int) float64 {
	// TODO
	return 0
}

// Dia es un día de la semana, con Lunes = 0.
type Dia int

const (
	Lunes Dia = iota
	Martes
	Miercoles
	Jueves
	Viernes
	Sabado
	Domingo
)

// NombreDia devuelve el nombre del día en español ("lunes", ..., "domingo"),
// o "desconocido" si el valor no es válido.
func NombreDia(d Dia) string {
	// TODO
	return ""
}

// EsFinDeSemana indica si el día es sábado o domingo.
func EsFinDeSemana(d Dia) bool {
	// TODO
	return false
}
