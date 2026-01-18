import pandas as pd
import pytest

from src.features.returns import add_returns

###############################################
# Colonnes bien créées
# Valeurs mathématiquement correctes
# Gestion des NaN
# Pas d’effet de bord
# Erreur claire si mauvaise entrée
###############################################


@pytest.fixture
def price_df():
    """
    Simple deterministic price series:
    price increases linearly by +1 each day.
    """
    return pd.DataFrame(
        {
            "close": [10, 11, 12, 13, 14, 15],
        }
    )


def test_add_returns_creates_columns(price_df):
    df = add_returns(price_df, windows=[1, 2])

    assert "ret_1" in df.columns
    assert "ret_2" in df.columns


def test_add_returns_values(price_df):
    df = add_returns(price_df, windows=[1])

    # ret_1 = (price[t] / price[t-1]) - 1
    expected = [None, 0.1, 1 / 11, 1 / 12, 1 / 13, 1 / 14]

    result = df["ret_1"].tolist()

    for r, e in zip(result, expected):
        if e is None:
            assert pd.isna(r)
        else:
            assert pytest.approx(r, rel=1e-6) == e


def test_add_returns_multiple_windows(price_df):
    df = add_returns(price_df, windows=[1, 3])

    # ret_3 at index 3: 13 / 10 - 1 = 0.3
    assert pytest.approx(df.loc[3, "ret_3"], rel=1e-6) == 0.3


def test_add_returns_does_not_modify_input(price_df):
    original_columns = price_df.columns.tolist()

    _ = add_returns(price_df, windows=[1, 2])

    assert price_df.columns.tolist() == original_columns


def test_missing_price_column_raises():
    df = pd.DataFrame({"price": [1, 2, 3]})

    with pytest.raises(ValueError):
        add_returns(df, windows=[1])

def test_add_returns_handles_string_close():
    df = pd.DataFrame(
        {
            "close": ["100", "102", "101", "103", "104"]
        }
    )

    df = add_returns(df, windows=[1])

    assert df["ret_1"].dtype.kind in ("f", "i")

