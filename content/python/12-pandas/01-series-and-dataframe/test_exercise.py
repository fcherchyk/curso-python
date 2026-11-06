import csv
from collections import Counter

import pandas as pd
import pytest
from exercise import from_records, load_sales, price_series, summary

with open("sales.csv", newline="", encoding="utf-8") as f:
    ROWS = list(csv.DictReader(f))  # reference computed without pandas


def test_price_series():
    s = price_series({"tea": 1200, "coffee": 9800, "sugar": 900})
    assert isinstance(s, pd.Series)
    assert s.name == "price"
    assert list(s.index) == ["coffee", "sugar", "tea"]
    assert s["coffee"] == 9800


def test_from_records():
    df = from_records([{"stock": 3, "product": "cocoa", "price": 3500}])
    assert list(df.columns) == ["product", "price", "stock"]
    assert df.loc[0, "product"] == "cocoa"


def test_load_sales_types():
    df = load_sales("sales.csv")
    assert df.index.name == "id"
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert len(df) == len(ROWS)
    row = ROWS[0]
    assert df.loc[int(row["id"]), "total"] == int(row["quantity"]) * int(row["unit_price"])


def test_summary():
    totals = {int(r["id"]): int(r["quantity"]) * int(r["unit_price"]) for r in ROWS}
    s = summary(load_sales("sales.csv"))
    assert s["rows"] == len(ROWS)
    assert s["total"] == sum(totals.values())
    assert s["average_ticket"] == pytest.approx(round(sum(totals.values()) / len(ROWS), 2))
    assert s["largest_sale"] == max(totals, key=totals.get)
    assert s["most_frequent_branch"] == Counter(r["branch"] for r in ROWS).most_common(1)[0][0]
