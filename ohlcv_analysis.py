"""Dependency-free OHLCV summary for CSV-shaped market rows."""
from __future__ import annotations

import math
from statistics import pstdev
from typing import Any, Iterable


def _value(row: dict[str, Any], name: str) -> Any:
    return row.get(name, row.get(name.lower()))


def _sma(values: list[float], period: int, index: int) -> float | None:
    if index + 1 < period:
        return None
    return round(sum(values[index + 1 - period:index + 1]) / period, 10)


def analyze_ohlcv(rows: Iterable[dict[str, Any]], source_name: str = "") -> dict[str, Any]:
    """Return JSON-safe moving averages, 20/50 crosses and log-return risk metrics."""
    data = list(rows)
    if not data:
        raise ValueError("at least one OHLCV row is required")
    closes = [float(_value(row, "Close")) for row in data]
    dates = [str(_value(row, "Date")) for row in data]
    averages = [
        {"date": dates[i], "sma_20": _sma(closes, 20, i), "sma_50": _sma(closes, 50, i), "sma_200": _sma(closes, 200, i)}
        for i in range(len(closes))
    ]
    golden: list[dict[str, Any]] = []
    death: list[dict[str, Any]] = []
    for i in range(1, len(averages)):
        previous, current = averages[i - 1], averages[i]
        if previous["sma_20"] is None or previous["sma_50"] is None or current["sma_20"] is None or current["sma_50"] is None:
            continue
        if previous["sma_20"] <= previous["sma_50"] and current["sma_20"] > current["sma_50"]:
            golden.append({"date": dates[i], "close": closes[i]})
        if previous["sma_20"] >= previous["sma_50"] and current["sma_20"] < current["sma_50"]:
            death.append({"date": dates[i], "close": closes[i]})
    returns = [math.log(closes[i] / closes[i - 1]) if closes[i - 1] > 0 and closes[i] > 0 else 0.0 for i in range(1, len(closes))]
    daily = pstdev(returns) if len(returns) > 1 else 0.0
    return {
        "source": source_name, "row_count": len(data), "date_range": {"start": dates[0], "end": dates[-1]},
        "latest_indicators": {key: averages[-1][key] for key in ("sma_20", "sma_50", "sma_200")},
        "indicators": averages, "crosses": {"golden_crosses": golden, "death_crosses": death},
        "daily_log_returns": returns,
        "volatility": {"daily_log_return_stddev": daily, "annualized_log_return_stddev": daily * math.sqrt(252)},
    }
