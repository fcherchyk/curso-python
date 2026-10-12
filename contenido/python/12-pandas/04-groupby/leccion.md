# groupby: agrupar y agregar

"¿Cuánto vendió cada sucursal?", "¿Cuál es el ticket promedio por categoría?", "¿Qué
participación tiene cada venta dentro de su sucursal?" Casi toda pregunta de negocio es una
**agregación por grupos**. En pandas se resuelve con `groupby`, que sigue el patrón
**split-apply-combine**: separar las filas en grupos, aplicar una operación a cada grupo y
combinar los resultados.

## Lo básico

```python
ventas.groupby("sucursal")["total"].sum()
# sucursal
# Centro    230900
# Norte     245400
# Sur       380300
# Name: total, dtype: int64

ventas.groupby("sucursal")["total"].agg(["sum", "mean", "count"])
ventas.groupby(["sucursal", "categoria"])["cantidad"].sum()   # varias claves → MultiIndex
ventas.groupby("sucursal").size()          # cantidad de filas por grupo
```

- Las claves del grupo pasan a ser el **índice** del resultado. Con `as_index=False`, o con
  `.reset_index()`, quedan como columnas.
- Agregaciones comunes: `sum`, `mean`, `median`, `count` (no nulos), `size` (filas), `min`, `max`,
  `std`, `nunique`, `first` y `last`.
- Es el equivalente directo del `GROUP BY` de SQL.

## Agregaciones con nombre: el estilo recomendado

```python
resumen = ventas.groupby("categoria").agg(
    unidades=("cantidad", "sum"),
    facturacion=("total", "sum"),
    ticket_promedio=("total", "mean"),
    productos_distintos=("producto", "nunique"),
).sort_values("facturacion", ascending=False)
```

Cada argumento es `nombre_de_salida=(columna, función)`. El resultado tiene columnas con nombres
claros y no un MultiIndex de columnas difícil de manejar. La función también puede ser una propia:
`("total", lambda s: s.quantile(0.9))`.

## `transform`: el resultado del grupo, en cada fila

`agg` **reduce** cada grupo a una fila. `transform` devuelve un valor **por cada fila original**,
alineado con el DataFrame. Es lo que hace falta para comparar cada fila con su grupo:

```python
total_sucursal = ventas.groupby("sucursal")["total"].transform("sum")
ventas["participacion"] = ventas["total"] / total_sucursal

# Desvío respecto del promedio de la categoría
ventas["vs_promedio"] = ventas["total"] - ventas.groupby("categoria")["total"].transform("mean")
```

Sin `transform`, habría que agregar, hacer un merge del resultado de vuelta a las filas y
después dividir.

## `filter` y `apply`

```python
# Solo los grupos (sucursales) con más de 20 ventas
ventas.groupby("sucursal").filter(lambda g: len(g) > 20)

# apply: una función arbitraria por grupo (flexible pero más lenta)
ventas.groupby("sucursal").apply(lambda g: g.nlargest(2, "total"))
```

Preferí `agg`/`transform` con funciones con nombre (`"sum"`, `"mean"`): están optimizadas. Usá
`apply` solo cuando no hay alternativa.

## "El mayor de cada grupo"

Un patrón muy común: el producto más vendido **de cada** sucursal.

```python
unidades = ventas.groupby(["sucursal", "producto"])["cantidad"].sum()
idx = unidades.groupby(level="sucursal").idxmax()      # (sucursal, producto) del máximo
unidades.loc[idx]
```

Otra forma: `sort_values` + `groupby(...).head(1)`, o `.nlargest(1)` dentro del grupo.

## Tablas dinámicas: `pivot_table`

La tabla dinámica de las planillas de cálculo:

```python
pd.pivot_table(
    ventas,
    values="total",
    index="sucursal",          # filas
    columns="categoria",       # columnas
    aggfunc="sum",
    fill_value=0,
    margins=True,              # totales de fila y columna ("All")
)
```

`pd.crosstab(ventas["sucursal"], ventas["categoria"])` cuenta frecuencias, y
`.unstack()`/`.stack()` pasan un nivel del índice a columnas y viceversa.

## Agrupar por tiempo

Con fechas se puede agrupar por período:

```python
ventas.groupby(ventas["fecha"].dt.month)["total"].sum()
ventas.groupby(pd.Grouper(key="fecha", freq="ME"))["total"].sum()    # por fin de mes
```

En el capítulo de series de tiempo lo vemos con `resample`.

## Resumen

- `groupby(clave)[col].agg(...)`: split-apply-combine, como el `GROUP BY` de SQL.
- Agregaciones con nombre: `agg(salida=("columna", "función"))`.
- `transform` devuelve un valor por fila (participaciones, desvíos respecto del grupo).
- `filter` para descartar grupos; `apply` solo como último recurso.
- El mayor por grupo: `groupby(...).idxmax()` o `sort_values` + `head(1)`.
- `pivot_table` para tablas cruzadas.

## Ejercicio

Sobre las ventas: totales por sucursal, un resumen por categoría con agregaciones con nombre,
participación de cada venta en su sucursal, una tabla dinámica y el producto top de cada
sucursal.

**Para profundizar:** [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html),
[Reshaping and pivot tables](https://pandas.pydata.org/docs/user_guide/reshaping.html).
