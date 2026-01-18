import pandas as pd
from typing import Iterable

###################################
#Calculer des glissements de prix
#Être déterministe, testable, lisible
#Fonctionne sur daily ou weekly
###################################


# ============================================================
# RETURNS / PRICE CHANGES
# ============================================================

def add_returns(
    df: pd.DataFrame,
    windows: Iterable[int],
    price_col: str = "close",
    prefix: str = "ret",
) -> pd.DataFrame:
    """
    Add rolling returns to a price DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a price column
    windows : Iterable[int]
        Number of periods for returns (e.g. [5, 21, 63])
    price_col : str
        Column used for return computation
    prefix : str
        Prefix for return columns

    Returns
    -------
    pd.DataFrame
        DataFrame with additional return columns
    """

    if price_col not in df.columns:
        raise ValueError(f"Column '{price_col}' not found in DataFrame")

    df_out = df.copy()
    
    # Force numeric close price (Yahoo safety)
    df_out[price_col] = pd.to_numeric(df_out[price_col], errors="coerce")

    for window in windows:
        col_name = f"{prefix}_{window}"
        df_out[col_name] = df_out[price_col].pct_change(periods=window)

    return df_out
