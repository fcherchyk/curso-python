# Graficar desde pandas y buenas prácticas

pandas trae métodos `.plot` que llaman a matplotlib por vos: con una línea pasás de una tabla a
un gráfico. Lo que no hacen es pensar el gráfico. En este capítulo vemos los dos lados: cómo
graficar rápido desde un DataFrame y cómo terminar el gráfico para que se entienda solo.

## `.plot` de Series y DataFrame

```python
serie.plot()                      # línea: índice en X, valores en Y
df.plot()                         # una línea por columna, con leyenda automática
df.plot.bar()                     # barras agrupadas por fila
serie.plot.barh()
serie.plot.hist(bins=30)
df.plot.scatter(x="precio", y="cantidad")
```

Cada llamada devuelve el **Axes** donde dibujó. Para combinarlo con la API orientada a objetos,
pasá tu propio `ax`:

```python
fig, ax = plt.subplots(figsize=(8, 4))
df.plot(ax=ax)
ax.set_title("...")
```

Así seguís teniendo el control de la figura (tamaño, subplots, guardado) y pandas solo dibuja.

## La forma de los datos decide el gráfico

`df.plot()` dibuja **una línea por columna**. Para tener una línea por sucursal, primero hay que
dejar las sucursales como columnas. Esto es exactamente lo que hace `pivot_table`:

```python
mensual = (
    ventas.assign(mes=ventas["fecha"].dt.to_period("M"), importe=ventas["cantidad"] * ventas["precio_unitario"])
    .pivot_table(index="mes", columns="sucursal", values="importe", aggfunc="sum")
)
mensual.plot(ax=ax, marker="o")
```

El 80 % del trabajo de graficar con pandas es **dar forma a la tabla**: el índice va al eje X, cada
columna es una serie y las etiquetas salen de los nombres.

## Buenas prácticas

Un gráfico tiene que entenderse **sin que lo expliques**.

1. **Título que diga la conclusión** cuando la hay: "Sur lidera en marzo" comunica más que
   "Ventas por sucursal".
2. **Ejes con unidades**: "Importe ($)", "Latencia (ms)". Sin unidades, el número no significa
   nada.
3. **Menos tinta**: sacá los bordes superior y derecho (`ax.spines[["top", "right"]].set_visible(False)`)
   y usá una grilla tenue solo en el eje que se lee (`ax.grid(axis="y", alpha=0.3)`).
4. **Ordená** las categorías por valor.
5. **Color con intención**: un color para todo y un color de acento para lo que querés
   destacar. Evitá el arcoíris.
6. **Accesibilidad**: alrededor del 8 % de los hombres tiene algún grado de daltonismo. Usá
   paletas pensadas para eso (`viridis`, `cividis`, o el estilo `tableau-colorblind10`) y no
   distingas series **solo** por el color: sumá marcadores o estilos de línea.
7. **Números legibles**: `ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))` pone
   separadores de miles.

```python
plt.style.use("tableau-colorblind10")   # estilo global, apto para daltonismo
```

## Una función para no repetirte

Las buenas prácticas se vuelven fáciles cuando están en una función:

```python
def estilizar(ax, titulo, xlabel, ylabel):
    ax.set(title=titulo, xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    return ax
```

Si la aplicás a todos tus gráficos, los reportes salen consistentes sin esfuerzo.

## Resumen

- `serie.plot`/`df.plot` (y `.bar`, `.barh`, `.hist`, `.scatter`) devuelven el Axes; pasá
  `ax=` para integrarlos con tu figura.
- Dale forma a la tabla primero (`groupby`, `pivot_table`): índice → X, columnas → series.
- Título con la conclusión, unidades en los ejes, menos tinta, categorías ordenadas.
- Color con intención y apto para daltonismo; no dependas solo del color.

## Ejercicio

Un gráfico de líneas con una serie por sucursal armado con `pivot_table`, barras ordenadas por
categoría y una función de estilo que aplica las buenas prácticas.

**Para profundizar:** [pandas: Chart visualization](https://pandas.pydata.org/docs/user_guide/visualization.html),
[Fundamentals of Data Visualization](https://clauswilke.com/dataviz/) (Claus Wilke, gratis online).
