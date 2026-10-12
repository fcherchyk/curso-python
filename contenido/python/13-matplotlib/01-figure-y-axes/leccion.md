# Figure y Axes: la API orientada a objetos

matplotlib es la librería de gráficos más usada de Python, y la base de seaborn y de los
`.plot()` de pandas. Tiene fama de confusa porque ofrece **dos interfaces** que se mezclan en
todos los tutoriales. Si entendés cuál usar y por qué, el resto es buscar el método adecuado.

```bash
uv add matplotlib
```

## Las dos interfaces

```python
import matplotlib.pyplot as plt

# 1. Interfaz "pyplot" (estado implícito): cómoda en un notebook, confusa en código
plt.plot([1, 2, 3], [4, 1, 6])
plt.title("Ventas")
plt.show()

# 2. Interfaz orientada a objetos (OO): explícita, la recomendada
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 1, 6])
ax.set_title("Ventas")
```

La interfaz pyplot opera sobre "la figura y los ejes actuales", un **estado global**: cuando hay
varios gráficos, no queda claro a cuál le estás hablando. La OO trabaja con objetos que tenés en
variables. **Usá la OO**, especialmente en funciones y en código que se reutiliza o se testea.
`plt` queda solo para crear la figura (`plt.subplots`) y, en scripts, para `plt.show()`.

## La anatomía

- **Figure**: el "lienzo" completo; puede contener varios gráficos. Tamaño, resolución y guardado.
- **Axes**: un gráfico, con su área de dibujo, sus ejes X/Y, su título y su leyenda. (No confundir
  con *axis*, que es cada eje X o Y.)
- **Artists**: todo lo que se dibuja: líneas, barras, textos y ticks.

```python
fig, ax = plt.subplots(figsize=(8, 4))     # ancho x alto en pulgadas
ax.plot(meses, ventas, marker="o", label="2025")
ax.set_title("Ventas mensuales")
ax.set_xlabel("Mes")
ax.set_ylabel("Ventas (miles de $)")
ax.grid(True, alpha=0.3)
ax.legend()
```

Casi todo se configura con `ax.set_<algo>(...)`: `set_xlim`, `set_ylim`, `set_xticks` y
`set_xticklabels`. O todo junto con `ax.set(title=..., xlabel=..., ylabel=...)`.

## Varias series en los mismos ejes

```python
ax.plot(x, a, label="Sucursal Norte")
ax.plot(x, b, label="Sucursal Sur", linestyle="--")
ax.legend()                      # usa los label=
```

Cada llamada a `ax.plot` agrega una línea. Los colores se asignan automáticamente de un ciclo, y
se pueden fijar con `color=`. Estilos de línea: `"-"`, `"--"`, `":"` y `"-."`. Marcadores: `"o"`,
`"s"`, `"^"` y `"x"`.

## Guardar

```python
fig.savefig("ventas.png", dpi=150, bbox_inches="tight")
fig.savefig("ventas.svg")                # vectorial: ideal para documentos y la web
plt.close(fig)                           # liberar memoria (importante en bucles y servidores)
```

`bbox_inches="tight"` recorta los márgenes sobrantes. En un servidor o en tests no hay pantalla:
se usa el *backend* `"Agg"` (`matplotlib.use("Agg")` antes de importar pyplot, o la variable de
entorno `MPLBACKEND=Agg`) y se guarda a archivo.

## Funciones que devuelven la figura

Un patrón que hace los gráficos reutilizables y **testeables**:

```python
def grafico_ventas(meses: list[str], ventas: list[float]) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(meses, ventas, marker="o")
    ax.set(title="Ventas mensuales", xlabel="Mes", ylabel="Ventas")
    return fig
```

Después, quien llama decide si mostrarla, guardarla o seguir modificándola. En un test se inspecciona:

```python
fig = grafico_ventas(...)
ax = fig.axes[0]
assert ax.get_title() == "Ventas mensuales"
linea = ax.get_lines()[0]
linea.get_ydata()          # los datos graficados
```

Así se testean los gráficos en este módulo: verificando la **estructura** (cuántos ejes, qué
líneas, qué títulos y qué datos), no comparando imágenes píxel a píxel.

## Resumen

- Usá la API OO: `fig, ax = plt.subplots()` y después métodos de `ax`.
- Figure = lienzo, Axes = cada gráfico; `ax.set(...)` para títulos y etiquetas.
- Varias líneas con `label=` y `ax.legend()`.
- `fig.savefig(..., dpi=..., bbox_inches="tight")` y `plt.close(fig)`; backend `Agg` sin pantalla.
- Funciones que **devuelven** la figura: reutilizables y testeables.

## Ejercicio

Un gráfico de línea con título, etiquetas y marcadores; dos series con leyenda; y guardar la
figura a PNG.

**Para profundizar:** [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html),
[The two interfaces](https://matplotlib.org/stable/users/explain/figure/api_interfaces.html).
