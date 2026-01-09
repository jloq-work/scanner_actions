# structures/oblique.py
#######################################
#On a au moins 2 sommets descendants

#Ils sont espacés dans le temps

#Une droite peut être tracée entre eux

#Le prix actuel est sous cette oblique
#######################################

from typing import Optional, Dict, List
import pandas as pd
import numpy as np


def _find_swing_highs(
    df: pd.DataFrame,
    window: int = 3,
) -> List[int]:
    """
    Détecte des sommets locaux (swing highs).
    Retourne les index des points.
    """

    highs = df["High"].values
    swing_indices = []

    for i in range(window, len(highs) - window):
        if highs[i] == max(highs[i - window : i + window + 1]):
            swing_indices.append(i)

    return swing_indices


def detect_bearish_oblique(
    df: pd.DataFrame,
    lookback: int = 60,
    tolerance: float = 0.01,
) -> Optional[Dict]:
    """
    Détecte une oblique baissière simple basée sur des swing highs.

    Paramètres
    ----------
    df : pd.DataFrame
        Données OHLCV daily
    lookback : int
        Fenêtre analysée
    tolerance : float
        Tolérance relative par rapport à l'oblique

    Retour
    ------
    dict ou None
        Informations sur l'oblique détectée
    """

    if df is None or len(df) < lookback:
        return None

    window = df.tail(lookback).copy()
    window.reset_index(inplace=True)

    swing_indices = _find_swing_highs(window)

    if len(swing_indices) < 2:
        return None

    # On prend les deux derniers sommets
    i1, i2 = swing_indices[-2], swing_indices[-1]

    y1 = window.loc[i1, "High"]
    y2 = window.loc[i2, "High"]

    # Doit être baissier
    if y2 >= y1:
        return None

    x1, x2 = i1, i2

    # Droite y = ax + b
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    # Résistance actuelle
    last_x = len(window) - 1
    resistance_now = slope * last_x + intercept

    last_close = window.loc[last_x, "Close"]

    # Le prix doit être sous l'oblique
    if last_close > resistance_now * (1 + tolerance):
        return None

    return {
        "type": "OBLIQUE",
        "slope": slope,
        "intercept": intercept,
        "resistance_price": round(resistance_now, 2),
        "points": [
            {
                "date": window.loc[i1, "Date"],
                "price": round(y1, 2),
            },
            {
                "date": window.loc[i2, "Date"],
                "price": round(y2, 2),
            },
        ],
        "lookback": lookback,
    }
