import pandas as pd

#########################################
# Convertir des données daily → weekly
# Garantir un OHLC propre
# Agréger les volumes
#| Champ  | Règle        |
#| ------ | ------------ |
#| open   | premier jour |
#| high   | max          |
#| low    | min          |
#| close  | dernier jour |
#| volume | somme        |
#########################################


# ============================================================
# DAILY -> WEEKLY
# ============================================================

def daily_to_weekly(df_daily: pd.DataFrame) -> pd.DataFrame:
    """
    Resample daily OHLCV data to weekly frequency.

    Assumes input DataFrame has columns:
    ['date', 'open', 'high', 'low', 'close', 'volume']

    Week definition:
    - Monday as first trading day
    - Weekly bar ends on Friday

    Returns
    -------
    pd.DataFrame
        Weekly OHLCV DataFrame with same columns
    """

    df = df_daily.copy()

    if "date" not in df.columns:
        raise ValueError("Input DataFrame must contain a 'date' column")

    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()

    weekly = df.resample("W-FRI").agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )

    weekly = weekly.dropna(subset=["open", "high", "low", "close"])
    weekly = weekly.reset_index()

    return weekly
