# tests/test_scan_breakouts_visual.py
###########################
#test de démonstration
###########################

import pandas as pd
from pathlib import Path

from scans.scan_breakouts import scan_breakouts


# ============================================================
# Local test data provider (CSV only)
# ============================================================

class TestDataProvider:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def get_daily(self, symbol: str) -> pd.DataFrame | None:
        path = self.data_dir / f"{symbol}.csv"
        if not path.exists():
            return None

        df = pd.read_csv(path, index_col=0, parse_dates=True)
        df.sort_index(inplace=True)
        return df

    def get_weekly(self, symbol: str) -> pd.DataFrame | None:
        df = self.get_daily(symbol)
        if df is None or df.empty:
            return None

        return (
            df.resample("W-FRI")
            .agg({
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            })
            .dropna()
        )


# ============================================================
# Visual test
# ============================================================

def main():
    print("\n🔍 Scan BREAKOUTS — Visual validation (sample data)")
    print("=" * 80)

    symbols = [
        "AIR.PA",
        "MERY.PA",
        "BB.PA",
    ]

    data_dir = Path(__file__).parent / "data"
    provider = TestDataProvider(data_dir)

    results = scan_breakouts(symbols, provider)

    if not results:
        print("❌ Aucun setup détecté")
        return

    for r in results:
        print(f"\n📌 {r['symbol']}")
        print(f"    Structure        : {r['structure']}")
        print(f"    State            : {r['state']}")
        print(f"    Resistance price : {r['resistance_price']:.2f}")

        if r["support_price"] is not None:
            print(f"    Support price    : {r['support_price']:.2f}")

        print(f"    Volume strength  : {r['volume_strength']}")

    print("\n" + "=" * 80)
    print(f"Total setups détectés: {len(results)}")


if __name__ == "__main__":
    main()
