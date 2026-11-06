# Chart types: which one to use and when

Picking the wrong chart type is the most common visualization mistake, and the most harmful: the
chart "works" but conveys something else. The rule is to start from the **question** you want to
answer and pick the chart that answers it at a glance.

## The quick guide

| Question                                    | Chart                       | matplotlib            |
|---------------------------------------------|-----------------------------|-----------------------|
| How does something change over time?        | lines                       | `ax.plot`             |
| How do categories compare?                  | bars (horizontal if the names are long) | `ax.bar` / `ax.barh` |
| Is there a relationship between two variables? | scatter                  | `ax.scatter`          |
| How are the values distributed?             | histogram (or boxplot)      | `ax.hist` / `ax.boxplot` |
| What part of the total is each one?         | stacked or 100% bars        | `ax.bar(..., bottom=)` |

## Lines: trends

```python
ax.plot(dates, prices)
ax.plot(dates, moving_average, linestyle="--", linewidth=1)
```

For **ordered, continuous** data, typically over time. Don't connect unordered categories (branches,
products) with lines: the line suggests a continuity that doesn't exist.

## Bars: comparing categories

```python
ax.bar(categories, values)                        # vertical
ax.barh(categories, values)                       # horizontal: better with long names
ax.bar_label(ax.containers[0], fmt="%.0f")        # the value on each bar
```

- **Sort the bars** by value (unless the category has a natural order, like months): the comparison
  becomes immediate.
- **The Y axis of a bar chart starts at 0.** Cutting it exaggerates the differences and is the most
  common way to lie with a chart.
- For grouped bars, shift the X positions:
  `ax.bar(x - w/2, a, w)` and `ax.bar(x + w/2, b, w)`.

## Scatter: the relationship between variables

```python
ax.scatter(advertising, sales, alpha=0.6, s=20)       # s = size, alpha = transparency
ax.scatter(x, y, c=numeric_category, cmap="viridis")  # color by a third variable
```

With many points, `alpha` keeps them from hiding each other. If you see a shape (a line, a curve,
clusters), there's a relationship. Careful: **correlation does not imply causation**.

## Histogram: distribution

```python
ax.hist(returns, bins=30, edgecolor="white")
ax.axvline(returns.mean(), color="red", linestyle="--", label="mean")
```

It shows **how many values fall in each range**. The number of `bins` changes the reading a lot:
with too few the shape is hidden, and with too many you see noise. Try several. The **boxplot**
(`ax.boxplot`) summarizes the same information (median, quartiles and outliers) and is useful for
comparing several distributions side by side.

## What about the pie chart?

`ax.pie` exists, but people are very bad at comparing angles and areas. With more than 3 or 4
slices, a sorted horizontal bar chart says the same thing, better.

## What the methods return

Each drawing method returns the *artists* it created, and the Axes keep them:

```python
bars = ax.bar(["a", "b"], [3, 5])           # BarContainer
[b.get_height() for b in bars]              # [3, 5]
ax.patches                                  # rectangles (bars and histogram)
ax.collections                              # scatter (PathCollection)
ax.get_lines()                              # lines
```

That's how charts are inspected in this module's tests.

## Summary

- Start from the question: trend → line, comparison → bars, relationship → scatter,
  distribution → histogram or boxplot.
- Sorted bars, with the axis starting at 0; `barh` for long names; `bar_label` for the values.
- Scatter with `alpha` when there are many points; correlation is not causation.
- Histogram: try several `bins`.
- Avoid pies with many slices.

## Exercise

Sorted bars with labels, a scatter plot with transparency, a histogram with the mean line, and a
function that picks the chart type based on the question.

**Further reading:** [Plot types](https://matplotlib.org/stable/plot_types/index.html),
[From Data to Viz](https://www.data-to-viz.com/) (how to choose a chart).
