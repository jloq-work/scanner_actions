import pandas as pd
import pytest
from datetime import datetime, timedelta

from src.scanner.run import scan_symbol

###############################################################
#l’orchestration complète
#l’enchaînement des modules
#la logique métier finale (trend + momentum + volume)

#Données factices déterministes
#On va construire une série daily telle que :
#baisse sur 3 mois
#reprise sur 5 jours
#explosion de volume
#donc DOIT être détectée
################################################################

# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def fake_daily_df():
    """
    Fake daily price & volume data engineered to trigger the scanner.
    """

    n_days = 100
    start_date = datetime.today() - timedelta(days=n_days)

    dates = pd.date_range(start=start_date, periods=n_days, freq="B")

    # Price: downtrend then rebound
    prices = (
        list(pd.Series(range(n_days)) * 0.0 + 100)  # flat base
    )
    prices = prices.copy()

    # Downtrend over first 80 days
    for i in range(80):
        prices[i] = 120 - i * 0.3

    # Rebound last 5 days
    for i in range(95, 100):
        prices[i] = prices[i - 1] * 1.01

    volumes = [1000] * 80 + [3000] * 20

    return pd.DataFrame(
        {
            "date": dates,
            "open": prices,
            "high": prices,
            "low": prices,
            "close": prices,
            "volume": volumes,
        }
    )


# ============================================================
# INTEGRATION TEST
# ============================================================

def test_scan_symbol_detects_opportunity(monkeypatch, fake_daily_df):
    """
    Integration test:
    - real scanner
    - mocked data + signals + volume filter
    """

    def mock_get_daily_data(symbol):
        return fake_daily_df

    def mock_classify_trend(df):
        df = df.copy()
        df["trend"] = "down"
        return df

    def mock_detect_momentum(df):
        df = df.copy()
        df["momentum"] = True
        return df

    def mock_add_volume_ratio(df, short_window, long_window):
        df = df.copy()
        df[f"vol_ratio_{short_window}_{long_window}"] = 2.0
        return df

    monkeypatch.setattr(
        "src.scanner.run.get_daily_data",
        mock_get_daily_data,
    )

    monkeypatch.setattr(
        "src.scanner.run.classify_trend",
        mock_classify_trend,
    )

    monkeypatch.setattr(
        "src.scanner.run.detect_short_term_momentum",
        mock_detect_momentum,
    )

    monkeypatch.setattr(
        "src.scanner.run.add_volume_ratio",
        mock_add_volume_ratio,
    )

    df_result = scan_symbol("FAKE.PA")

    assert not df_result.empty
    assert df_result.loc[0, "symbol"] == "FAKE.PA"
    assert df_result.loc[0, "trend"] == "down"
    assert df_result.loc[0, "volume_ratio"] == 2.0



def test_scan_symbol_no_signal(monkeypatch, fake_daily_df):
    """
    No momentum => no signal
    """

    df_no_momentum = fake_daily_df.copy()
    df_no_momentum["close"] = 100  # flat prices

    def mock_get_daily_data(symbol):
        return df_no_momentum

    monkeypatch.setattr(
        "src.scanner.run.get_daily_data",
        mock_get_daily_data,
    )

    df_result = scan_symbol("FAKE.PA")

    assert df_result.empty
