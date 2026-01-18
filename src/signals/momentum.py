import pandas as pd

##############################################################
# Détecter une reprise courte
# Basée uniquement sur le momentum récent
# Ne dépendre ni de la tendance long terme ni des volumes
##############################################################


# ============================================================
# MOMENTUM SIGNALS
# ============================================================

def detect_short_term_momentum(
    df: pd.DataFrame,
    ret_col: str = "ret_5",
    threshold: float = 0,
) -> pd.DataFrame:
    """
    Detect short-term positive momentum.

    Momentum rule:
    - ret_5 > threshold

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with return column
    ret_col : str
        Short-term return column (default: ret_5)
    threshold : float
        Minimum return threshold

    Returns
    -------
    pd.DataFrame
        DataFrame with a boolean 'momentum' column
    """

    if ret_col not in df.columns:
        raise ValueError(f"Column '{ret_col}' not found in DataFrame")

    df_out = df.copy()

    df_out["momentum"] = df_out[ret_col] > threshold

    return df_out
