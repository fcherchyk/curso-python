# Figure and Axes: the object-oriented API

matplotlib is the most widely used plotting library in Python, and the foundation of seaborn and of
pandas' `.plot()`. It has a reputation for being confusing because it offers **two interfaces** that
get mixed up in every tutorial. Once you understand which one to use and why, the rest is finding the
right method.

```bash
uv add matplotlib
```

## The two interfaces

```python
import matplotlib.pyplot as plt

# 1. "pyplot" interface (implicit state): handy in a notebook, confusing in code
plt.plot([1, 2, 3], [4, 1, 6])
plt.title("Sales")
plt.show()

# 2. Object-oriented (OO) interface: explicit, the recommended one
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 1, 6])
ax.set_title("Sales")
```

The pyplot interface operates on "the current figure and axes", a **global state**: when there are
several charts, it isn't clear which one you're talking to. The OO interface works with objects you
hold in variables. **Use the OO interface**, especially in functions and in code that gets reused or
tested. Keep `plt` only for creating the figure (`plt.subplots`) and, in scripts, for `plt.show()`.

## The anatomy

- **Figure**: the whole "canvas"; it can contain several charts. Size, resolution and saving.
- **Axes**: one chart, with its plotting area, its X/Y axes, its title and its legend. (Don't confuse
  it with *axis*, which is each X or Y axis.)
- **Artists**: everything that gets drawn: lines, bars, text and ticks.

```python
fig, ax = plt.subplots(figsize=(8, 4))     # width x height in inches
ax.plot(months, sales, marker="o", label="2025")
ax.set_title("Monthly sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (thousands of $)")
ax.grid(True, alpha=0.3)
ax.legend()
```

Almost everything is configured with `ax.set_<something>(...)`: `set_xlim`, `set_ylim`, `set_xticks`
and `set_xticklabels`. Or all at once with `ax.set(title=..., xlabel=..., ylabel=...)`.

## Several series on the same axes

```python
ax.plot(x, a, label="North branch")
ax.plot(x, b, label="South branch", linestyle="--")
ax.legend()                      # uses the label= values
```

Each call to `ax.plot` adds a line. Colors are assigned automatically from a cycle, and you can set
them with `color=`. Line styles: `"-"`, `"--"`, `":"` and `"-."`. Markers: `"o"`, `"s"`, `"^"` and
`"x"`.

## Saving

```python
fig.savefig("sales.png", dpi=150, bbox_inches="tight")
fig.savefig("sales.svg")                 # vector: ideal for documents and the web
plt.close(fig)                           # free memory (important in loops and servers)
```

`bbox_inches="tight"` trims the extra margins. On a server or in tests there's no display: you use
the `"Agg"` *backend* (`matplotlib.use("Agg")` before importing pyplot, or the environment variable
`MPLBACKEND=Agg`) and save to a file.

## Functions that return the figure

A pattern that makes charts reusable and **testable**:

```python
def sales_chart(months: list[str], sales: list[float]) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months, sales, marker="o")
    ax.set(title="Monthly sales", xlabel="Month", ylabel="Sales")
    return fig
```

Then the caller decides whether to show it, save it or keep modifying it. In a test you inspect it:

```python
fig = sales_chart(...)
ax = fig.axes[0]
assert ax.get_title() == "Monthly sales"
line = ax.get_lines()[0]
line.get_ydata()           # the plotted data
```

That's how charts are tested in this module: by checking the **structure** (how many axes, which
lines, which titles and which data), not by comparing images pixel by pixel.

## Summary

- Use the OO API: `fig, ax = plt.subplots()` and then methods on `ax`.
- Figure = canvas, Axes = each chart; `ax.set(...)` for titles and labels.
- Several lines with `label=` and `ax.legend()`.
- `fig.savefig(..., dpi=..., bbox_inches="tight")` and `plt.close(fig)`; the `Agg` backend when there's no display.
- Functions that **return** the figure: reusable and testable.

## Exercise

A line chart with a title, labels and markers; two series with a legend; and saving the figure to
PNG.

**Further reading:** [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html),
[The two interfaces](https://matplotlib.org/stable/users/explain/figure/api_interfaces.html).
