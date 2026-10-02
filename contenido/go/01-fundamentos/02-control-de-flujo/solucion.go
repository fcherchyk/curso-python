package ejercicio

import "strconv"

func FizzBuzz(n int) []string {
	res := make([]string, 0, n)
	for i := 1; i <= n; i++ {
		switch {
		case i%15 == 0:
			res = append(res, "FizzBuzz")
		case i%3 == 0:
			res = append(res, "Fizz")
		case i%5 == 0:
			res = append(res, "Buzz")
		default:
			res = append(res, strconv.Itoa(i))
		}
	}
	return res
}

func Clasificar(t float64) string {
	switch {
	case t < 10:
		return "frío"
	case t < 25:
		return "templado"
	default:
		return "calor"
	}
}

func EsPrimo(n int) bool {
	if n < 2 {
		return false
	}
	for d := 2; d*d <= n; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func Buscar(matriz [][]int, objetivo int) (fila, col int, ok bool) {
buscar:
	for i, f := range matriz {
		for j, v := range f {
			if v == objetivo {
				fila, col, ok = i, j, true
				break buscar
			}
		}
	}
	return fila, col, ok
}
