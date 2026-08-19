"""Fixed-calendar regime sensitivity for the preliminary ES post-news r20 study.

This descriptive screen reuses the parent event classification and return convention.
Regimes are predeclared calendar buckets: 2020--2021 and 2022--2024.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

import pandas as pd
from scipy import stats

from post_news_robustness import classify_events
from news_event_study import DAILY, event_study

STUDY_DIR = Path(__file__).resolve().parent
REGIMES = ("2020_2021", "2022_2024")


def regime_label(date: str) -> str:
    """Assign an event date to a fixed, predeclared calendar regime."""
    year = int(str(date)[:4])
    if 2020 <= year <= 2021:
        return "2020_2021"
    if 2022 <= year <= 2024:
        return "2022_2024"
    raise ValueError(f"Date outside study regimes: {date}")


def filter_regime(events: Iterable[dict], regime: str) -> list[dict]:
    if regime not in REGIMES:
        raise ValueError(f"Unknown regime: {regime}")
    return [dict(event) for event in events if regime_label(event["date"]) == regime]


def student_t_stats(values: Iterable[float]) -> dict:
    """Finite-sample descriptive summary, independent of parent normal approximation."""
    xs = [float(x) for x in values if x is not None and math.isfinite(float(x))]
    n = len(xs)
    if not n:
        return {"n": 0}
    mean = sum(xs) / n
    median = float(pd.Series(xs).median())
    std = math.sqrt(sum((x - mean) ** 2 for x in xs) / (n - 1)) if n > 1 else 0.0
    t_stat = mean / (std / math.sqrt(n)) if n > 1 and std > 0 else None
    p_value = float(stats.t.sf(abs(t_stat), df=n - 1) * 2.0) if t_stat is not None else None
    return {
        "n": n,
        "mean_pct": round(mean * 100.0, 4),
        "median_pct": round(median * 100.0, 4),
        "std_pct": round(std * 100.0, 4),
        "t_stat": round(t_stat, 3) if t_stat is not None else None,
        "p_value": round(p_value, 4) if p_value is not None else None,
        "win_rate_pct": round(100.0 * sum(x > 0 for x in xs) / n, 2),
    }


def r20_stats(events: list[dict], family: str) -> dict[str, dict]:
    """Compute r20 values directly, then use finite-sample Student-t summaries."""
    del family  # Family is retained in the caller for transparent result structure.
    dates = DAILY["session_date"].reset_index(drop=True)
    positions = pd.Series(range(len(dates)), index=dates)
    closes = DAILY["close"].reset_index(drop=True)
    grouped: dict[str, list[float]] = {}
    for event in events:
        anchor = pd.Timestamp(event["date"]) - pd.Timedelta(days=1)
        candidates = positions.index[positions.index >= anchor]
        if not len(candidates):
            continue
        index = int(positions[candidates[0]])
        if index + 20 >= len(closes):
            continue
        grouped.setdefault(str(event["group"]), []).append(float(closes[index + 20] / closes[index] - 1.0))
    return {group: student_t_stats(values) for group, values in grouped.items()}


def run() -> dict:
    event_sets = classify_events()
    results: dict[str, dict] = {}
    for regime in REGIMES:
        results[regime] = {}
        for family, events in event_sets.items():
            selected = filter_regime(events, regime)
            results[regime][family] = r20_stats(selected, family)
    return {
        "study": "ES post-release long-horizon fixed-calendar regime sensitivity",
        "status": "preliminary_non_promotable",
        "instrument": "ES (E-mini S&P 500)",
        "period": "2020-01-01..2024-12-30",
        "horizon": "r20: close-to-close forward 20 CME Globex sessions",
        "regimes": {
            "2020_2021": "Events dated 2020-01-01 through 2021-12-31.",
            "2022_2024": "Events dated 2022-01-01 through 2024-12-31.",
        },
        "event_classification": "Realized CPI month-over-month, NFP payroll change, and FOMC target-range action; not consensus surprises.",
        "results": results,
        "limitations": [
            "This is a fixed-calendar descriptive split, not a causal or volatility-regime model.",
            "The ES daily source has no attached source-file provenance manifest or as-of actual/forecast-vintage record.",
            "Twenty-session windows overlap; reported Student-t p-values are not overlap-robust.",
            "No multiplicity correction is applied across the wider exploratory study family.",
            "Daily-close reference returns have no executable fill, cost, slippage, roll, or position-sizing model.",
            "This does not establish a tradeable strategy or a promised edge.",
        ],
    }


def render_report(summary: dict) -> str:
    lines = [
        "# Post-News Fixed-Calendar Regime Split — ES Long-Horizon Event Study", "",
        "**Status:** Preliminary and non-promotable. Descriptive sensitivity only; not a trading rule.", "",
        "## Method", "The predeclared event-date buckets are 2020–2021 and 2022–2024. Event definitions and r20 alignment are unchanged from the parent study.", "",
        "## Results (r20)", "",
        "| Regime | Family/group | N | Mean % | Median % | Std % | t | two-sided p | Win % |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for regime, families in summary["results"].items():
        for family, groups in families.items():
            for group, item in groups.items():
                lines.append(f"| {regime} | {family}/{group} | {item.get('n', 0)} | {item.get('mean_pct', '—')} | {item.get('median_pct', '—')} | {item.get('std_pct', '—')} | {item.get('t_stat', '—')} | {item.get('p_value', '—')} | {item.get('win_rate_pct', '—')} |")
    lines += ["", "## Interpretation", "Differences between the two cells are regime sensitivity, not confirmation. Small cells, overlapping horizons, multiple exploration, and missing source/vintage/execution gates prevent promotion.", "", "## Limits"]
    lines.extend(f"- {limit}" for limit in summary["limitations"])
    lines += ["", "## Reproducibility", "Run `.venv/Scripts/python.exe research/studies/news_longhorizon/post_news_regime_split.py`. Outputs: `post_news_regime_split_results.json` and this report."]
    return "\n".join(lines) + "\n"


def main() -> None:
    summary = run()
    output = STUDY_DIR / "post_news_regime_split_results.json"
    report = STUDY_DIR / "POST_NEWS_REGIME_SPLIT_REPORT.md"
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    report.write_text(render_report(summary), encoding="utf-8")
    for regime, families in summary["results"].items():
        weak = families.get("nfp", {}).get("weak", {})
        hold = families.get("fomc", {}).get("hold", {})
        print(f"{regime}: nfp_weak n={weak.get('n')} mean={weak.get('mean_pct')} p={weak.get('p_value')} | fomc_hold n={hold.get('n')} mean={hold.get('mean_pct')} p={hold.get('p_value')}")
    print(f"SAVED {output.name} {report.name}")


if __name__ == "__main__":
    main()
