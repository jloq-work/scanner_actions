# scans/scan_breakouts.py

##########################################################
# PRE_BREAKOUT	Pas encore cassé la résistance
# BREAKOUT_FAIBLE	Cassure technique mais volumes faibles
# BREAKOUT_FRANC	Cassure + volumes forts
##########################################################

from typing import List, Dict

from engines.structure_engine import analyze_structure
from patterns.volumes import analyze_volume


def scan_breakouts(
    symbols: List[str],
    data_provider,
) -> List[Dict]:
    """
    Scan des titres pour détecter :
    - PRE_BREAKOUT
    - BREAKOUT_FAIBLE
    - BREAKOUT_FRANC
    """

    results: List[Dict] = []

    for symbol in symbols:
        try:
            df_daily = data_provider.get_daily(symbol)
            df_weekly = data_provider.get_weekly(symbol)

            if df_daily is None or df_weekly is None:
                continue

            # --------------------------------------------------
            # 1. Structure (weekly)
            # --------------------------------------------------
            structure = analyze_structure(df_weekly)

            if structure is None:
                continue

            # --------------------------------------------------
            # 2. Volume (daily)
            # --------------------------------------------------
            volume_info = analyze_volume(df_daily)

            # --------------------------------------------------
            # 3. Classification
            # --------------------------------------------------
            if not structure["is_breakout"]:
                state = "PRE_BREAKOUT"

            else:
                if volume_info["volume_strength"] == "STRONG":
                    state = "BREAKOUT_FRANC"
                else:
                    state = "BREAKOUT_FAIBLE"

            # --------------------------------------------------
            # 4. Output
            # --------------------------------------------------
            results.append({
                "symbol": symbol,
                "structure": structure["structure_type"],
                "state": state,
                "resistance_price": structure["resistance_price"],
                "support_price": structure["support_price"],
                "volume_strength": volume_info["volume_strength"],
            })

        except Exception as e:
            # volontairement silencieux pour repo public
            print(f"✗ {symbol} failed: {e}")

    return results
