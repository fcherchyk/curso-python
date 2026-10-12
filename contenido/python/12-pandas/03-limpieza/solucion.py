import pandas as pd


def normalizar_nombres(s: pd.Series) -> pd.Series:
    return s.str.strip().str.replace(r"\s+", " ", regex=True).str.title()


def convertir_montos(s: pd.Series) -> pd.Series:
    limpio = (
        s.str.replace("$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )
    return pd.to_numeric(limpio, errors="coerce").astype(float)


def nulos_por_columna(df: pd.DataFrame) -> dict[str, int]:
    nulos = df.isna().sum()
    return {col: int(n) for col, n in nulos[nulos > 0].items()}


def limpiar_clientes(crudo: pd.DataFrame) -> pd.DataFrame:
    return (
        crudo.assign(email=lambda d: d["email"].str.strip().str.lower())
        .dropna(subset=["email"])
        .assign(
            nombre=lambda d: normalizar_nombres(d["nombre"]),
            edad=lambda d: pd.to_numeric(d["edad"], errors="coerce").astype("Int64"),
            saldo=lambda d: convertir_montos(d["saldo"]),
            ciudad=lambda d: d["ciudad"].str.strip().str.title().fillna("Desconocida"),
        )
        .drop_duplicates(subset=["email"], keep="first")
        .reset_index(drop=True)
    )
