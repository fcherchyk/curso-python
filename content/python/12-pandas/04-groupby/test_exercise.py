import csv
from collections import defaultdict

import pandas as pd
import pytest
from exercise import (
    branch_category_table,
    category_summary,
    share_of_branch,
    top_product_by_branch,
    total_by_branch,
)

# References computed in pure Python (no pandas)
with open("sales.csv", newline="", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))
for row in ROWS:
    row["total"] = int(row["quantity"]) * int(row["unit_price"])

BY_BRANCH: dict[str, int] = defaultdict(int)
for row in ROWS:
    BY_BRANCH[row["branch"]] += row["total"]


@pytest.fixture
def sales():
    df = pd.read_csv("sales.csv", index_col="id", parse_dates=["date"])
    df["total"] = df["quantity"] * df["unit_price"]
    return df


def test_total_by_branch(sales):
    result = total_by_branch(sales)
    assert result.to_dict() == dict(BY_BRANCH)
    assert result.is_monotonic_decreasing


def test_category_summary(sales):
    result = category_summary(sales)
    assert list(result.columns) == ["units", "revenue", "average_ticket", "products"]
    assert result["revenue"].is_monotonic_decreasing
    beverages = [r for r in ROWS if r["category"] == "beverages"]
    row = result.loc["beverages"]
    assert row["units"] == sum(int(r["quantity"]) for r in beverages)
    assert row["revenue"] == sum(r["total"] for r in beverages)
    assert row["average_ticket"] == round(sum(r["total"] for r in beverages) / len(beverages), 2)
    assert row["products"] == len({r["product"] for r in beverages})


def test_share_of_branch(sales):
    result = share_of_branch(sales)
    assert result.index.equals(sales.index)
    first = ROWS[0]
    assert result.loc[int(first["id"])] == pytest.approx(first["total"] / BY_BRANCH[first["branch"]])
    assert result.groupby(sales["branch"]).sum().round(9).eq(1).all()


def test_branch_category_table(sales):
    table = branch_category_table(sales)
    assert sorted(table.index) == sorted(BY_BRANCH)
    assert table.sum(axis=1).to_dict() == dict(BY_BRANCH)
    expected = sum(r["total"] for r in ROWS if r["branch"] == "South" and r["category"] == "pantry")
    assert table.loc["South", "pantry"] == expected
    assert (table >= 0).all().all()


def test_top_product_by_branch(sales):
    units: dict[tuple[str, str], int] = defaultdict(int)
    for r in ROWS:
        units[(r["branch"], r["product"])] += int(r["quantity"])
    expected = {}
    for branch in BY_BRANCH:
        candidates = {p: u for (b, p), u in units.items() if b == branch}
        expected[branch] = max(candidates, key=candidates.get)
    assert top_product_by_branch(sales) == expected
