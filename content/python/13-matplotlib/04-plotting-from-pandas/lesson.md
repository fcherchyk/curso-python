# Plotting from pandas and good practices

pandas ships `.plot` methods that call matplotlib for you: one line takes you from a table to a
chart. What they don't do is think the chart through. In this chapter we cover both sides: how to
plot quickly from a DataFrame and how to finish the chart so it explains itself.

## `.plot` on Series and DataFrame

```python
series.plot()                     # line: index on X, values on Y
df.plot()                         # one line per column, with an automatic legend
df.plot.bar()                     # bars grouped by row
series.plot.barh()
series.plot.hist(bins=30)
df.plot.scatter(x="price", y="quantity")
```

Each call returns the **Axes** it drew on. To combine it with the object-oriented API, pass your own
`ax`:

```python
fig, ax = plt.subplots(figsize=(8, 4))
df.plot(ax=ax)
ax.set_title("...")
```

That way you stay in control of the figure (size, subplots, saving) and pandas only draws.

## The shape of the data decides the chart

`df.plot()` draws **one line per column**. To get one line per branch, you first need the branches
as columns. That's exactly what `pivot_table` does:

```python
monthly = (
    sales.assign(month=sales["date"].dt.to_period("M"), amount=sales["quantity"] * sales["unit_price"])
    .pivot_table(index="month", columns="branch", values="amount", aggfunc="sum")
)
monthly.plot(ax=ax, marker="o")
```

80% of the work of plotting with pandas is **shaping the table**: the index goes on the X axis, each
column is a series and the labels come from the names.

## Good practices

A chart has to make sense **without you explaining it**.

1. **A title that states the conclusion** when there is one: "South leads in March" says more than
   "Sales by branch".
2. **Axes with units**: "Amount ($)", "Latency (ms)". Without units, the number means nothing.
3. **Less ink**: remove the top and right spines (`ax.spines[["top", "right"]].set_visible(False)`)
   and use a faint grid only on the axis people read (`ax.grid(axis="y", alpha=0.3)`).
4. **Sort** categories by value.
5. **Color with intent**: one color for everything and an accent color for what you want to
   highlight. Avoid the rainbow.
6. **Accessibility**: about 8% of men have some degree of color blindness. Use palettes designed
   for it (`viridis`, `cividis`, or the `tableau-colorblind10` style) and don't distinguish series by
   color **alone**: add markers or line styles.
7. **Readable numbers**: `ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))` adds
   thousands separators.

```python
plt.style.use("tableau-colorblind10")   # global style, colorblind-friendly
```

## A function so you don't repeat yourself

Good practices become easy when they live in a function:

```python
def style_axes(ax, title, xlabel, ylabel):
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)
    return ax
```

If you apply it to all your charts, your reports come out consistent with no effort.

## Summary

- `series.plot`/`df.plot` (and `.bar`, `.barh`, `.hist`, `.scatter`) return the Axes; pass
  `ax=` to integrate them with your figure.
- Shape the table first (`groupby`, `pivot_table`): index → X, columns → series.
- A title with the conclusion, units on the axes, less ink, sorted categories.
- Color with intent and colorblind-friendly; don't rely on color alone.

## Exercise

A line chart with one series per branch built with `pivot_table`, bars sorted by category, and a
style function that applies the good practices.

**Further reading:** [pandas: Chart visualization](https://pandas.pydata.org/docs/user_guide/visualization.html),
[Fundamentals of Data Visualization](https://clauswilke.com/dataviz/) (Claus Wilke, free online).
