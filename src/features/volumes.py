import pandas as pd
from typing import Iterable

##############################################################
# Calculer des statistiques de volume
# Fournir des ratios court / moyen terme
# Poser les bases du filtre de liquidité sur actions
##############################################################


# ============================================================
# VOLUME FEATURES
# ============================================================

def add_volume_means(
    df: pd.DataFrame,
    windows: Iterable[int],
    volume_col: str = "volume",
    prefix: str = "vol_mean",
) -> pd.DataFrame:
    """
    Add rolling mean volumes to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a volume column
    windows : Iterable[int]
        Rolling window sizes (e.g. [5, 20])
    volume_col : str
        Column used for volume computation
    prefix : str
        Prefix for volume mean columns

    Returns
    -------
    pd.DataFrame
        DataFrame with additional volume mean columns
    """

    if volume_col not in df.columns:
        raise ValueError(f"Column '{volume_col}' not found in DataFrame")

    df_out = df.copy()

    for window in windows:
        col_name = f"{prefix}_{window}"
        df_out[col_name] = (
            df_out[volume_col]
            .rolling(window=window)
            .mean()
        )

    return df_out


def add_volume_ratio(
    df: pd.DataFrame,
    short_window: int,
    long_window: int,
    volume_col: str = "volume",
    prefix: str = "vol_ratio",
) -> pd.DataFrame:
    """
    Add a volume ratio (short-term / long-term average).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with a volume column
    short_window : int
        Short rolling window (e.g. 5)
    long_window : int
        Long rolling window (e.g. 20)
    volume_col : str
        Volume column name
    prefix : str
        Prefix for ratio column

    Returns
    -------
    pd.DataFrame
        DataFrame with volume ratio column
    """

    if volume_col not in df.columns:
        raise ValueError(f"Column '{volume_col}' not found in DataFrame")

    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window")

    df_out = df.copy()
    
    # Force numeric volume (Yahoo safety)
    df_out[volume_col] = pd.to_numeric(df_out[volume_col], errors="coerce")

    short_mean = df_out[volume_col].rolling(window=short_window).mean()
    long_mean = df_out[volume_col].rolling(window=long_window).mean()

    col_name = f"{prefix}_{short_window}_{long_window}"
    df_out[col_name] = short_mean / long_mean

    return df_out
