# patterns/volumes.py

######################################
# LOW	pas de confirmation
# NORMAL	activité standard
# HIGH	participation significative
######################################

from typing import Literal
import pandas as pd


VolumeState = Literal[
    "LOW",
    "NORMAL",
    "HIGH",
]


def analyze_volume(
    df_daily: pd.DataFrame,
    lookback: int = 20,
    high_volume_ratio: float = 1.5,
    low_volume_ratio: float = 0.7,
) -> VolumeState:
    """
    Analyse le volume récent par rapport à sa moyenne.

    Paramètres
    ----------
    df_daily : pd.DataFrame
        Données daily OHLCV
    lookback : int
        Fenêtre de calcul de la moyenne de volume
    high_volume_ratio : float
        Seuil au-dessus duquel le volume est considéré comme élevé
    low_volume_ratio : float
        Seuil en-dessous duquel le volume est considéré comme faible

    Retour
    ------
    VolumeState
    """

    if df_daily is None or len(df_daily) < lookback + 1:
        return "LOW"

    recent = df_daily.iloc[-1]["Volume"]
    avg_volume = df_daily["Volume"].iloc[-lookback - 1:-1].mean()

    if avg_volume == 0 or pd.isna(avg_volume):
        return "LOW"

    ratio = recent / avg_volume

    if ratio >= high_volume_ratio:
        return "HIGH"

    if ratio <= low_volume_ratio:
        return "LOW"

    return "NORMAL"
