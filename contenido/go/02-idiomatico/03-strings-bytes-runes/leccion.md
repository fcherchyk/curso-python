# Strings, bytes y runes

En Python 3 un `str` es una secuencia de caracteres Unicode y casi nunca pensás en bytes. En
Go, un `string` es una **secuencia inmutable de bytes**, normalmente UTF-8. Esa diferencia
aparece apenas trabajás con texto en español: `len("año")` no es 3.

## `string` = bytes UTF-8

```go
s := "año"
len(s)                        // 4: bytes, no caracteres ("ñ" ocupa 2 bytes)
utf8.RuneCountInString(s)     // 3: caracteres (runes)
s[1]                          // 195: un BYTE (el primero de "ñ"), de tipo uint8
s[0:1]                        // "a": rebanar también cuenta bytes
```

- Indexar un string devuelve un **byte**, no un carácter.
- Rebanar puede **cortar un carácter por la mitad** si no tenés cuidado.
- Los strings son **inmutables**: `s[0] = 'A'` no compila.

## `rune`: un carácter Unicode

`rune` es un alias de `int32` y representa un *code point* Unicode. Los literales entre comillas
simples son runes:

```go
r := 'ñ'              // rune: 241
fmt.Printf("%c %d %U\n", r, r, r)   // ñ 241 U+00F1
```

### Recorrer con `range`: por runes

```go
for i, r := range "año" {
    fmt.Println(i, string(r))
}
// 0 a
// 1 ñ
// 3 o      ← el índice salta: es la posición en BYTES
```

`range` sobre un string **decodifica UTF-8** y entrega runes. Es la forma correcta de recorrer
texto carácter por carácter. Un `for i := 0; i < len(s); i++` recorre bytes.

### Convertir

```go
runas := []rune("año")        // [97 241 111]: ahora sí, un elemento por carácter
len(runas)                    // 3
string(runas[1])              // "ñ"
bytes := []byte("año")        // [97 195 177 111]
string(bytes)                 // "año"
```

Convertir a `[]rune` o `[]byte` **copia** los datos. Para invertir un string o acceder al
enésimo carácter, pasar por `[]rune` es lo más directo.

> Hay caracteres "visibles" formados por varios runes, como algunos emojis o letras con
> acentos combinados. Para esos casos existen librerías de *grapheme clusters*. Para el
> español habitual, runes alcanzan.

## El paquete `strings`

Casi todo lo que hacías con métodos de `str` en Python está como **funciones** en `strings`:

```go
strings.ToUpper(s), strings.ToLower(s)
strings.TrimSpace(s)                    // strip()
strings.Trim(s, "-"), strings.TrimPrefix(s, "http://"), strings.TrimSuffix(s, ".go")
strings.Split("a,b,c", ",")             // ["a" "b" "c"]
strings.Fields("  a  b ")               // ["a" "b"]: split() sin argumentos
strings.Join([]string{"a", "b"}, "-")   // "a-b"
strings.Contains(s, "sub"), strings.HasPrefix(s, "x"), strings.HasSuffix(s, "y")
strings.Index(s, "sub")                 // -1 si no está
strings.Replace(s, "a", "b", -1), strings.ReplaceAll(s, "a", "b")
strings.Repeat("-", 10)
strings.Cut("clave=valor", "=")         // ("clave", "valor", true): el partition de Go
strings.EqualFold("Go", "GO")           // comparar sin mayúsculas
```

Y `unicode` para clasificar runes: `unicode.IsLetter`, `IsDigit`, `IsSpace`, `IsUpper`,
`ToUpper`.

`TrimLeft`/`TrimRight` sacan **caracteres** de un conjunto, igual que `strip` en Python.
Para un prefijo exacto, `TrimPrefix`.

## `byte` y el paquete `bytes`

Cuando trabajás con datos binarios o con E/S, se usa `[]byte`. El paquete `bytes` tiene las
mismas funciones que `strings` pero para `[]byte`: `bytes.Contains`, `bytes.Split`, etc.
Muchas APIs (`os.ReadFile`, `json.Marshal`) devuelven `[]byte`.

## Comparar y ordenar

Los strings se comparan con `==`, `<` y `>` **byte a byte** (orden lexicográfico por código).
Para ignorar mayúsculas, `strings.EqualFold`. Para ordenar "como en el diccionario" en
español hace falta `golang.org/x/text/collate`.

## Comparación con Python

| Python                     | Go                                             |
|----------------------------|------------------------------------------------|
| `len("año")` → 3           | `len("año")` → 4 (bytes); `utf8.RuneCountInString` → 3 |
| `s[1]` → `"ñ"`             | `s[1]` → un byte; `[]rune(s)[1]` → `'ñ'`       |
| `for c in s`               | `for _, r := range s` (runes)                  |
| `s.upper()`                | `strings.ToUpper(s)`                           |
| `s.split()`                | `strings.Fields(s)`                            |
| `s.partition("=")`         | `strings.Cut(s, "=")`                          |
| `s[::-1]`                  | invertir un `[]rune` y convertirlo             |
| `str` / `bytes`            | `string` / `[]byte`                            |

## Resumen

- Un `string` es un conjunto de bytes UTF-8 inmutables: `len` cuenta bytes.
- `rune` = carácter Unicode; `range` sobre un string recorre runes.
- `[]rune(s)` para indexar o invertir por caracteres; `utf8.RuneCountInString` para contarlos.
- Funciones de `strings` y `unicode` en lugar de métodos.
- `strings.Cut` es el `partition` de Go.

## Ejercicio

Contar caracteres, invertir respetando Unicode, un palíndromo que ignora mayúsculas y
puntuación, y capitalizar palabras.

**Para profundizar:** [Strings, bytes, runes and characters in Go](https://go.dev/blog/strings),
[paquete strings](https://pkg.go.dev/strings).
