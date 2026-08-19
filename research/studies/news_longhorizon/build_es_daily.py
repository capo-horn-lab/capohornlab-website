"""Build the daily ES close series (2020-2024) from owned 1-minute OHLCV.

Session rule mirrors the verified engine (research/market_data_engine.py,
cme_globex_equity_index): bars are assigned to the CME Globex session starting
17:00 America/Chicago (DST-aware), i.e. a bar at/after 17:00 CT belongs to the
NEXT session date. Daily row = aggregation of the 1-minute bars of one session.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_DIR = Path("D:/marketdata/ES")
OUT = Path(__file__).resolve().parent / "es_daily.csv"
YEARS = range(2020, 2025)


def session_date_of(ts: pd.Series) -> pd.Series:
    local = ts.dt.tz_convert("America/Chicago")
    sday = local.dt.normalize().where(
        local.dt.hour >= 17, local.dt.normalize() - pd.Timedelta(days=1)
    )
    return sday.dt.date


def main() -> None:
    frames = []
    for year in YEARS:
        path = DATA_DIR / f"ES_ohlcv_1m_{year}.parquet"
        if not path.exists():
            print(f"skip missing: {path}")
            continue
        df = pd.read_parquet(path)
        df = df.reset_index()
        if "ts_event" not in df.columns:
            df = df.rename(columns={"index": "ts_event"})
        df["ts_event"] = pd.to_datetime(df["ts_event"], utc=True)
        df["session_date"] = session_date_of(df["ts_event"])
        daily = df.groupby("session_date").agg(
            open=("open", "first"),
            high=("high", "max"),
            low=("low", "min"),
            close=("close", "last"),
            volume=("volume", "sum"),
            bar_count=("close", "count"),
        )
        frames.append(daily.reset_index())
        print(f"{year}: 1m bars {len(df):,} -> daily {len(daily)}")

    all_daily = pd.concat(frames, ignore_index=True)
    all_daily["session_date"] = pd.to_datetime(all_daily["session_date"])
    all_daily = all_daily.sort_values("session_date").drop_duplicates("session_date", keep="last")
    all_daily.to_csv(OUT, index=False)
    print(
        f"saved: {OUT} ({len(all_daily)} daily rows, "
        f"{all_daily['session_date'].min().date()}..{all_daily['session_date'].max().date()})"
    )


if __name__ == "__main__":
    main()
