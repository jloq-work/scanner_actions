import pandas as pd

from src.scanner.run import run_scanner

###############################################################
# la boucle sur les symboles
# la gestion des erreurs
# la concaténation des résultats
# le comportement quand certains symboles passent et d’autres non
################################################################

def test_run_scanner_multiple_symbols(monkeypatch):
    """
    Integration test for run_scanner():
    - multiple symbols
    - some return signals
    - some return nothing
    """

    # --- Mock symbols universe
    def mock_get_srd_symbols():
        return ["AAA.PA", "BBB.PA", "CCC.PA"]

    # --- Mock scan_symbol behavior
    def mock_scan_symbol(symbol):
        if symbol == "BBB.PA":
            return pd.DataFrame(
                [
                    {
                        "symbol": "BBB.PA",
                        "trend": "down",
                        "ret_5": 0.02,
                        "ret_21": -0.05,
                        "ret_63": -0.10,
                        "volume_ratio": 1.4,
                    }
                ]
            )
        return pd.DataFrame()  # no signal

    monkeypatch.setattr(
        "src.scanner.run.get_srd_symbols",
        mock_get_srd_symbols,
    )

    monkeypatch.setattr(
        "src.scanner.run.scan_symbol",
        mock_scan_symbol,
    )

    df = run_scanner()

    # --- Assertions
    assert not df.empty
    assert len(df) == 1
    assert df.loc[0, "symbol"] == "BBB.PA"

def test_run_scanner_no_results(monkeypatch):
    """
    run_scanner should return empty DataFrame if no symbol matches
    """

    def mock_get_srd_symbols():
        return ["AAA.PA", "BBB.PA"]

    def mock_scan_symbol(symbol):
        return pd.DataFrame()

    monkeypatch.setattr(
        "src.scanner.run.get_srd_symbols",
        mock_get_srd_symbols,
    )

    monkeypatch.setattr(
        "src.scanner.run.scan_symbol",
        mock_scan_symbol,
    )

    df = run_scanner()

    assert df.empty

def test_run_scanner_handles_symbol_error(monkeypatch):
    """
    One symbol crashes, scanner continues
    """

    def mock_get_srd_symbols():
        return ["AAA.PA", "BAD.PA", "CCC.PA"]

    def mock_scan_symbol(symbol):
        if symbol == "BAD.PA":
            raise RuntimeError("boom")
        return pd.DataFrame()

    monkeypatch.setattr(
        "src.scanner.run.get_srd_symbols",
        mock_get_srd_symbols,
    )

    monkeypatch.setattr(
        "src.scanner.run.scan_symbol",
        mock_scan_symbol,
    )

    df = run_scanner()

    assert isinstance(df, pd.DataFrame)
