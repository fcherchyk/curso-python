# Series y DataFrame

pandas es **la** herramienta de Python para datos tabulares: CSV, Excel, tablas de bases de
datos, logs y series de tiempo. Agrega a NumPy dos cosas fundamentales: **etiquetas** (filas y
columnas con nombre, no solo posiciones) y **tipos distintos por columna** (fechas, textos,
números, categorías en la misma tabla). Si alguna vez armaste una planilla de cálculo con
fórmulas, pandas es eso mismo, programable, reproducible y capaz de manejar millones de filas.

```bash
uv add pandas
```
```python
import pandas as pd       # alias universal
```

## Series: una columna con índice

```python
precios = pd.Series([3500, 9800, 1200], index=["yerba", "café", "té"], name="precio")
precios["café"]           # 9800: acceso por etiqueta
precios.iloc[0]           # 3500: acceso por posición
precios * 1.21            # vectorizado, como NumPy
precios[precios > 2000]   # máscaras, como NumPy
precios.index             # Index(['yerba', 'café', 'té'])
precios.values            # el array de NumPy subyacente (mejor: .to_numpy())
pd.Series({"a": 1, "b": 2})   # desde un dict: las claves son el índice
```

Una Series es un array de NumPy **con un índice**. Las operaciones entre Series se **alinean por
etiqueta**, no por posición:

```python
a = pd.Series({"x": 1, "y": 2})
b = pd.Series({"y": 10, "z": 20})
a + b        # x: NaN, y: 12.0, z: NaN  ← alineó por etiqueta; donde falta uno, NaN
```

## DataFrame: una tabla

Un DataFrame es una colección de Series que **comparten el índice**: cada columna es una Series.

```python
df = pd.DataFrame({
    "producto": ["yerba", "café", "té"],
    "precio": [3500, 9800, 1200],
    "stock": [10, 0, 25],
})

df["precio"]               # una columna → Series
df[["producto", "stock"]]  # varias columnas → DataFrame (¡doble corchete!)
df["total"] = df["precio"] * df["stock"]      # columna nueva, vectorizada
df.shape                   # (3, 4)
df.columns, df.index, df.dtypes
len(df)
```

Otras formas de crearlo:

```python
pd.DataFrame([{"a": 1, "b": 2}, {"a": 3, "b": 4}])   # lista de dicts (registros)
pd.DataFrame(matriz, columns=["x", "y"])             # desde NumPy
```

## Leer datos

```python
df = pd.read_csv("ventas.csv")
df = pd.read_csv("ventas.csv", parse_dates=["fecha"], index_col="id")
df = pd.read_csv("datos.csv", sep=";", decimal=",", encoding="latin-1")   # formato europeo
pd.read_excel("archivo.xlsx", sheet_name="Hoja1")      # necesita openpyxl
pd.read_json(...), pd.read_parquet(...), pd.read_sql(consulta, conexion)
df.to_csv("salida.csv", index=False), df.to_parquet("salida.parquet")
```

- `parse_dates` convierte columnas a fechas (`datetime64`); sin esto, quedan como texto.
- `index_col` usa una columna como índice.
- **Parquet** es el formato recomendado para guardar datos intermedios: rápido, comprimido y
  conserva los tipos.

## Explorar

```python
df.head(), df.tail(3), df.sample(5)
df.info()              # columnas, tipos, no nulos y memoria
df.describe()          # estadística de las columnas numéricas
df["sucursal"].value_counts()      # frecuencia de cada valor
df["sucursal"].unique(), df["sucursal"].nunique()
df.sort_values("total", ascending=False).head(10)
df["total"].sum(), df["total"].mean(), df["total"].idxmax()
```

`idxmax()` devuelve la **etiqueta** (no la posición) del máximo: el `argmax` de pandas.

## dtypes en pandas 3

| Dato                  | dtype                                    |
|-----------------------|------------------------------------------|
| enteros               | `int64` (o `Int64` si admite nulos)      |
| decimales             | `float64`                                |
| texto                 | `str` (el dtype de strings de pandas 3)  |
| fechas                | `datetime64[ns]`                         |
| verdadero/falso       | `bool` (o `boolean` con nulos)           |
| pocos valores repetidos | `category` (ahorra memoria)            |

`df.astype({"stock": "int32"})` convierte y `pd.to_datetime`/`pd.to_numeric` son las
conversiones "robustas" (las vemos en limpieza).

> **pandas 3 (2026)** cambió dos cosas importantes respecto de pandas 1.x y 2.x, que es lo que
> vas a ver en muchos tutoriales: **copy-on-write** está activado siempre (próximo capítulo) y
> los textos tienen un dtype propio `str` en lugar de `object`.

## Resumen

- Series = array con índice; DataFrame = columnas (Series) que comparten el índice.
- Las operaciones se alinean por etiqueta; donde no hay par, `NaN`.
- `df["col"]` da una Series, `df[["a", "b"]]` un DataFrame, y `df["nueva"] = ...` agrega columnas.
- `read_csv` con `parse_dates` e `index_col`; Parquet para guardar.
- `head`, `info`, `describe`, `value_counts`, `sort_values` e `idxmax` para explorar.

## Ejercicio

Crear Series y DataFrames, leer el CSV de ventas con los tipos correctos, agregar una columna
calculada y armar un resumen. El archivo `ventas.csv` tiene las columnas `id, fecha, sucursal,
producto, cantidad, categoria, precio_unitario`.

**Para profundizar:** [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html),
[IO tools](https://pandas.pydata.org/docs/user_guide/io.html).
