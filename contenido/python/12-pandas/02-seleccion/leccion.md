# Seleccionar y filtrar: loc, iloc, máscaras y copy-on-write

Elegir filas y columnas es lo que más vas a hacer con pandas, y también donde más confusión hay:
`[]`, `loc` e `iloc` se parecen pero no son lo mismo, y modificar un subconjunto de datos solía
dar el famoso `SettingWithCopyWarning`. En pandas 3 la regla quedó simple gracias a
**copy-on-write**. En este capítulo armamos un modelo mental claro.

## `loc`: por etiquetas

```python
df.loc[5]                         # la fila con índice 5 → Series
df.loc[5, "producto"]             # un valor
df.loc[[1, 5, 9], ["producto", "total"]]     # filas y columnas por etiqueta
df.loc[10:20]                     # ¡INCLUYE el 20! (los slices por etiqueta son inclusivos)
df.loc[:, "fecha":"producto"]     # rango de columnas, también inclusivo
```

## `iloc`: por posiciones

```python
df.iloc[0]                        # la primera fila, sea cual sea su etiqueta
df.iloc[0, 2]                     # fila 0, columna 2
df.iloc[:5]                       # las primeras 5 (excluye la 5, como en Python)
df.iloc[-3:, [0, 1]]              # las últimas 3 filas, columnas 0 y 1
```

**Regla:** `loc` = etiquetas (inclusivo), `iloc` = posiciones (exclusivo, como Python). Si el
índice es 0, 1, 2… parecen iguales, pero después de filtrar u ordenar dejan de coincidir:

```python
ordenado = df.sort_values("total", ascending=False)
ordenado.loc[0]     # la fila con ETIQUETA 0, esté donde esté
ordenado.iloc[0]    # la PRIMERA fila: la de mayor total
```

## Filtrar con máscaras booleanas

Igual que en NumPy, pero las columnas tienen nombre:

```python
df[df["total"] > 10_000]
df[(df["sucursal"] == "Centro") & (df["cantidad"] >= 5)]       # & | ~ con paréntesis
df[df["producto"].isin(["yerba", "mate"])]
df[df["fecha"].between("2025-02-01", "2025-02-28")]
df.loc[df["total"] > 10_000, ["producto", "total"]]   # filtrar Y elegir columnas
```

### `query`: el mismo filtro como texto

```python
df.query("total > 10_000 and sucursal == 'Centro'")
minimo = 5
df.query("cantidad >= @minimo")          # @ para usar variables de Python
```

`query` se lee bien en filtros largos. Funciona sobre las columnas por nombre (los nombres con
espacios van entre backticks).

## Copy-on-write: la regla de pandas 3

**Todo resultado de una selección se comporta como una copia.** Modificarlo nunca cambia el
DataFrame original:

```python
centro = df[df["sucursal"] == "Centro"]
centro["total"] = 0               # modifica `centro`, NO `df` (y sin warnings)
```

Para modificar el **original**, hay que hacerlo en **un solo paso**, con `loc` sobre el propio
DataFrame:

```python
df.loc[df["sucursal"] == "Centro", "total"] = 0       # ✓ modifica df
df["total"][df["sucursal"] == "Centro"] = 0           # ✗ asignación encadenada: NO hace nada
                                                       #   (pandas 3 levanta ChainedAssignmentError)
```

Internamente, pandas comparte los datos y solo copia cuando alguien escribe, por eso se llama
*copy-on-write*. Eso lo hace eficiente.

> En pandas 1.x y 2.x el comportamiento dependía de si el resultado era una "vista" o una
> "copia", y de ahí venía el `SettingWithCopyWarning`. En código y tutoriales viejos vas a ver
> `.copy()` por todos lados "por las dudas": en pandas 3 ya no hace falta.

## Funciones que no mutan

Un buen hábito en análisis de datos es escribir funciones que **reciben un DataFrame y devuelven
otro**, sin modificar la entrada. Así las celdas de un notebook se pueden re-ejecutar y los
pasos se encadenan:

```python
def con_descuento(df: pd.DataFrame, categoria: str, pct: float) -> pd.DataFrame:
    resultado = df.copy()         # explícito: vamos a escribir
    mascara = resultado["categoria"] == categoria
    resultado.loc[mascara, "precio_unitario"] *= 1 - pct
    return resultado
```

O con `assign`, que siempre devuelve un DataFrame nuevo:

```python
df.assign(total=lambda d: d["cantidad"] * d["precio_unitario"])
```

## Elegir columnas

```python
df[["a", "b"]]
df.drop(columns=["c"])
df.filter(like="precio")              # columnas cuyo nombre contiene "precio"
df.select_dtypes("number")            # solo columnas numéricas
df.rename(columns={"cant": "cantidad"})
```

## Resumen

- `loc` por etiquetas (inclusivo); `iloc` por posiciones (exclusivo).
- Máscaras con `&`, `|` y `~` entre paréntesis; `isin` y `between`; `query` para filtros legibles.
- Copy-on-write: una selección nunca modifica el original; para escribir, `df.loc[mascara, col] = v`
  en un paso; nunca asignación encadenada.
- Las funciones de análisis reciben y devuelven DataFrames sin mutar la entrada (`copy()` o `assign`).

## Ejercicio

Filtros por condiciones combinadas, `query` con variables, la diferencia entre `loc` e `iloc`
después de ordenar y una función que aplica un descuento sin modificar el DataFrame original.

**Para profundizar:** [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html),
[Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html).
