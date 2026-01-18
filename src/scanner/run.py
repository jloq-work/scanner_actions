import pandas as pd

from src.data.symbols import get_srd_symbols
from src.data.loaders import get_daily_data
from src.data.resample import daily_to_weekly

from src.features.returns import add_returns
from src.features.volumes import add_volume_ratio

from src.signals.trend import classify_trend
from src.signals.momentum import detect_short_term_momentum

##############################################################
#Orchestrer tout le pipeline
#Scanner tous les symboles des actions
#Identifier :
#baisse + reprise
#stable + reprise
#Filtrer par accélération des volumes
#Produire une sortie claire
##############################################################


# ============================================================
# SCANNER PARAMETERS (V1)
# ============================================================

RET_WINDOWS = [5, 21, 63]

VOLUME_SHORT = 5
VOLUME_LONG = 20
VOLUME_RATIO_MIN = 1.15


# ============================================================
# SCANNER CORE
# ============================================================

def scan_symbol(symbol: str) -> pd.DataFrame:
    """
    Run the full scan pipeline for one symbol.
    Returns the last row with signals if conditions are met.
    """

    # --- Load data
    df = get_daily_data(symbol)

    if len(df) < max(RET_WINDOWS) + VOLUME_LONG:
        return pd.DataFrame()

    # --- Features
    df = add_returns(df, windows=RET_WINDOWS)
    df = add_volume_ratio(
        df,
        short_window=VOLUME_SHORT,
        long_window=VOLUME_LONG,
    )

    # --- Signals
    df = classify_trend(df)
    df = detect_short_term_momentum(df)

    # --- Keep last available row only
    row = df.iloc[-1]

    
        # --- Required signals must not be NA
    required_fields = [
        "trend",
        "momentum",
        f"vol_ratio_{VOLUME_SHORT}_{VOLUME_LONG}",
    ]

    if row[required_fields].isna().any():
        return pd.DataFrame()

        # --- Filters
    if not row["momentum"]:
        return pd.DataFrame()

    if row["trend"] not in ("down", "stable"):
        return pd.DataFrame()

    if row[f"vol_ratio_{VOLUME_SHORT}_{VOLUME_LONG}"] < VOLUME_RATIO_MIN:
        return pd.DataFrame()


    # --- Output row
    result = {
        "symbol": symbol,
        "trend": row["trend"],
        "ret_5": row["ret_5"],
        "ret_21": row["ret_21"],
        "ret_63": row["ret_63"],
        "volume_ratio": row[f"vol_ratio_{VOLUME_SHORT}_{VOLUME_LONG}"],
    }

    return pd.DataFrame([result])


def run_scanner() -> pd.DataFrame:
    """
    Run scanner on all SRD symbols.
    """

    results = []

    for symbol in get_srd_symbols():
        try:
            df_res = scan_symbol(symbol)
            if not df_res.empty:
                results.append(df_res)
        except Exception as e:
            print(f"[ERROR] {symbol}: {e}")

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":
    df_results = run_scanner()

    if df_results.empty:
        print("No SRD opportunities detected.")
    else:
        df_results = df_results.sort_values(
            by=["trend", "volume_ratio"],
            ascending=[True, False],
        )

        print("\nSRD Scanner Results:\n")
        print(df_results.to_string(index=False))
