# Subplots, scales and annotations

A chart almost never stands alone. Comparing several series side by side, using the right scale and
pointing out what matters is what turns a chart into an argument.

## Subplot grids

```python
fig, axs = plt.subplots(2, 2, figsize=(10, 6))   # axs is a 2x2 array of Axes
axs[0, 0].plot(x, a)
axs[1, 1].bar(cats, b)

fig, (top, bottom) = plt.subplots(2, 1)          # unpack if there are only a few
for ax, (name, series) in zip(axs.flat, all_series.items()):   # iterate over the grid
    ax.plot(series)
    ax.set_title(name)
```

- `axs.flat` iterates over the grid as if it were a list.
- `squeeze=False` always returns a 2D array, even for 1x1: useful when the number of subplots
  varies.
- `fig.suptitle("...")` sets a title for the whole figure, and `layout="constrained"` (or
  `fig.tight_layout()`) keeps titles and labels from overlapping.

## Shared axes

```python
fig, axs = plt.subplots(3, 1, sharex=True)     # same X scale: dates line up
fig, axs = plt.subplots(1, 3, sharey=True)     # same Y scale: honest comparison
```

With `sharey=True`, all panels have the same vertical range. **Without shared axes, two panels can
look the same even if one is worth 10 times more than the other.** If the goal is to compare
magnitudes, share the axis.

## Logarithmic scale

```python
ax.set_yscale("log")
```

On a log scale, **equal distances are equal multiplications**: going from 10 to 100 takes up the
same space as going from 100 to 1000. Use it when:

- The data spans several orders of magnitude (population, income, latencies).
- What matters is **percentage growth**: a price growing at a constant rate looks like a straight
  line. That's why long-term charts of a stock index use a log scale.

It doesn't work with values ≤ 0. Say in the axis label that the scale is logarithmic.

## Dual Y axis: handle with care

```python
ax2 = ax.twinx()   # second Y axis, on the right
```

Two scales in the same panel let you "manufacture" any correlation by moving the ranges. Two
subplots with `sharex=True` are almost always better.

## Annotations

```python
ax.axhline(0, color="gray", linewidth=0.8)             # horizontal reference line
ax.axvspan(start, end, alpha=0.2, color="red")         # shade a period
ax.annotate(
    "maximum",
    xy=(x_max, y_max),               # the point being marked
    xytext=(x_max, y_max * 1.1),     # where the text goes
    arrowprops={"arrowstyle": "->"},
)
ax.text(0.02, 0.95, "n = 500", transform=ax.transAxes)  # coordinates relative to the panel
```

`transform=ax.transAxes` makes (0, 0) the bottom-left corner of the panel and (1, 1) the top-right
one, regardless of the data. It's useful for fixed notes.

## Legends

```python
ax.plot(x, a, label="North")
ax.legend(loc="upper left", frameon=False)
ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))   # outside, on the right
```

With only a few series, labeling the end of each line with `ax.text` is sometimes clearer than a
legend: the eye doesn't have to go back and forth.

## Summary

- `plt.subplots(r, c)` returns an array of Axes; iterate over it with `axs.flat`.
- `sharex`/`sharey` for honest comparisons; `suptitle` and `layout="constrained"`.
- Log scale for orders of magnitude and percentage growth.
- Avoid `twinx`; prefer panels with a shared X axis.
- `annotate`, `axhline`, `axvspan` and `text` with `transAxes` to point out what matters.

## Exercise

A grid of panels with a shared Y axis, a log-scale chart and an annotation at the maximum of a
series.

**Further reading:** [Arranging multiple Axes](https://matplotlib.org/stable/users/explain/axes/arranging_axes.html),
[Annotations](https://matplotlib.org/stable/users/explain/text/annotations.html).
