# Combinar tablas: merge, join y concat

Los datos casi nunca vienen en una sola tabla: las ventas por un lado, el catálogo de productos
por otro, cada mes en un archivo distinto. pandas combina tablas de dos formas: **por clave**
(`merge`, el `JOIN` de SQL) y **apilando** (`concat`, el `UNION`). La parte difícil no es la
sintaxis, sino **no perder ni duplicar filas sin darte cuenta**, y para eso pandas tiene
herramientas de validación que conviene usar siempre.

## `merge`: unir por columnas clave

```python
ventas.merge(productos, on="producto", how="left")
```

| `how`     | Qué filas quedan                                         | SQL                 |
|-----------|----------------------------------------------------------|---------------------|
| `"inner"` | solo las que tienen clave en **ambas** tablas (default)  | `INNER JOIN`        |
| `"left"`  | **todas** las de la izquierda; sin match → NaN           | `LEFT JOIN`         |
| `"right"` | todas las de la derecha                                  | `RIGHT JOIN`        |
| `"outer"` | todas las de las dos                                      | `FULL OUTER JOIN`   |
| `"cross"` | producto cartesiano                                       | `CROSS JOIN`        |

Para enriquecer una tabla de hechos (ventas) con atributos (el catálogo), lo habitual es
**`left`**: no querés perder ventas por un producto que falta en el catálogo.

```python
# Claves con nombres distintos
pedidos.merge(clientes, left_on="cliente_id", right_on="id", suffixes=("", "_cliente"))
# Varias claves
a.merge(b, on=["sucursal", "fecha"])
```

## Las trampas: filas que se pierden o se multiplican

1. **Con `inner`, perdés filas en silencio** si alguna clave no está en la otra tabla.
2. **Si la clave se repite en la tabla de la derecha, las filas de la izquierda se
   multiplican.** Un producto duplicado en el catálogo duplica todas sus ventas, y los totales
   quedan inflados sin ningún error.

### `validate`: que pandas verifique tus supuestos

```python
ventas.merge(productos, on="producto", how="left", validate="many_to_one")
```

Con `validate`, pandas **levanta `MergeError`** si la relación no es la que declaraste:
`"one_to_one"`, `"one_to_many"`, `"many_to_one"` o `"many_to_many"`. Es una línea que te ahorra
horas de buscar por qué los números no cierran. Usalo siempre.

### `indicator`: ¿de dónde vino cada fila?

```python
r = ventas.merge(productos, on="producto", how="left", indicator=True)
r["_merge"].value_counts()      # both / left_only / right_only
r.loc[r["_merge"] == "left_only", "producto"].unique()   # ventas sin producto en catálogo
```

Es la forma idiomática de encontrar las claves "huérfanas" (el *anti-join*).

### Verificá antes y después

```python
assert productos["producto"].is_unique                     # la clave es única
assert len(resultado) == len(ventas)                       # un left many-to-one no agrega filas
```

## `join`: merge por índice

```python
ventas.join(productos.set_index("producto"), on="producto")
df1.join(df2)                   # índice contra índice
```

Es un atajo de `merge` cuando la clave de la derecha es su índice.

## `concat`: apilar

```python
enero = pd.read_csv("ventas_2025_01.csv")
febrero = pd.read_csv("ventas_2025_02.csv")

pd.concat([enero, febrero], ignore_index=True)         # una debajo de la otra
pd.concat({"ene": enero, "feb": febrero})               # con un nivel de índice que indica el origen
pd.concat([a, b], axis=1)                               # lado a lado (alineando por índice)
```

- `ignore_index=True` renumera el índice (si no, quedan índices repetidos).
- Pasar un **dict** agrega una etiqueta de origen, que se convierte en columna con
  `.reset_index(level=0)`.
- Si las columnas no coinciden, las que faltan quedan con `NaN`.
- **No hagas `concat` dentro de un bucle** (es cuadrático): juntá los DataFrames en una lista y
  concatená una sola vez.

```python
partes = [pd.read_csv(ruta) for ruta in sorted(Path("datos").glob("ventas_*.csv"))]
todas = pd.concat(partes, ignore_index=True)
```

## Resumen

- `merge(on=..., how=...)`: `left` para enriquecer sin perder filas.
- **Siempre** `validate="many_to_one"` (o la relación que corresponda) para detectar claves
  duplicadas.
- `indicator=True` para encontrar las filas sin match.
- `join` cuando la clave es el índice.
- `concat` para apilar (con `ignore_index` o un dict para el origen); juntar en una lista y
  concatenar una vez.

## Ejercicio

`ventas.csv` (id, fecha, sucursal, producto, cantidad) y `productos.csv` (producto, categoria,
precio_unitario). En el catálogo **falta un producto** que sí aparece en las ventas.

**Para profundizar:** [Merge, join, concatenate and compare](https://pandas.pydata.org/docs/user_guide/merging.html).
