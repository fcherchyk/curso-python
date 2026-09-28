# Strings idiomáticos

Los `str` de Python son **inmutables**, están en Unicode y traen muchos métodos. La mayoría
de los errores con strings vienen de construirlos mal (concatenando en bucles), de
parsearlos a mano con índices o de no conocer el método que ya resuelve el problema.

## f-strings: el formato por defecto

Desde 3.6, las f-strings son la forma recomendada de interpolar. Son más legibles y más
rápidas que `%` y que `.format()`:

```python
nombre, edad = "Ana", 31
f"{nombre} tiene {edad} años"
f"{nombre!r}"            # repr: "'Ana'"  (útil en logs y mensajes de error)
f"{edad + 1}"            # cualquier expresión
f"{x=}"                  # debug (3.8+): "x=42"
f"{x = }"                # con espacios: "x = 42"
```

### El mini-lenguaje de formato

Después de los `:` va una especificación de formato:

```python
precio = 1234.5
f"{precio:.2f}"          # '1234.50'     2 decimales
f"{precio:,.2f}"         # '1,234.50'    separador de miles
f"{precio:_.0f}"         # '1_234'
f"{0.256:.1%}"           # '25.6%'
f"{42:>6}"               # '    42'      alineado a la derecha en 6
f"{'hola':<8}|"          # 'hola    |'   izquierda
f"{'hola':^10}"          # '   hola   '  centrado
f"{7:03d}"               # '007'         relleno con ceros
f"{255:x} {255:b}"       # 'ff 11111111' hexa y binario
f"{fecha:%Y-%m-%d}"      # los objetos definen su propio formato (datetime)
```

La especificación también puede venir de una variable: `f"{valor:>{ancho}}"`.

> El separador de miles de `,` usa el formato inglés (`1,234.50`). Para el formato
> argentino (`1.234,50`) hay dos caminos: `locale` (que depende de la configuración del
> sistema) o intercambiar los caracteres después de formatear. Lo practicás en el ejercicio.

## Unir y partir

```python
", ".join(["a", "b", "c"])         # 'a, b, c'  <- join es un método del SEPARADOR
" ".join(str(n) for n in nums)     # join solo acepta strings: convertí antes

"a,b,,c".split(",")                # ['a', 'b', '', 'c']
"  hola   mundo ".split()          # ['hola', 'mundo']  <- sin argumento: cualquier espacio, sin vacíos
"k=v=w".split("=", 1)              # ['k', 'v=w']       <- como máximo 1 corte
"ruta/a/archivo.txt".rsplit("/", 1)  # ['ruta/a', 'archivo.txt']
```

### Nunca concatenes en un bucle

```python
# ✗ Cuadrático: cada += puede copiar todo el string
s = ""
for palabra in palabras:
    s += palabra + " "

# ✓ Lineal
s = " ".join(palabras)
```

### `partition`: partir en tres sin sorpresas

```python
"clave=valor".partition("=")       # ('clave', '=', 'valor')
"sin-igual".partition("=")         # ('sin-igual', '', '')  <- no falla
usuario, _, dominio = email.partition("@")
```

Con `split("=")` tenés que controlar cuántos pedazos quedaron. `partition` siempre devuelve
una tupla de tres elementos, así que el desempaquetado nunca falla.

## Limpiar y consultar

```python
"  hola \n".strip()                # 'hola'   (también lstrip / rstrip)
"xxhola".lstrip("x")               # 'hola'   ¡OJO! saca CARACTERES, no un prefijo
"https://sitio".removeprefix("https://")   # 'sitio'  (3.9+) saca el prefijo exacto
"foto.jpg".removesuffix(".jpg")    # 'foto'

"archivo.py".endswith((".py", ".pyi"))     # acepta una tupla de opciones
"ab" in "cabeza"                   # búsqueda de substring
"hola".find("z")                   # -1 (index() levantaría ValueError)
"Straße".casefold() == "strasse"   # True: comparación sin mayúsculas más robusta que lower()
"42".isdigit(), "abc".isalpha(), "   ".isspace()
```

La trampa de `strip("https://")` es clásica: saca cualquier combinación de los caracteres
`h t p s : /` de los extremos, no el prefijo. Para prefijos y sufijos usá
`removeprefix` y `removesuffix`.

## Reemplazar y traducir

```python
"a-b-c".replace("-", "_")          # 'a_b_c'
"a-b-c".replace("-", "_", 1)       # 'a_b-c'   solo el primero

# translate: varios reemplazos de un carácter en una sola pasada
tabla = str.maketrans({",": ".", ".": ","})
"1,234.50".translate(tabla)        # '1.234,50'
```

`translate` es la forma correcta de **intercambiar** caracteres. Con dos `replace` seguidos,
el segundo pisaría lo que hizo el primero.

## Strings multilínea y crudos

```python
sql = """
    SELECT *
    FROM usuarios
"""
import textwrap
textwrap.dedent(sql).strip()       # saca la indentación común

r"C:\nueva\carpeta"                # raw string: la \ no escapa (útil en regex y en rutas de Windows)
```

## `str` vs. `bytes`

`str` es texto Unicode; `bytes` son octetos. Se convierte en los bordes del programa:

```python
"ñandú".encode("utf-8")            # b'\xc3\xb1and\xc3\xba'
b"\xc3\xb1".decode("utf-8")        # 'ñ'
```

Regla: **decodificá al leer y codificá al escribir**. Adentro del programa trabajá siempre
con `str`, y abrí los archivos de texto con `encoding="utf-8"` explícito.

## Resumen

| Querés…                                 | Usá                                  |
|-----------------------------------------|--------------------------------------|
| interpolar                              | f-string                             |
| formatear números                       | `f"{x:,.2f}"`, `f"{x:.1%}"`          |
| unir muchas partes                      | `sep.join(partes)`                   |
| partir en dos por un separador          | `a, _, b = s.partition(sep)`         |
| sacar un prefijo o sufijo exacto        | `removeprefix` / `removesuffix`      |
| varias terminaciones posibles           | `s.endswith((".a", ".b"))`           |
| intercambiar caracteres                 | `str.maketrans` + `translate`        |
| comparar sin mayúsculas                 | `a.casefold() == b.casefold()`       |

## Ejercicio

Cuatro funciones: formatear moneda en formato argentino, generar un *slug*, parsear pares
`clave=valor` y construir una URL.

**Para profundizar:** [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec),
[métodos de str](https://docs.python.org/3/library/stdtypes.html#string-methods).
