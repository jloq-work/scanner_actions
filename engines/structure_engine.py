# engines/structure_engine.py

################################
# OBLIQUE (prioritaire)
# RANGE
# sinon → None
################################

from typing import Optional, Dict
import pandas as pd

from structures.oblique import detect_bearish_oblique
from structures.range import detect_range


def analyze_structure(df_weekly: pd.DataFrame) -> Optional[Dict]:
    """
    Analyse la structure technique dominante sur données weekly.

    Priorité :
    1. Résistance oblique baissière
    2. Range horizontal

    Retourne None si aucune structure valide n'est détectée.
    """

    if df_weekly is None or len(df_weekly) < 10:
        return None

    last_close = df_weekly["Close"].iloc[-1]

    # ==================================================
    # 1. OBLIQUE
    # ==================================================
    oblique = detect_bearish_oblique(df_weekly)

    if oblique:
        resistance = oblique["resistance_price"]

        return {
            "structure_type": "OBLIQUE",
            "resistance_price": resistance,
            "support_price": None,
            "is_breakout": last_close > resistance,
            "details": {
                "slope": oblique["slope"],
                "points": oblique["points"],
            },
        }

    # ==================================================
    # 2. RANGE
    # ==================================================
    range_struct = detect_range(df_weekly)

    if range_struct:
        resistance = range_struct["resistance_price"]
        support = range_struct["support_price"]

        return {
            "structure_type": "RANGE",
            "resistance_price": resistance,
            "support_price": support,
            "is_breakout": last_close > resistance,
            "details": {
                "width_pct": range_struct["width_pct"],
                "touches_resistance": range_struct["touches_resistance"],
                "touches_support": range_struct["touches_support"],
            },
        }

    return None
