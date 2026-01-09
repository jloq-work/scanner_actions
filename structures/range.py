# structures/range.py
##################################################
# Le prix oscille entre :

# une résistance ≈ max des hauts

# un support ≈ min des bas

# Le range est respecté sur une fenêtre récente

# Le prix n’est pas déjà en sortie nette
##################################################

from typing import Optional, Dict
import pandas as pd


def detect_range(
    df: pd.DataFrame,
    lookback: int = 40,
    tolerance: float = 0.01,
    min_touches: int = 2,
) -> Optional[Dict]:
    """
    Détecte un range horizontal simple.

    Paramètres
    ----------
    df : pd.DataFrame
        Données OHLCV daily
    lookback : int
        Nombre de bougies analysées
    tolerance : float
        Tolérance relative (ex: 0.01 = 1 %)
    min_touches : int
        Nombre minimum de touches sur support et résistance

    Retour
    ------
    dict ou None
        Informations sur le range détecté
    """

    if df is None or len(df) < lookback:
        return None

    window = df.tail(lookback)

    resistance = window["High"].max()
    support = window["Low"].min()

    range_height = resistance - support
    if range_height <= 0:
        return None

    # Zones tolérées
    resistance_zone = resistance * (1 - tolerance)
    support_zone = support * (1 + tolerance)

    touches_resistance = (window["High"] >= resistance_zone).sum()
    touches_support = (window["Low"] <= support_zone).sum()

    if touches_resistance < min_touches or touches_support < min_touches:
        return None

    last_close = window["Close"].iloc[-1]

    # Le prix doit être à l'intérieur du range
    if not (support < last_close < resistance):
        return None

    return {
        "type": "RANGE",
        "support_price": round(support, 2),
        "resistance_price": round(resistance, 2),
        "touches_support": int(touches_support),
        "touches_resistance": int(touches_resistance),
        "lookback": lookback,
    }
