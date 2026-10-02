package ejercicio

func CelsiusAFahrenheit(c float64) float64 {
	return c*9/5 + 32
}

func Promedio(nums []int) float64 {
	if len(nums) == 0 {
		return 0
	}
	suma := 0
	for _, n := range nums {
		suma += n
	}
	return float64(suma) / float64(len(nums))
}

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

var nombres = [...]string{"lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"}

func NombreDia(d Dia) string {
	if d < Lunes || d > Domingo {
		return "desconocido"
	}
	return nombres[d]
}

func EsFinDeSemana(d Dia) bool {
	return d == Sabado || d == Domingo
}
