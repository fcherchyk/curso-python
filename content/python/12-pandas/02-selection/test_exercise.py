import csv

import pandas as pd
import pytest
from exercise import (
    for_products,
    large_sales_at,
    lookup,
    top_and_first_label,
    with_discount,
)

with open("sales.csv", newline="", encoding="utf-8") as f:
    ROWS = [
        {**r, "id": int(r["id"]), "quantity": int(r["quantity"]), "price": int(r["unit_price"])}
        for r in csv.DictReader(f)
    ]
for r in ROWS:
    r["total"] = r["quantity"] * r["price"]


@pytest.fixture
def sales():
    df = pd.read_csv("sales.csv", index_col="id", parse_dates=["date"])
    df["total"] = df["quantity"] * df["unit_price"]
    return df


def test_large_sales_at(sales):
    result = large_sales_at(sales, "Central", 10_000)
    expected = sorted(
        (r for r in ROWS if r["branch"] == "Central" and r["total"] >= 10_000),
        key=lambda r: -r["total"],
    )
    assert list(result.columns) == ["product", "total"]
    assert result["total"].tolist() == [r["total"] for r in expected]


def test_for_products(sales):
    result = for_products(sales, ["cocoa", "mug"])
    assert result.sum() == sum(r["quantity"] for r in ROWS if r["product"] in ("cocoa", "mug"))


def test_lookup(sales):
    expected = sorted(r["id"] for r in ROWS if r["category"] == "beverages" and r["quantity"] >= 5)
    assert lookup(sales, "beverages", 5) == expected


def test_top_and_first_label(sales):
    top = max(ROWS, key=lambda r: r["total"])
    assert top_and_first_label(sales) == (top["id"], ROWS[0]["quantity"])


def test_with_discount_does_not_mutate(sales):
    before = sales.copy()
    result = with_discount(sales, "beverages", 0.1)
    pd.testing.assert_frame_equal(sales, before)
    beverage = next(r for r in ROWS if r["category"] == "beverages")
    other = next(r for r in ROWS if r["category"] != "beverages")
    assert result.loc[beverage["id"], "unit_price"] == pytest.approx(beverage["price"] * 0.9)
    assert result.loc[beverage["id"], "total"] == pytest.approx(beverage["total"] * 0.9)
    assert result.loc[other["id"], "total"] == other["total"]
