import pandas as pd
import pytest

from src.signals.trend import classify_trend

########################################################
# Création de la colonne trend
# Détection correcte des baisses
# Détection correcte des ranges
# Cas non classés (NaN)
# Entrée
# Validation des colonnes requises
########################################################


@pytest.fixture
def trend_df():
    """
    DataFrame covering all trend cases.
    """
    return pd.DataFrame(
        {
            "ret_21": [-0.10, -0.02, 0.01, 0.10],
            "ret_63": [-0.05, -0.02, 0.02, 0.15],
        }
    )


def test_classify_trend_creates_column(trend_df):
    df = classify_trend(trend_df)

    assert "trend" in df.columns


def test_classify_trend_down(trend_df):
    df = classify_trend(trend_df)

    # First row: strong 1m drop
    assert df.loc[0, "trend"] == "down"


def test_classify_trend_stable(trend_df):
    df = classify_trend(trend_df)

    # Second & third rows: inside stability thresholds
    assert df.loc[1, "trend"] == "stable"
    assert df.loc[2, "trend"] == "stable"


def test_classify_trend_other_is_nan(trend_df):
    df = classify_trend(trend_df)

    # Last row: strong uptrend -> not classified
    assert pd.isna(df.loc[3, "trend"])


def test_classify_trend_does_not_modify_input(trend_df):
    original_columns = trend_df.columns.tolist()

    _ = classify_trend(trend_df)

    assert trend_df.columns.tolist() == original_columns


def test_missing_return_columns_raise():
    df = pd.DataFrame({"ret_21": [0.01, 0.02]})

    with pytest.raises(ValueError):
        classify_trend(df)
