package ejercicio

import (
	"math"
	"strconv"
	"strings"
	"unicode"
	"unicode/utf8"
)

func SumarNumeros(texto string) (int, error) {
	total := 0
	for _, parte := range strings.Split(texto, ",") {
		n, err := strconv.Atoi(strings.TrimSpace(parte))
		if err != nil {
			return 0, err
		}
		total += n
	}
	return total, nil
}

func Iniciales(nombre string) string {
	var b strings.Builder
	for _, palabra := range strings.Fields(nombre) {
		primera := []rune(palabra)[0]
		b.WriteRune(unicode.ToUpper(primera))
	}
	return b.String()
}

func Hipotenusa(a, b float64) float64 {
	return math.Round(math.Hypot(a, b)*100) / 100
}

func EsIdentificadorExportado(nombre string) bool {
	r, _ := utf8.DecodeRuneInString(nombre)
	return unicode.IsUpper(r)
}
