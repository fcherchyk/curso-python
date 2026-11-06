import math

import pandas as pd
import pytest
from exercise import clean_customers, normalize_names, nulls_per_column, parse_amounts


@pytest.fixture
def raw():
    return pd.read_csv("customers.csv", dtype=str, keep_default_na=False, na_values=[""])


def test_normalize_names():
    s = pd.Series(["  alice   SMITH ", "bob", None])
    result = normalize_names(s)
    assert result.iloc[0] == "Alice Smith"
    assert result.iloc[1] == "Bob"
    assert pd.isna(result.iloc[2])


def test_parse_amounts():
    result = parse_amounts(pd.Series(["$ 1.234,50", "$ 20.000,75", "$ 0,00", None, "abc"]))
    assert result.iloc[0] == pytest.approx(1234.5)
    assert result.iloc[1] == pytest.approx(20000.75)
    assert result.iloc[2] == 0
    assert math.isnan(result.iloc[3]) and math.isnan(result.iloc[4])


def test_nulls_per_column(raw):
    assert nulls_per_column(raw) == {"name": 1, "email": 1, "balance": 1, "city": 1}


def test_clean_customers(raw):
    before = raw.copy()
    df = clean_customers(raw)
    pd.testing.assert_frame_equal(raw, before)  # does not mutate the input

    assert df["email"].tolist() == [
        "alice@mail.com",
        "bob@mail.com",
        "carol@mail.com",
        "dave@mail.com",
        "x@mail.com",
    ]
    assert df.index.tolist() == [0, 1, 2, 3, 4]
    assert df.loc[0, "name"] == "Alice Smith"
    assert df.loc[1, "name"] == "Bob Jones"
    assert str(df["age"].dtype) == "Int64"
    assert pd.isna(df.loc[2, "age"]) and df.loc[0, "age"] == 31
    assert df.loc[0, "balance"] == pytest.approx(1234.5)
    assert math.isnan(df.loc[2, "balance"])
    assert df["city"].tolist() == ["Boston", "Boston", "Denver", "Unknown", "Austin"]
