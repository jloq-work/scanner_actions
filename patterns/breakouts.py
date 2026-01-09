# patterns/breakouts.py
#####################################################
# PRE_BREAKOUT	le prix est juste sous la résistance
# BREAKOUT_FAIBLE	cassure marginale, clôture hésitante
# BREAKOUT_FRANC	cassure nette, clôture au-dessus
#####################################################

from typing import Literal
import pandas as pd


BreakoutState = Literal[
    "NO_BREAKOUT",
    "PRE_BREAKOUT",
    "BREAKOUT_FAIBLE",
    "BREAKOUT_FRANC",
]


def analyze_weekly_breakout(
    df_weekly: pd.DataFrame,
    resistance_price: float,
    pre_breakout_zone: float = 0.02,
    weak_breakout_zone: float = 0.01,
) -> BreakoutState:
    """
    Analyse la dernière bougie weekly par rapport à une résistance.

    Paramètres
    ----------
    df_weekly : pd.DataFrame
        Données weekly OHLCV
    resistance_price : float
        Niveau de résistance identifié
    pre_breakout_zone : float
        Distance relative sous résistance pour PRE_BREAKOUT
    weak_breakout_zone : float
        Distance relative au-dessus pour BREAKOUT_FAIBLE

    Retour
    ------
    BreakoutState
    """

    if df_weekly is None or df_weekly.empty:
        return "NO_BREAKOUT"

    last = df_weekly.iloc[-1]
    close = last["Close"]
    high = last["High"]

    # Distance relative à la résistance
    distance = (close - resistance_price) / resistance_price

    # --------------------------------------------------
    # PRE-BREAKOUT (juste sous la résistance)
    # --------------------------------------------------
    if -pre_breakout_zone <= distance < 0:
        return "PRE_BREAKOUT"

    # --------------------------------------------------
    # BREAKOUT FAIBLE
    # --------------------------------------------------
    if 0 <= distance <= weak_breakout_zone:
        return "BREAKOUT_FAIBLE"

    # --------------------------------------------------
    # BREAKOUT FRANC
    # --------------------------------------------------
    if distance > weak_breakout_zone and close >= high * 0.95:
        return "BREAKOUT_FRANC"

    return "NO_BREAKOUT"
