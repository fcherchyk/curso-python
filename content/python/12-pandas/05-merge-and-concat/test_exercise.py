import csv
from collections import defaultdict

import pandas as pd
import pytest
from exercise import enrich, products_not_in_catalog, revenue_by_category, stack

with open("sales.csv", newline="", encoding="utf-8") as f:
    SALES = list(csv.DictReader(f))
with open("products.csv", newline="", encoding="utf-8") as f:
    CATALOG = {p["product"]: p for p in csv.DictReader(f)}


@pytest.fixture
def sales():
    return pd.read_csv("sales.csv")


@pytest.fixture
def products():
    return pd.read_csv("products.csv")


def test_enrich_keeps_all_rows(sales, products):
    result = enrich(sales, products)
    assert len(result) == len(sales)
    assert {"category", "unit_price", "total"} <= set(result.columns)
    in_catalog = next(s for s in SALES if s["product"] in CATALOG)
    row = result[result["id"] == int(in_catalog["id"])].iloc[0]
    expected = int(in_catalog["quantity"]) * int(CATALOG[in_catalog["product"]]["unit_price"])
    assert row["total"] == expected
    assert result.loc[result["product"] == "mug", "category"].isna().all()


def test_enrich_validates_duplicate_keys(sales, products):
    duplicated = pd.concat([products, products.head(1)], ignore_index=True)
    with pytest.raises(pd.errors.MergeError):
        enrich(sales, duplicated)


def test_products_not_in_catalog(sales, products):
    expected = sorted({s["product"] for s in SALES} - set(CATALOG))
    assert products_not_in_catalog(sales, products) == expected == ["mug"]


def test_revenue_by_category(sales, products):
    expected: dict[str, int] = defaultdict(int)
    for s in SALES:
        if s["product"] in CATALOG:
            p = CATALOG[s["product"]]
            expected[p["category"]] += int(s["quantity"]) * int(p["unit_price"])
    result = revenue_by_category(sales, products)
    assert result == pytest.approx(dict(expected))


def test_stack():
    jan = pd.DataFrame({"product": ["a", "b"], "quantity": [1, 2]})
    feb = pd.DataFrame({"product": ["c"], "quantity": [3]})
    result = stack({"jan": jan, "feb": feb})
    assert list(result.columns) == ["batch", "product", "quantity"]
    assert result["batch"].tolist() == ["jan", "jan", "feb"]
    assert result.index.tolist() == [0, 1, 2]
    assert result["quantity"].sum() == 6
