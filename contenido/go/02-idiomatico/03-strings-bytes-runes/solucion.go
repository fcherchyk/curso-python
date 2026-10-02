package ejercicio

import (
	"strings"
	"unicode"
	"unicode/utf8"
)

func ContarCaracteres(s string) int {
	return utf8.RuneCountInString(s)
}

func Invertir(s string) string {
	runas := []rune(s)
	for i, j := 0, len(runas)-1; i < j; i, j = i+1, j-1 {
		runas[i], runas[j] = runas[j], runas[i]
	}
	return string(runas)
}

func EsPalindromo(s string) bool {
	var limpias []rune
	for _, r := range s {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			limpias = append(limpias, unicode.ToLower(r))
		}
	}
	for i, j := 0, len(limpias)-1; i < j; i, j = i+1, j-1 {
		if limpias[i] != limpias[j] {
			return false
		}
	}
	return true
}

func Capitalizar(s string) string {
	palabras := strings.Fields(s)
	for i, p := range palabras {
		runas := []rune(strings.ToLower(p))
		runas[0] = unicode.ToUpper(runas[0])
		palabras[i] = string(runas)
	}
	return strings.Join(palabras, " ")
}
