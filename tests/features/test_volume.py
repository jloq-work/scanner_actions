import pandas as pd
import pytest

from src.features.volumes import (
    add_volume_means,
    add_volume_ratio,
)

###########################################################
# Moyennes correctement calculées
# Ratios exacts
# Gestion correcte des NaN
# Validation des paramètres
# Aucune mutation des entrées
###########################################################



@pytest.fixture
def volume_df():
    """
    Deterministic volume series:
    volume increases by +10 each day.
    """
    return pd.DataFrame(
        {
            "volume": [100, 110, 120, 130, 140, 150],
        }
    )


# ============================================================
# add_volume_means
# ============================================================

def test_add_volume_means_creates_columns(volume_df):
    df = add_volume_means(volume_df, windows=[2, 3])

    assert "vol_mean_2" in df.columns
    assert "vol_mean_3" in df.columns


def test_add_volume_means_values(volume_df):
    df = add_volume_means(volume_df, windows=[2])

    # rolling mean of window=2
    expected = [None, 105, 115, 125, 135, 145]
    result = df["vol_mean_2"].tolist()

    for r, e in zip(result, expected):
        if e is None:
            assert pd.isna(r)
        else:
            assert pytest.approx(r) == e


def test_add_volume_means_does_not_modify_input(volume_df):
    original_columns = volume_df.columns.tolist()

    _ = add_volume_means(volume_df, windows=[2])

    assert volume_df.columns.tolist() == original_columns


def test_add_volume_means_missing_column_raises():
    df = pd.DataFrame({"vol": [1, 2, 3]})

    with pytest.raises(ValueError):
        add_volume_means(df, windows=[2])


# ============================================================
# add_volume_ratio
# ============================================================

def test_add_volume_ratio_creates_column(volume_df):
    df = add_volume_ratio(volume_df, short_window=2, long_window=4)

    assert "vol_ratio_2_4" in df.columns


def test_add_volume_ratio_values(volume_df):
    df = add_volume_ratio(volume_df, short_window=2, long_window=4)

    # At index 4:
    # short mean = (130 + 140) / 2 = 135
    # long mean  = (110 + 120 + 130 + 140) / 4 = 125
    expected_ratio = 135 / 125

    assert pytest.approx(df.loc[4, "vol_ratio_2_4"], rel=1e-6) == expected_ratio


def test_add_volume_ratio_short_window_must_be_smaller():
    df = pd.DataFrame({"volume": [100, 110, 120]})

    with pytest.raises(ValueError):
        add_volume_ratio(df, short_window=3, long_window=3)


def test_add_volume_ratio_missing_column_raises():
    df = pd.DataFrame({"vol": [1, 2, 3]})

    with pytest.raises(ValueError):
        add_volume_ratio(df, short_window=2, long_window=4)
        
        
def test_add_volume_ratio_handles_string_volume():
    df = pd.DataFrame(
        {
            "volume": ["1000", "2000", "3000", "4000", "5000", "6000"]
        }
    )

    df = add_volume_ratio(df, short_window=2, long_window=3)

    assert df["vol_ratio_2_3"].dtype.kind in ("f", "i")

