# data/loaders.py
##################################
# Charger un CSV OHLCV

# Vérifier le format minimal

# Retourner un pd.DataFrame propre
###################################
from pathlib import Path
import pandas as pd


# Racine du projet
BASE_DIR = Path(__file__).resolve().parents[1]

# Dossier contenant les CSV de démonstration
DATA_DIR = BASE_DIR / "tests" / "data"


REQUIRED_COLUMNS = {"Open", "High", "Low", "Close", "Volume"}


def load_csv(symbol: str) -> pd.DataFrame:
    """
    Charge un fichier CSV OHLCV de démonstration.

    Paramètres
    ----------
    symbol : str
        Nom du symbole (ex: 'MERY.PA')

    Retour
    ------
    pd.DataFrame
        DataFrame indexé par Date, colonnes OHLCV

    Lève
    ----
    FileNotFoundError
        Si le fichier CSV n'existe pas
    ValueError
        Si le format du fichier est invalide
    """
    file_path = DATA_DIR / f"{symbol}.csv"

    if not file_path.exists():
        raise FileNotFoundError(f"CSV not found for symbol: {symbol}")

    df = pd.read_csv(
        file_path,
        parse_dates=["Date"],
        index_col="Date",
    )

    df.sort_index(inplace=True)

    # Validation minimale du format
    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise ValueError(
            f"Invalid CSV format for {symbol}. "
            f"Required columns: {REQUIRED_COLUMNS}"
        )

    if len(df) < 20:
        raise ValueError(
            f"Not enough data for {symbol} "
            f"({len(df)} rows, minimum 20 required)"
        )

    return df
