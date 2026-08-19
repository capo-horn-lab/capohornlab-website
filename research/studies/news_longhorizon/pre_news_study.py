"""Pre-news predictive study — does ES behavior BEFORE macro releases predict
the release outcome and the post-release direction? 2020-2024.

Extends news_event_study.py with pre-news windows:
  pre1  = close(t-1)/close(t-2) - 1   (day before)
  pre3  = close(t-1)/close(t-4) - 1
  pre5  = close(t-1)/close(t-6) - 1
Questions:
  1. Does pre-news drift differ by release outcome (hot/cool CPI, strong/weak NFP)?
  2. Does pre-news drift predict the post-release direction (r0, r20)?
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from news_event_study import (
    DAILY, fetch_bls_values, build_event_sets, session_positions,
    HORIZONS, STUDY_DIR,
)

OUT = STUDY_DIR / "pre_news_results.json"

POS = session_positions(DAILY)
CLOSES = DAILY["close"].reset_index(drop=True)
N = len(CLOSES)


def event_label(date: str) -> int:
    """Session position for an event date (label = first session >= date-1)."""
    d = pd.Timestamp(date) - pd.Timedelta(days=1)
    idx = POS.index.searchsorted(d, side="left")
    if idx >= N:
        return -1
    return POS.iloc[idx]


def fwd_ret(i: int, k: int):
    if k == 0:
        return CLOSES[i] / CLOSES[i - 1] - 1.0 if i >= 1 else None
    if i + k < N:
        return CLOSES[i + k] / CLOSES[i] - 1.0
    return None


def pre_ret(i: int, k: int):
    """Return over k sessions ending at session i-1 (i.e., before the event session)."""
    if i - k < 0:
        return None
    return CLOSES[i - 1] / CLOSES[i - k - 1] - 1.0 if i - k - 1 >= 0 else None


def build_pre(events, group_key):
    rows = []
    for ev in events:
        i = event_label(ev["date"])
        if i < 0:
            continue
        rows.append({
            "date": ev["date"],
            "group": str(ev[group_key]),
            "pre1": pre_ret(i, 1),
            "pre3": pre_ret(i, 3),
            "pre5": pre_ret(i, 5),
            "r0": fwd_ret(i, 0),
            "r1": fwd_ret(i, 1),
            "r20": fwd_ret(i, 20),
        })
    return pd.DataFrame(rows)


def tstats(xs):
    xs = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
    n = len(xs)
    if n < 2:
        return {"n": n}
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    se = math.sqrt(var / n) if n > 1 else float("inf")
    t = m / se if se > 0 else 0.0
    p = float(stats.t.sf(abs(t), df=n - 1) * 2.0)
    return {"n": n, "mean": round(m * 100, 3), "median": round(float(pd.Series(xs).median()) * 100, 3),
            "t": round(t, 2), "p": round(p, 4)}


def pearson(xs, ys):
    pairs = [(float(x), float(y)) for x, y in zip(xs, ys)
             if x is not None and y is not None and math.isfinite(float(x)) and math.isfinite(float(y))]
    n = len(pairs)
    if n < 3:
        return {"n": n}
    mx = sum(p[0] for p in pairs) / n
    my = sum(p[1] for p in pairs) / n
    cov = sum((p[0] - mx) * (p[1] - my) for p in pairs)
    vx = sum((p[0] - mx) ** 2 for p in pairs)
    vy = sum((p[1] - my) ** 2 for p in pairs)
    if vx == 0 or vy == 0:
        return {"n": n}
    r = cov / math.sqrt(vx * vy)
    t = r * math.sqrt((n - 2) / (1 - r * r)) if abs(r) < 1 else float("inf")
    p = float(stats.t.sf(abs(t), df=n - 2) * 2.0)
    return {"n": n, "r": round(r, 3), "p": round(p, 4)}


def contingency(df, pre_col, post_col):
    """Sign(pre) vs sign(post): win rate of 'pre-sign predicts post-sign'."""
    pairs = df[[pre_col, post_col]].dropna()
    same = int(((pairs[pre_col] > 0) & (pairs[post_col] > 0)).sum() +
               ((pairs[pre_col] < 0) & (pairs[post_col] < 0)).sum())
    total = int(((pairs[pre_col] != 0) & (pairs[post_col] != 0)).sum())
    p = float(stats.binomtest(same, total, p=0.5, alternative="two-sided").pvalue) if total else None
    return {"n": total, "same_sign": same,
            "hit_rate": round(100.0 * same / total, 1) if total else None,
            "p_vs_50": round(p, 4) if p is not None else None}



def holm_adjust(p_values):
    """Holm family-wise adjustment; preserves input order and missing p-values."""
    valid = [(i, float(p)) for i, p in enumerate(p_values)
             if p is not None and math.isfinite(float(p))]
    adjusted = [None] * len(p_values)
    running = 0.0
    m = len(valid)
    for rank, (idx, p) in enumerate(sorted(valid, key=lambda item: item[1])):
        running = max(running, min(1.0, (m - rank) * p))
        adjusted[idx] = round(running, 4)
    return adjusted


def regime_label(date):
    """Predeclared coarse comparison: pandemic/zero-rate vs inflation/hiking era."""
    return "2020_2021" if str(date)[:4] in {"2020", "2021"} else "2022_2024"


def subset_sensitivity(rows, subset):
    """Descriptive pre5/r20 relationship for a fixed regime or COVID exclusion."""
    if subset == "all":
        selected = rows
    elif subset == "ex_covid":
        selected = [row for row in rows if not str(row["date"]).startswith("2020")]
    else:
        selected = [row for row in rows if regime_label(row["date"]) == subset]
    frame = pd.DataFrame(selected)
    if frame.empty:
        return {"n": 0}
    return {"n": int(len(frame)), "pre5": tstats(frame["pre5"].tolist()),
            "r20": tstats(frame["r20"].tolist()),
            "pre5_vs_r20": pearson(frame["pre5"].tolist(), frame["r20"].tolist()),
            "same_sign": contingency(frame, "pre5", "r20")}


def polarity_interaction(df):
    """Welch comparison of r20 after positive vs negative pre5 drift (descriptive)."""
    pos = [float(x) for x in df.loc[df["pre5"] > 0, "r20"].dropna()]
    neg = [float(x) for x in df.loc[df["pre5"] < 0, "r20"].dropna()]
    if len(pos) < 2 or len(neg) < 2:
        return {"n_positive": len(pos), "n_negative": len(neg)}
    res = stats.ttest_ind(pos, neg, equal_var=False, nan_policy="omit")
    return {"n_positive": len(pos), "n_negative": len(neg),
            "r20_positive_pre5_mean_pct": round(100 * sum(pos) / len(pos), 3),
            "r20_negative_pre5_mean_pct": round(100 * sum(neg) / len(neg), 3),
            "difference_pct": round(100 * ((sum(pos) / len(pos)) - (sum(neg) / len(neg))), 3),
            "t": round(float(res.statistic), 2), "p": round(float(res.pvalue), 4)}

def main():
    bls = fetch_bls_values()
    cpi_events, nfp_events = build_event_sets(bls)
    for e in cpi_events:
        e["group"] = "hot" if e["hot"] else "cool" if e["cool"] else "moderate"
    for e in nfp_events:
        e["group"] = "strong" if e["strong"] else "weak" if e["weak"] else "moderate"

    prev = None
    for e in sorted(cpi_events + nfp_events, key=lambda x: x["date"]):
        pass

    out = {"cpi": {}, "nfp": {}}
    for name, events, gk in (("cpi", cpi_events, "group"), ("nfp", nfp_events, "group")):
        df = build_pre(events, gk)
        groups = {}
        for g in sorted(df["group"].unique()):
            sub = df[df["group"] == g]
            groups[g] = {
                "n": int(len(sub)),
                "pre5": tstats(sub["pre5"].tolist()),
                "pre1": tstats(sub["pre1"].tolist()),
                "r0": tstats(sub["r0"].tolist()),
                "r20": tstats(sub["r20"].tolist()),
                "pre5_vs_r0": pearson(sub["pre5"].tolist(), sub["r0"].tolist()),
                "pre5_vs_r20": pearson(sub["pre5"].tolist(), sub["r20"].tolist()),
                "pre5_r0_same_sign": contingency(sub, "pre5", "r0"),
                "pre5_r20_same_sign": contingency(sub, "pre5", "r20"),
            }
        correlations = [groups[g]["pre5_vs_r20"].get("p") for g in sorted(groups)]
        adjusted = holm_adjust(correlations)
        for group_name, adjusted_p in zip(sorted(groups), adjusted):
            groups[group_name]["pre5_vs_r20"]["p_holm_within_release"] = adjusted_p
        robustness_rows = df.to_dict("records")
        out[name] = {"groups": groups, "pre_post_interaction_r20": polarity_interaction(df),
                     "regime_sensitivity": {key: subset_sensitivity(robustness_rows, key)
                                            for key in ("all", "2020_2021", "2022_2024", "ex_covid")}}
        # print
        print(f"===== {name.upper()} — PRE-NEWS DRIFT BY OUTCOME =====")
        for g, d in groups.items():
            print(f"  {g:9s} n={d['n']:3d} | pre5 {d['pre5'].get('mean','-')}% (t={d['pre5'].get('t','-')}, p={d['pre5'].get('p','-')}) "
                  f"| pre1 {d['pre1'].get('mean','-')}% | r0 {d['r0'].get('mean','-')}% | r20 {d['r20'].get('mean','-')}%")
            print(f"            corr pre5→r0 {d['pre5_vs_r0'].get('r','-')} (p={d['pre5_vs_r0'].get('p','-')}) | "
                  f"corr pre5→r20 {d['pre5_vs_r20'].get('r','-')} (p={d['pre5_vs_r20'].get('p','-')}) | "
                  f"stesso segno pre5/r20 {d['pre5_r20_same_sign']}")
        print()

    out["meta"] = {"sessions": N, "period": "2020-01-01..2024-12-30",
        "note": "pre windows measured on CME Globex session labels (event session = first label >= date-1)",
        "robustness": {"pre_post_interaction": "Welch two-sample comparison of r20 after positive versus negative pre5 drift; descriptive, unadjusted.",
        "regimes": "Fixed calendar split: 2020-2021 vs 2022-2024; ex_covid removes 2020 observations only.",
        "multiple_testing": "Holm family-wise adjustment is applied within each release family across pre5-to-r20 group correlations; all other p-values remain descriptive.",
        "implied_volatility": "Not evaluated: the owned ES daily source has no implied-volatility/VIX field, and no external implied-volatility series was introduced.",
        "overlap": "r20 windows overlap; inference is indicative and not overlap-robust."}}
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("saved:", OUT)


if __name__ == "__main__":
    main()
