"""Reproducible exploratory NQ RTH session study (not a trading strategy)."""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(r"D:/marketdata/NQ/1m")
OUT = Path(__file__).resolve().parent / "studies" / "nq_rth_2023_2024"
OUT.mkdir(parents=True, exist_ok=True)


def load_year(year: int) -> pd.DataFrame:
    p = ROOT / f"NQ_ohlcv_1m_{year}.parquet"
    df = pd.read_parquet(p)
    if "ts_event" not in df.columns:
        raise ValueError(f"{p} has no ts_event column")
    df["ts_event"] = pd.to_datetime(df["ts_event"], utc=True)
    return df.set_index("ts_event").sort_index()[["open", "high", "low", "close", "volume"]]


def at_or_before(day: pd.DataFrame, time: str) -> pd.Series | None:
    x = day.between_time("09:30", time)
    return None if x.empty else x.iloc[-1]


def main() -> None:
    raw = pd.concat([load_year(2023), load_year(2024)]).sort_index()
    ny = raw.tz_convert("America/New_York")
    ny = ny[(ny.index.dayofweek < 5) & (ny.index.time >= pd.Timestamp("09:30").time()) & (ny.index.time <= pd.Timestamp("15:59").time())]

    rows = []
    for date, day in ny.groupby(ny.index.date):
        op = at_or_before(day, "09:30")
        first = at_or_before(day, "09:59")
        last_open = day.between_time("15:30", "15:30")
        close = at_or_before(day, "15:59")
        if op is None or first is None or close is None or last_open.empty:
            continue
        lo = last_open.iloc[0]
        first_ret = first.close / op.open - 1
        last_ret = close.close / lo.open - 1
        rth_ret = close.close / op.open - 1
        first_range_bps = (day.between_time("09:30", "09:59").high.max() - day.between_time("09:30", "09:59").low.min()) / op.open * 1e4
        rows.append({"date": str(date), "first30_return": first_ret, "last30_return": last_ret, "rth_return": rth_ret, "first30_range_bps": first_range_bps})
    daily = pd.DataFrame(rows).set_index("date")
    daily["session_year"] = pd.to_datetime(daily.index).year
    daily["sample"] = np.where(daily.session_year == 2023, "IS_2023", "OOS_2024")
    daily["signal"] = np.sign(daily.first30_return)
    daily["gross_signal_return"] = daily.signal * daily.last30_return

    # Freeze condition thresholds on 2023 only, then apply unchanged to 2024.
    # This prevents OOS labels from using any 2024 distributional information.
    is_ranges = daily.loc[daily.session_year == 2023, "first30_range_bps"]
    low_cut, high_cut = is_ranges.quantile([1 / 3, 2 / 3]).tolist()
    daily["range_tercile"] = pd.cut(daily["first30_range_bps"], bins=[-np.inf, low_cut, high_cut, np.inf], labels=["low", "mid", "high"], include_lowest=True)

    bins = ny.copy()
    # Reset returns at each RTH session: never leak the overnight gap into 09:30.
    bins["ret_bps"] = bins.groupby(bins.index.date)["close"].pct_change() * 1e4
    bins["bin"] = bins.index.map(lambda x: x.replace(minute=(x.minute // 30) * 30, second=0, microsecond=0).strftime("%H:%M"))
    profile = bins.groupby("bin").agg(mean_return_bps=("ret_bps", "mean"), mean_abs_return_bps=("ret_bps", lambda x: x.abs().mean()), mean_volume=("volume", "mean"), observations=("ret_bps", "count")).reset_index()

    def metrics(frame: pd.DataFrame) -> dict:
        return {
            "days": int(len(frame)), "gross_mean_bps": float(frame.gross_signal_return.mean() * 1e4),
            "gross_median_bps": float(frame.gross_signal_return.median() * 1e4),
            "positive_rate": float((frame.gross_signal_return > 0).mean()),
            "gross_total_bps": float(frame.gross_signal_return.sum() * 1e4),
            "correlation_first_last": float(frame.first30_return.corr(frame.last30_return)),
        }

    conditions = daily.groupby(["sample", "range_tercile"], observed=True).agg(
        days=("gross_signal_return", "size"), gross_mean_bps=("gross_signal_return", lambda x: x.mean() * 1e4),
        gross_median_bps=("gross_signal_return", lambda x: x.median() * 1e4), positive_rate=("gross_signal_return", lambda x: (x > 0).mean()),
        gross_total_bps=("gross_signal_return", lambda x: x.sum() * 1e4),
    ).reset_index()
    overall = {
        "days": int(len(daily)),
        "gross_mean_bps": float(daily.gross_signal_return.mean() * 1e4),
        "gross_median_bps": float(daily.gross_signal_return.median() * 1e4),
        "positive_rate": float((daily.gross_signal_return > 0).mean()),
        "gross_total_bps": float(daily.gross_signal_return.sum() * 1e4),
        "correlation_first_last": float(daily.first30_return.corr(daily.last30_return)),
        "note": "Gross exploratory returns only: no spread, commission, slippage, roll or latency model has been applied.",
        "pre_registered_split": {
            "IS_2023": metrics(daily.loc[daily.session_year == 2023]),
            "OOS_2024": metrics(daily.loc[daily.session_year == 2024]),
            "range_thresholds_bps_fitted_on_IS_2023": {"low_cut": float(low_cut), "high_cut": float(high_cut)},
        },
    }

    daily.to_csv(OUT / "daily_observations.csv")
    conditions.to_csv(OUT / "conditions.csv", index=False)
    profile.to_csv(OUT / "session_profile.csv", index=False)
    (OUT / "summary.json").write_text(json.dumps({"overall": overall, "conditions": conditions.to_dict(orient="records")}, indent=2), encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 1, figsize=(13, 9), constrained_layout=True)
    cumulative = daily.gross_signal_return.cumsum() * 1e4
    axes[0].plot(pd.to_datetime(daily.index), cumulative, color="#2463eb", linewidth=1.4, label="gross cumulative bps")
    axes[0].axhline(0, color="#333", linewidth=.8)
    axes[0].set(title="NQ: first 30 min direction → last 30 min, exploratory gross result", ylabel="cumulative basis points")
    axes[0].legend()
    axes[1].bar(profile.bin, profile.mean_abs_return_bps, color="#8b5cf6", label="mean absolute 1m return (bps)")
    axes[1].set(title="NQ RTH intraday activity profile", ylabel="mean absolute 1m return (bps)", xlabel="New York time")
    axes[1].tick_params(axis="x", labelrotation=90)
    fig.savefig(OUT / "nq_rth_signal_and_activity.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(conditions.range_tercile.astype(str), conditions.gross_mean_bps, color=["#94a3b8", "#f59e0b", "#10b981"])
    ax.axhline(0, color="#333", linewidth=.8)
    ax.set(title="NQ gross signal return by first-30-min range tercile", xlabel="first-30-min range", ylabel="mean gross bps per day")
    fig.tight_layout()
    fig.savefig(OUT / "nq_condition_range_terciles.png", dpi=180)
    plt.close(fig)

    report = f"""# NQ RTH exploratory session study — 2023–2024\n\n## Scope\n\nThis is a descriptive, reproducible screen of the hypothesis: **the sign of the first 30 RTH minutes predicts the sign of the final 30 RTH minutes**. It is not a trade recommendation and it is not cost-adjusted.\n\n- Source: `D:/marketdata/NQ/1m/NQ_ohlcv_1m_2023.parquet` and `...2024.parquet`\n- Session: weekdays, 09:30–15:59 America/New_York\n- Observations: {overall['days']} complete RTH days\n- Gross mean signal return: {overall['gross_mean_bps']:.3f} bps/day\n- Gross median signal return: {overall['gross_median_bps']:.3f} bps/day\n- Positive-day rate: {overall['positive_rate']:.1%}\n- Correlation, first-30 vs final-30 return: {overall['correlation_first_last']:.4f}\n\n## Frozen IS/OOS screen\n\nThe threshold rule is fixed before OOS inspection: first-30-minute range terciles are fitted on 2023 only and applied unchanged to 2024. No parameter is selected from 2024.\n\n| Sample | Complete days | Gross mean bps/day | Positive-day rate | First-30 / final-30 correlation |\n|---|---:|---:|---:|---:|\n| IS (2023) | {overall['pre_registered_split']['IS_2023']['days']} | {overall['pre_registered_split']['IS_2023']['gross_mean_bps']:.3f} | {overall['pre_registered_split']['IS_2023']['positive_rate']:.1%} | {overall['pre_registered_split']['IS_2023']['correlation_first_last']:.4f} |\n| OOS (2024) | {overall['pre_registered_split']['OOS_2024']['days']} | {overall['pre_registered_split']['OOS_2024']['gross_mean_bps']:.3f} | {overall['pre_registered_split']['OOS_2024']['positive_rate']:.1%} | {overall['pre_registered_split']['OOS_2024']['correlation_first_last']:.4f} |\n\nFrozen 2023 range cuts: low ≤ {overall['pre_registered_split']['range_thresholds_bps_fitted_on_IS_2023']['low_cut']:.2f} bps; mid between the cuts; high > {overall['pre_registered_split']['range_thresholds_bps_fitted_on_IS_2023']['high_cut']:.2f} bps.\n\n## Interpretation boundary\n\nA positive gross result is only a hypothesis filter. It fails promotion unless it survives a pre-registered 2023/2024 split, realistic bid/ask execution, commissions, slippage, minimum holding/exposure controls, and a no-look-ahead review. The output specifically exposes hours of activity and conditional range buckets so that a future strategy has testable **when-not-to-trade** filters as well as entries.\n\n## Artifacts\n\n- `daily_observations.csv` — one row per complete RTH day\n- `conditions.csv` — performance by first-30-minute range tercile\n- `session_profile.csv` — minute-by-minute activity/volume profile\n- `nq_rth_signal_and_activity.png` — cumulative line and RTH activity profile\n- `nq_condition_range_terciles.png` — condition chart\n"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(overall, indent=2))
    print(f"artifacts={OUT}")


if __name__ == "__main__":
    main()
