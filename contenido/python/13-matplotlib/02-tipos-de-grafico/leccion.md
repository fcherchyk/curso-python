# Tipos de gráfico: cuál usar y cuándo

Elegir mal el tipo de gráfico es el error de visualización más común, y el más dañino: el
gráfico "funciona" pero transmite otra cosa. La regla es empezar por la **pregunta** que querés
responder y elegir el gráfico que la contesta de un vistazo.

## La guía rápida

| Pregunta                                    | Gráfico                    | matplotlib            |
|---------------------------------------------|----------------------------|-----------------------|
| ¿Cómo evoluciona algo en el tiempo?          | líneas                      | `ax.plot`             |
| ¿Cómo se comparan categorías?               | barras (horizontales si los nombres son largos) | `ax.bar` / `ax.barh` |
| ¿Hay relación entre dos variables?          | dispersión                  | `ax.scatter`          |
| ¿Cómo se distribuyen los valores?            | histograma (o boxplot)      | `ax.hist` / `ax.boxplot` |
| ¿Qué parte del total es cada uno?            | barras apiladas o al 100 %  | `ax.bar(..., bottom=)` |

## Líneas: evolución

```python
ax.plot(fechas, precios)
ax.plot(fechas, media_movil, linestyle="--", linewidth=1)
```

Para datos **ordenados y continuos**, típicamente en el tiempo. No unas con líneas categorías
sin orden (sucursales, productos): la línea sugiere una continuidad que no existe.

## Barras: comparar categorías

```python
ax.bar(categorias, valores)                       # verticales
ax.barh(categorias, valores)                      # horizontales: mejor con nombres largos
ax.bar_label(ax.containers[0], fmt="%.0f")        # el valor sobre cada barra
```

- **Ordená las barras** por valor (salvo que la categoría tenga un orden natural, como meses):
  la comparación se vuelve inmediata.
- **El eje Y de las barras empieza en 0.** Cortarlo exagera las diferencias y es la manera más
  común de mentir con un gráfico.
- Para barras agrupadas, se desplazan las posiciones X:
  `ax.bar(x - w/2, a, w)` y `ax.bar(x + w/2, b, w)`.

## Dispersión: relación entre variables

```python
ax.scatter(publicidad, ventas, alpha=0.6, s=20)       # s = tamaño, alpha = transparencia
ax.scatter(x, y, c=categoria_numerica, cmap="viridis")  # color por una tercera variable
```

Con muchos puntos, `alpha` evita que se tapen. Si ves una forma (una recta, una curva, grupos),
hay una relación. Ojo: **correlación no implica causalidad**.

## Histograma: distribución

```python
ax.hist(retornos, bins=30, edgecolor="white")
ax.axvline(retornos.mean(), color="red", linestyle="--", label="media")
```

Muestra **cuántos valores caen en cada rango**. La cantidad de `bins` cambia mucho la lectura:
con pocos se esconde la forma y con muchos se ve ruido. Probá varias. El **boxplot**
(`ax.boxplot`) resume la misma información (mediana, cuartiles y outliers) y sirve para comparar
varias distribuciones lado a lado.

## ¿Y el gráfico de torta?

`ax.pie` existe, pero las personas comparan muy mal ángulos y áreas. Con más de 3 o 4 porciones,
una barra horizontal ordenada comunica lo mismo, mejor.

## Lo que devuelven los métodos

Cada método de dibujo devuelve los *artists* que creó, y los Axes los guardan:

```python
barras = ax.bar(["a", "b"], [3, 5])        # BarContainer
[b.get_height() for b in barras]            # [3, 5]
ax.patches                                  # rectángulos (barras e histograma)
ax.collections                              # scatter (PathCollection)
ax.get_lines()                              # líneas
```

Así se inspeccionan los gráficos en los tests de este módulo.

## Resumen

- Empezá por la pregunta: evolución → línea, comparación → barras, relación → dispersión,
  distribución → histograma o boxplot.
- Barras ordenadas, con el eje desde 0; `barh` con nombres largos; `bar_label` para los valores.
- Dispersión con `alpha` cuando hay muchos puntos; correlación no es causalidad.
- Histograma: probá varios `bins`.
- Evitá las tortas con muchas porciones.

## Ejercicio

Barras ordenadas con etiquetas, dispersión con transparencia, un histograma con la línea de la
media y una función que elige el tipo de gráfico según la pregunta.

**Para profundizar:** [Plot types](https://matplotlib.org/stable/plot_types/index.html),
[From Data to Viz](https://www.data-to-viz.com/) (cómo elegir el gráfico).
