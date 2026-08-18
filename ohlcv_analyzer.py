"""Small standard-library OHLCV analyser and JSON CLI."""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import pstdev
from typing import Any, Iterable


def _sma(values: list[float], period: int, index: int) -> float | None:
    return None if index + 1 < period else sum(values[index + 1 - period:index + 1]) / period


def analyse_ohlcv(rows: Iterable[dict[str, Any]], source: str = "") -> dict[str, Any]:
    data = list(rows)
    if not data:
        raise ValueError("at least one OHLCV observation is required")
    closes = [float(row["close"]) for row in data]
    dates = [str(row.get("date", "")) for row in data]
    moving = [{"date": dates[i], "sma_20": _sma(closes, 20, i), "sma_50": _sma(closes, 50, i), "sma_200": _sma(closes, 200, i)} for i in range(len(data))]
    returns: list[dict[str, float | None]] = [{"date": dates[0], "log_return": None}]
    for i in range(1, len(closes)):
        returns.append({"date": dates[i], "log_return": math.log(closes[i] / closes[i - 1]) if closes[i] > 0 and closes[i - 1] > 0 else None})
    valid_returns = [item["log_return"] for item in returns if item["log_return"] is not None]
    daily = pstdev(valid_returns) if len(valid_returns) > 1 else 0.0
    crosses=[]
    for i in range(1, len(moving)):
        p,c=moving[i-1],moving[i]
        if None not in (p["sma_50"],p["sma_200"],c["sma_50"],c["sma_200"]):
            if p["sma_50"] <= p["sma_200"] < c["sma_50"]: crosses.append({"date":dates[i],"pattern":"golden_cross"})
            if p["sma_50"] >= p["sma_200"] > c["sma_50"]: crosses.append({"date":dates[i],"pattern":"death_cross"})
    return {"source": source, "observations": len(data), "moving_averages": moving, "latest": moving[-1], "daily_log_returns": returns, "volatility": {"daily": daily, "annualized_252_days": daily * math.sqrt(252)}, "crosses": crosses}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("csv_path"); parser.add_argument("--output",required=True); args=parser.parse_args()
    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows=[{"date":r["Date"],"open":r["Open"],"high":r["High"],"low":r["Low"],"close":r["Close"],"volume":r["Volume"]} for r in csv.DictReader(f)]
    Path(args.output).write_text(json.dumps(analyse_ohlcv(rows, source=args.csv_path), allow_nan=False),encoding="utf-8")

if __name__ == "__main__": main()
