package ejercicio

import (
	"slices"
	"strings"
)

func ContarPalabras(texto string) map[string]int {
	conteo := make(map[string]int)
	for _, p := range strings.Fields(texto) {
		conteo[strings.ToLower(p)]++
	}
	return conteo
}

func AgruparPorLargo(palabras []string) map[int][]string {
	grupos := make(map[int][]string)
	for _, p := range palabras {
		grupos[len(p)] = append(grupos[len(p)], p)
	}
	return grupos
}

func Invertir(notas map[string]int) map[int][]string {
	inverso := make(map[int][]string)
	for nombre, nota := range notas {
		inverso[nota] = append(inverso[nota], nombre)
	}
	for _, nombres := range inverso {
		slices.Sort(nombres) // ordena en el lugar: el slice del map se ve modificado
	}
	return inverso
}

func Comunes(a, b []string) []string {
	enA := make(map[string]struct{}, len(a))
	for _, x := range a {
		enA[x] = struct{}{}
	}
	vistos := make(map[string]struct{})
	var res []string
	for _, x := range b {
		if _, ok := enA[x]; !ok {
			continue
		}
		if _, repetido := vistos[x]; !repetido {
			vistos[x] = struct{}{}
			res = append(res, x)
		}
	}
	slices.Sort(res)
	return res
}
