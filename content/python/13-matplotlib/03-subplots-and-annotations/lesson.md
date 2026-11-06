# Subplots, escalas y anotaciones

Un gráfico casi nunca vive solo. Comparar varias series lado a lado, usar la escala correcta y
señalar lo importante es lo que convierte un gráfico en un argumento.

## Grillas de subplots

```python
fig, axs = plt.subplots(2, 2, figsize=(10, 6))   # axs es un array 2x2 de Axes
axs[0, 0].plot(x, a)
axs[1, 1].bar(cats, b)

fig, (arriba, abajo) = plt.subplots(2, 1)        # desempaquetar si son pocos
for ax, (nombre, serie) in zip(axs.flat, series.items()):   # recorrer la grilla
    ax.plot(serie)
    ax.set_title(nombre)
```

- `axs.flat` recorre la grilla como si fuera una lista.
- `squeeze=False` devuelve siempre un array 2D, incluso con 1x1: útil si la cantidad de
  subplots es variable.
- `fig.suptitle("...")` pone un título para toda la figura, y `layout="constrained"` (o
  `fig.tight_layout()`) evita que se pisen los títulos y las etiquetas.

## Ejes compartidos

```python
fig, axs = plt.subplots(3, 1, sharex=True)     # misma escala X: se alinean las fechas
fig, axs = plt.subplots(1, 3, sharey=True)     # misma escala Y: comparación honesta
```

Con `sharey=True`, todos los paneles tienen el mismo rango vertical. **Sin ejes compartidos,
dos paneles pueden parecer iguales aunque uno valga 10 veces más que el otro.** Si el objetivo
es comparar magnitudes, compartí el eje.

## Escala logarítmica

```python
ax.set_yscale("log")
```

En escala log, **distancias iguales son multiplicaciones iguales**: pasar de 10 a 100 ocupa lo
mismo que pasar de 100 a 1000. Úsala cuando:

- Los datos abarcan varios órdenes de magnitud (población, ingresos, latencias).
- Lo que importa es el **crecimiento porcentual**: un precio que crece a tasa constante se ve
  como una recta. Por eso los gráficos de largo plazo de un índice bursátil van en log.

No sirve con valores ≤ 0. Avisá en la etiqueta del eje que la escala es logarítmica.

## Doble eje Y: con cuidado

```python
ax2 = ax.twinx()   # segundo eje Y, a la derecha
```

Dos escalas en el mismo panel permiten "fabricar" cualquier correlación moviendo los rangos.
Casi siempre es mejor usar dos subplots con `sharex=True`.

## Anotaciones

```python
ax.axhline(0, color="gray", linewidth=0.8)             # línea de referencia horizontal
ax.axvspan(inicio, fin, alpha=0.2, color="red")        # sombrear un período
ax.annotate(
    "máximo",
    xy=(x_max, y_max),               # el punto señalado
    xytext=(x_max, y_max * 1.1),     # dónde va el texto
    arrowprops={"arrowstyle": "->"},
)
ax.text(0.02, 0.95, "n = 500", transform=ax.transAxes)  # coordenadas relativas al panel
```

`transform=ax.transAxes` hace que (0, 0) sea la esquina inferior izquierda del panel y (1, 1)
la superior derecha, sin importar los datos. Sirve para notas fijas.

## Leyendas

```python
ax.plot(x, a, label="Norte")
ax.legend(loc="upper left", frameon=False)
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))   # afuera, a la derecha
```

Con pocas series, a veces es más claro etiquetar el final de cada línea con `ax.text` que usar
una leyenda: el ojo no tiene que ir y volver.

## Resumen

- `plt.subplots(f, c)` devuelve un array de Axes; recorrelo con `axs.flat`.
- `sharex`/`sharey` para comparar con honestidad; `suptitle` y `layout="constrained"`.
- Escala log para órdenes de magnitud y crecimiento porcentual.
- Evitá `twinx`; preferí paneles con el eje X compartido.
- `annotate`, `axhline`, `axvspan` y `text` con `transAxes` para señalar lo importante.

## Ejercicio

Una grilla de paneles con el eje Y compartido, un gráfico en escala log y una anotación en el
máximo de una serie.

**Para profundizar:** [Arranging multiple Axes](https://matplotlib.org/stable/users/explain/axes/arranging_axes.html),
[Annotations](https://matplotlib.org/stable/users/explain/text/annotations.html).
