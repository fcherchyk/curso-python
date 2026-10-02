// Paquetes, módulos e imports.
//
// Usá la biblioteca estándar. Este archivo no importa nada todavía:
// agregá el bloque import con los paquetes que necesites.
package ejercicio

// SumarNumeros recibe números separados por comas ("1, 2,3") y devuelve la suma.
// Si algún elemento no es un entero, devuelve el error de la conversión.
// Pista: strings.Split, strings.TrimSpace, strconv.Atoi.
func SumarNumeros(texto string) (int, error) {
	// TODO
	return 0, nil
}

// Iniciales devuelve la primera letra de cada palabra, en mayúscula.
// "ana maría pérez" → "AMP". Pista: strings.Fields, unicode.ToUpper y []rune.
func Iniciales(nombre string) string {
	// TODO
	return ""
}

// Hipotenusa devuelve la hipotenusa de un triángulo rectángulo, redondeada a 2
// decimales. Pista: math.Hypot y math.Round(x*100) / 100.
func Hipotenusa(a, b float64) float64 {
	// TODO
	return 0
}

// EsIdentificadorExportado indica si un nombre de Go estaría exportado: tiene que
// empezar con una letra mayúscula. Pista: utf8.DecodeRuneInString y unicode.IsUpper.
func EsIdentificadorExportado(nombre string) bool {
	// TODO
	return false
}
