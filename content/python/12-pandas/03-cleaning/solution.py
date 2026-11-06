import pandas as pd


def normalize_names(s: pd.Series) -> pd.Series:
    return s.str.strip().str.replace(r"\s+", " ", regex=True).str.title()


def parse_amounts(s: pd.Series) -> pd.Series:
    cleaned = (
        s.str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce").astype(float)


def nulls_per_column(df: pd.DataFrame) -> dict[str, int]:
    nulls = df.isna().sum()
    return {col: int(n) for col, n in nulls[nulls > 0].items()}


def clean_customers(raw: pd.DataFrame) -> pd.DataFrame:
    return (
        raw.assign(email=lambda d: d["email"].str.strip().str.lower())
        .dropna(subset=["email"])
        .assign(
            name=lambda d: normalize_names(d["name"]),
            age=lambda d: pd.to_numeric(d["age"], errors="coerce").astype("Int64"),
            balance=lambda d: parse_amounts(d["balance"]),
            city=lambda d: d["city"].str.strip().str.title().fillna("Unknown"),
        )
        .drop_duplicates(subset=["email"], keep="first")
        .reset_index(drop=True)
    )
