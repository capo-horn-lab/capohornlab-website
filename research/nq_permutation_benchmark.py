"""Deterministic permutation benchmark for the NQ 30-minute directional screen.

This is a falsification/control study, not a trading strategy or recommendation.
It tests whether the observed first-30-minute sign -> final-30-minute return
is distinguishable from shuffled entry directions, separately in 2023 IS and
2024 OOS.  No 2024 values are used to fit a rule.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SOURCE = Path(__file__).resolve().parent / "studies" / "nq_rth_2023_2024" / "daily_observations.csv"
OUT = Path(__file__).resolve().parent / "studies" / "nq_rth_permutation_2023_2024"
SEED = 20260818
N_PERMUTATIONS = 10_000


def permutation_metrics(frame: pd.DataFrame, rng: np.random.Generator) -> tuple[float, np.ndarray, float, float]:
    """Return observed mean bps/day, null draws, two-sided p value, and z score.

    Null: retain final-30-minute returns and the empirical count of long/short/flat
    first-30-minute signs, but randomly reassign signs to days without replacement.
    """
    signals = np.sign(frame["first30_return"].to_numpy(dtype=float))
    final_returns = frame["last30_return"].to_numpy(dtype=float)
    observed_bps = float(np.mean(signals * final_returns) * 1e4)
    null_bps = np.empty(N_PERMUTATIONS, dtype=float)
    for i in range(N_PERMUTATIONS):
        null_bps[i] = np.mean(rng.permutation(signals) * final_returns) * 1e4
    # Add one to numerator/denominator to avoid a zero Monte-Carlo p-value.
    two_sided_p = float((1 + np.count_nonzero(np.abs(null_bps) >= abs(observed_bps))) / (N_PERMUTATIONS + 1))
    null_std = float(null_bps.std(ddof=1))
    z_score = float((observed_bps - null_bps.mean()) / null_std) if null_std else float("nan")
    return observed_bps, null_bps, two_sided_p, z_score


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Run nq_session_study.py first; source missing: {SOURCE}")
    OUT.mkdir(parents=True, exist_ok=True)
    daily = pd.read_csv(SOURCE, parse_dates=["date"])
    required = {"date", "first30_return", "last30_return", "sample"}
    missing = required.difference(daily.columns)
    if missing:
        raise ValueError(f"source is missing columns: {sorted(missing)}")

    # The sample labels were frozen in the source study: 2023 IS and 2024 OOS.
    rng = np.random.default_rng(SEED)
    output: list[dict[str, float | int | str]] = []
    null_draws: dict[str, np.ndarray] = {}
    for sample in ("IS_2023", "OOS_2024"):
        frame = daily.loc[daily["sample"] == sample].copy()
        if frame.empty:
            raise ValueError(f"no rows for {sample}")
        observed_bps, draws, p_value, z_score = permutation_metrics(frame, rng)
        null_draws[sample] = draws
        output.append(
            {
                "sample": sample,
                "days": int(len(frame)),
                "observed_mean_bps_per_day": observed_bps,
                "null_mean_bps_per_day": float(draws.mean()),
                "null_std_bps_per_day": float(draws.std(ddof=1)),
                "null_p05_bps_per_day": float(np.quantile(draws, 0.05)),
                "null_p95_bps_per_day": float(np.quantile(draws, 0.95)),
                "two_sided_permutation_p_value": p_value,
                "z_score_vs_null": z_score,
                "permutations": N_PERMUTATIONS,
                "seed": SEED,
            }
        )

    results = pd.DataFrame(output)
    results.to_csv(OUT / "permutation_summary.csv", index=False)
    (OUT / "summary.json").write_text(
        json.dumps(
            {
                "study": "NQ first-30-minute sign to final-30-minute return permutation benchmark",
                "source": str(SOURCE),
                "formula": "observed = mean(sign(first30_return_d) * last30_return_d) * 10,000; null permutes sign(first30_return) across days within each sample",
                "split": "IS_2023 / OOS_2024 fixed by source study; no 2024 fitting",
                "seed": SEED,
                "permutations": N_PERMUTATIONS,
                "results": output,
                "limitations": [
                    "One-minute OHLCV only; no order-book imbalance, bid/ask, fill, latency, roll, commission or slippage model.",
                    "The permutation test measures directional association against a shuffled-sign control; it does not validate an executable strategy.",
                    "The sample is limited to 2023-2024 and complete RTH days already selected by the source screen.",
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
    for ax, sample in zip(axes, ("IS_2023", "OOS_2024")):
        row = results.loc[results["sample"] == sample].iloc[0]
        draws = null_draws[sample]
        ax.hist(draws, bins=45, color="#8b5cf6", alpha=0.78, label="shuffled-sign null")
        ax.axvline(row.observed_mean_bps_per_day, color="#dc2626", linewidth=2, label=f"observed {row.observed_mean_bps_per_day:.2f} bps")
        ax.axvline(0, color="#334155", linewidth=0.9)
        ax.set_title(f"{sample}: observed vs 10,000 shuffled signs")
        ax.set_xlabel("mean gross bps/day")
        ax.set_ylabel("permutation count")
        ax.legend(fontsize=8)
    fig.savefig(OUT / "nq_directional_permutation_null.png", dpi=180)
    plt.close(fig)

    report_rows = "\n".join(
        f"| {r['sample']} | {r['days']} | {r['observed_mean_bps_per_day']:.3f} | {r['null_mean_bps_per_day']:.3f} | {r['null_p05_bps_per_day']:.3f} to {r['null_p95_bps_per_day']:.3f} | {r['two_sided_permutation_p_value']:.4f} | {r['z_score_vs_null']:.3f} |"
        for r in output
    )
    report = f"""# NQ directional screen — permutation benchmark (2023 IS / 2024 OOS)

## Objective

Falsify the previously negative descriptive screen: does its daily directional result differ from a control that randomly reassigns the observed first-30-minute long/short signs across the same days? This is a research control, **not** a trade rule or performance claim.

## Data and split

- Input: `{SOURCE.as_posix()}` produced from owned NQ one-minute OHLCV.
- RTH convention: weekdays, 09:30–15:59 America/New_York; complete days only.
- Fixed split: 2023 IS and 2024 OOS. The control fits no signal and uses no OOS parameter selection.

## Formula and null

For day $d$, observed gross return in basis points is:

`mean(sign(first30_return_d) × last30_return_d) × 10,000`.

For each sample separately, the null preserves all final-30-minute returns and the exact empirical distribution of first-30-minute signs, then randomly permutes those signs across days without replacement. We use {N_PERMUTATIONS:,} deterministic permutations (NumPy PCG64 seed `{SEED}`). The two-sided Monte-Carlo p-value is `(1 + count(|null| >= |observed|)) / ({N_PERMUTATIONS} + 1)`.

## Results

| Sample | Days | Observed gross mean bps/day | Null mean | 5th–95th null interval | Two-sided p | Z vs null |
|---|---:|---:|---:|---:|---:|---:|
{report_rows}

The screen remains unsuitable for promotion: its observed means are negative, and this test is only a directional-association control rather than an executable cost-aware backtest.

## Costs and limitations

- Gross descriptive returns only: no spread, bid/ask execution, commissions, slippage, market impact, latency, roll handling, or partial fills.
- One-minute OHLCV cannot establish order-flow or order-book imbalance.
- The shuffled-sign null does not cure multiple-hypothesis risk or prove causal predictability.
- Two years of NQ data are too short for robustness claims across contract rolls and market regimes.

## Artifacts

- `permutation_summary.csv`
- `summary.json`
- `nq_directional_permutation_null.png`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(results.to_json(orient="records", indent=2))
    print(f"artifacts={OUT}")


if __name__ == "__main__":
    main()
