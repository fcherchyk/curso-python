import pandas as pd


def total_by_branch(sales: pd.DataFrame) -> pd.Series:
    return sales.groupby("branch")["total"].sum().sort_values(ascending=False)


def category_summary(sales: pd.DataFrame) -> pd.DataFrame:
    summary = sales.groupby("category").agg(
        units=("quantity", "sum"),
        revenue=("total", "sum"),
        average_ticket=("total", "mean"),
        products=("product", "nunique"),
    )
    return summary.assign(average_ticket=summary["average_ticket"].round(2)).sort_values(
        "revenue", ascending=False
    )


def share_of_branch(sales: pd.DataFrame) -> pd.Series:
    return sales["total"] / sales.groupby("branch")["total"].transform("sum")


def branch_category_table(sales: pd.DataFrame) -> pd.DataFrame:
    return pd.pivot_table(
        sales, values="total", index="branch", columns="category", aggfunc="sum", fill_value=0
    )


def top_product_by_branch(sales: pd.DataFrame) -> dict[str, str]:
    units = sales.groupby(["branch", "product"])["quantity"].sum()
    maxima = units.groupby(level="branch").idxmax()  # (branch, product) tuples
    return {branch: product for branch, product in maxima}
