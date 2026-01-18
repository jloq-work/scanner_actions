import pandas as pd

###############################################################
#Qualifier la tendance
#Distinguer :
#baisse
#stable
#S’appuyer uniquement sur des caractéristiques déjà calculées
#Baisse
#ret_21 < -5% OR ret_63 < -10%
#Stable (1mois: 21j, 3 mois: 63j)
#|ret_21| < 3% AND |ret_63| < 5%
#Tout le reste = neutre / ignoré
#############################################################


# ============================================================
# TREND SIGNALS
# ============================================================

def classify_trend(
    df: pd.DataFrame,
    ret_1m_col: str = "ret_21",
    ret_3m_col: str = "ret_63",
) -> pd.DataFrame:
    """
    Classify trend context based on medium-term returns.

    Trend labels:
    - 'down'   : medium-term downtrend
    - 'stable' : range / consolidation
    - NaN      : other cases

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with return columns
    ret_1m_col : str
        1-month return column (default: ret_21)
    ret_3m_col : str
        3-month return column (default: ret_63)

    Returns
    -------
    pd.DataFrame
        DataFrame with a 'trend' column
    """

    for col in (ret_1m_col, ret_3m_col):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame")

    df_out = df.copy()

    df_out["trend"] = pd.NA

    # Downtrend
    down_mask = (
        (df_out[ret_1m_col] < -0.05)
        | (df_out[ret_3m_col] < -0.10)
    )

    # Stable / range
    stable_mask = (
        (df_out[ret_1m_col].abs() < 0.03)
        & (df_out[ret_3m_col].abs() < 0.05)
    )

    df_out.loc[down_mask, "trend"] = "down"
    df_out.loc[stable_mask, "trend"] = "stable"

    return df_out
