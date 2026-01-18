import pandas as pd
import pytest

from src.signals.momentum import detect_short_term_momentum

###############################################################
# Création correcte de la colonne
# Application exacte du seuil
# Paramétrage du seuil fonctionnel
# Pas d’effet de bord
# Erreur claire si colonne manquante
###############################################################


@pytest.fixture
def momentum_df():
    """
    DataFrame with various short-term return cases.
    """
    return pd.DataFrame(
        {
            "ret_5": [-0.03, 0.00, 0.015, 0.021, 0.10],
        }
    )


def test_detect_short_term_momentum_creates_column(momentum_df):
    df = detect_short_term_momentum(momentum_df)

    assert "momentum" in df.columns


def test_detect_short_term_momentum_values(momentum_df):
    df = detect_short_term_momentum(momentum_df)

    expected = [False, False, False, True, True]
    result = df["momentum"].tolist()

    assert result == expected


def test_detect_short_term_momentum_custom_threshold(momentum_df):
    df = detect_short_term_momentum(momentum_df, threshold=0.05)

    expected = [False, False, False, False, True]
    assert df["momentum"].tolist() == expected


def test_detect_short_term_momentum_does_not_modify_input(momentum_df):
    original_columns = momentum_df.columns.tolist()

    _ = detect_short_term_momentum(momentum_df)

    assert momentum_df.columns.tolist() == original_columns


def test_missing_return_column_raises():
    df = pd.DataFrame({"ret": [0.01, 0.02]})

    with pytest.raises(ValueError):
        detect_short_term_momentum(df)
