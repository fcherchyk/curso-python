package ejercicio

import "iter"

func Rango(desde, hasta, paso int) iter.Seq[int] {
	return func(yield func(int) bool) {
		if paso <= 0 {
			return
		}
		for i := desde; i < hasta; i += paso {
			if !yield(i) {
				return
			}
		}
	}
}

func Fibonacci() iter.Seq[int] {
	return func(yield func(int) bool) {
		a, b := 0, 1
		for yield(a) {
			a, b = b, a+b
		}
	}
}

func Tomar(seq iter.Seq[int], n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		if n <= 0 {
			return
		}
		tomados := 0
		for v := range seq {
			if !yield(v) {
				return
			}
			tomados++
			if tomados == n {
				return // al retornar, el range sobre seq hace que su yield devuelva false
			}
		}
	}
}

func Enumerar(xs []string, inicio int) iter.Seq2[int, string] {
	return func(yield func(int, string) bool) {
		for i, x := range xs {
			if !yield(inicio+i, x) {
				return
			}
		}
	}
}
