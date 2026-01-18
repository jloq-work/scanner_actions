from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd
import yfinance as yf

#####################
# Télécharger les données daily depuis Yahoo Finance
# Normaliser les colonnes
# Gérer l’historique 3 ans glissants
# Sauvegarder / recharger localement (cache simple)
#####################

# ============================================================
# PATHS
# ============================================================

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CORE LOADER
# ============================================================

def download_daily_data(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    years: int = 3,
) -> pd.DataFrame:
    """
    Download daily OHLCV data from Yahoo Finance.

    Parameters
    ----------
    symbol : str
        Yahoo Finance symbol (e.g. 'AIR.PA')
    start : str, optional
        Start date (YYYY-MM-DD)
    end : str, optional
        End date (YYYY-MM-DD)
    years : int
        Number of years of history if start is None

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        ['date', 'open', 'high', 'low', 'close', 'volume']
    """

    if end is None:
        (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    if start is None:
        start_date = datetime.today() - timedelta(days=365 * years)
        start = start_date.strftime("%Y-%m-%d")

    try:
        df = yf.download(
            symbol,
            start=start,
            end=end,
            interval="1d",
            auto_adjust=False,
            progress=False,
        )
        
    except Exception:
       df = pd.DataFrame()

    # Fallback: retry without explicit end date
    if df.empty:
        df = yf.download(
            symbol,
            start=start,
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

    if df.empty:
        raise ValueError(f"No data returned for symbol {symbol}")

    # Normalize columns
    df = df.reset_index()

    df = df.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    df = df[["date", "open", "high", "low", "close", "volume"]]

    # Ensure proper types
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    return df


# ============================================================
# LOCAL CACHE
# ============================================================

def save_local_data(df: pd.DataFrame, symbol: str) -> None:
    """
    Save raw daily data to CSV.
    """
    path = RAW_DIR / f"{symbol}.csv"
    df.to_csv(path, index=False)


def load_local_data(symbol: str) -> Optional[pd.DataFrame]:
    """
    Load raw daily data from local CSV if exists.
    """
    path = RAW_DIR / f"{symbol}.csv"
    if not path.exists():
        return None

    df = pd.read_csv(path, parse_dates=["date"])
    return df


# ============================================================
# API
# ============================================================

def get_daily_data(
    symbol: str,
    force_download: bool = False,
    years: int = 2,
) -> pd.DataFrame:
    """
    Load daily data from local cache or download it.

    Parameters
    ----------
    symbol : str
        Yahoo Finance symbol
    force_download : bool
        If True, always download data
    years : int
        Number of years of history

    Returns
    -------
    pd.DataFrame
    """

    if not force_download:
        df_local = load_local_data(symbol)
        if df_local is not None:
            return df_local

    df = download_daily_data(symbol=symbol, years=years)
    save_local_data(df, symbol)

    return df
