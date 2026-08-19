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
    xs = [x for x in xs if x is not None]
    n = len(xs)
    if n < 2:
        return {"n": n}
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / (n - 1)
    se = math.sqrt(var / n) if n > 1 else float("inf")
    t = m / se if se > 0 else 0.0
    p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t) / math.sqrt(2.0))))
    return {"n": n, "mean": round(m * 100, 3), "median": round(sorted(xs)[n // 2] * 100, 3),
            "t": round(t, 2), "p": round(p, 4)}


def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
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
    p = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t) / math.sqrt(2.0))))
    return {"n": n, "r": round(r, 3), "p": round(p, 4)}


def contingency(df, pre_col, post_col):
    """Sign(pre) vs sign(post): win rate of 'pre-sign predicts post-sign'."""
    pairs = df[[pre_col, post_col]].dropna()
    same = int(((pairs[pre_col] > 0) & (pairs[post_col] > 0)).sum() +
               ((pairs[pre_col] < 0) & (pairs[post_col] < 0)).sum())
    total = int(((pairs[pre_col] != 0) & (pairs[post_col] != 0)).sum())
    return {"n": total, "same_sign": same,
            "hit_rate": round(100.0 * same / total, 1) if total else None}


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
        out[name] = groups
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
                   "note": "pre windows measured on CME Globex session labels (event session = first label >= date-1)"}
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("saved:", OUT)


if __name__ == "__main__":
    main()
