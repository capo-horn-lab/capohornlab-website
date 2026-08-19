"""News-trading long-horizon event study — ES daily, 2020-2024.

Events: FOMC decisions (44), CPI releases (60), Employment Situation/NFP (60).
Horizons: event-day (r0), +1, +5, +20 trading sessions. All returns are computed
AFTER the event date (no lookahead). Statistics: N, mean, median, std, t-stat,
two-sided p (normal approx), win rate, vs all-session baseline. Overlapping
long-window events are noted as a limitation, not adjusted.

Sources:
- ES daily: owned ES 1m OHLCV 2020-2024 aggregated on CME Globex session dates.
- FOMC: Wikipedia "History of FOMC actions" table (each row links the official
  Federal Reserve statement) + Jan 2020 supplement from Fed statement.
- CPI/NFP dates: official BLS release calendar ICS (via Wayback snapshots).
- CPI/NFP values: BLS public API v2 (CUSR0000SA0, CES0000000001).
"""
from __future__ import annotations

import json
import math
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

STUDY_DIR = Path(__file__).resolve().parent
DAILY = pd.read_csv(STUDY_DIR / "es_daily.csv", parse_dates=["session_date"])
FOMC = json.loads((STUDY_DIR / "fomc_events.json").read_text(encoding="utf-8"))
BLS_DATES = json.loads((STUDY_DIR / "bls_release_dates.json").read_text(encoding="utf-8"))
CHART_DIR = STUDY_DIR / "charts"
CHART_DIR.mkdir(exist_ok=True)

HORIZONS = {"r0": 0, "r1": 1, "r5": 5, "r20": 20}
BLS_SERIES = {"CUSR0000SA0": "cpi", "CES0000000001": "nfp"}


def norm_p(t: float, n: int) -> float:
    if n < 2:
        return float("nan")
    # two-sided normal-approximation p-value via erf
    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t) / math.sqrt(2.0))))


def fetch_bls_values() -> dict:
    body = json.dumps(
        {"seriesid": list(BLS_SERIES), "startyear": "2020", "endyear": "2024"}
    ).encode()
    req = urllib.request.Request(
        "https://api.bls.gov/publicAPI/v2/timeseries/data/",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "CapoHornLab-research/1.0"},
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    out: dict[str, list[tuple[str, float]]] = {}
    for s in resp["Results"]["series"]:
        sid = s["seriesID"]
        rows = []
        for d in s["data"]:
            rows.append((f"{d['year']}-{d['period'][1:]}-01", float(d["value"])))
        out[BLS_SERIES[sid]] = sorted(rows)
    return out


def build_event_sets(bls: dict) -> tuple[list[dict], list[dict]]:
    # CPI mom% and NFP monthly change
    cpi_df = pd.DataFrame(bls["cpi"], columns=["month", "cpi"])
    cpi_df["mom"] = cpi_df["cpi"].pct_change() * 100.0
    nfp_df = pd.DataFrame(bls["nfp"], columns=["month", "nfp"])
    nfp_df["chg"] = nfp_df["nfp"].diff()  # CES0000000001 is in thousands of persons; diff = payroll change (thousands)

    cpi_events, nfp_events = [], []
    for year, evs in BLS_DATES.items():
        for ev in evs:
            date = f"{ev['date'][:4]}-{ev['date'][4:6]}-{ev['date'][6:]}"
            # A release in month R reports the data of month R-1 (BLS convention).
            rel = pd.Timestamp(date)
            data_month = (rel - pd.DateOffset(months=1)).strftime("%Y-%m-01")
            if ev["release"] == "Consumer Price Index":
                row = cpi_df[cpi_df["month"] == data_month]
                if row.empty:
                    continue
                mom = float(row["mom"].iloc[0])
                prev = cpi_df[cpi_df["month"] < data_month]
                prev_mom = float(prev["mom"].iloc[-1]) if len(prev) else float("nan")
                cpi_events.append({
                    "date": date, "type": "cpi", "mom_pct": mom,
                    "hot": mom >= 0.4, "cool": mom <= 0.1, "accel": mom > prev_mom,
                })
            elif ev["release"] == "Employment Situation":
                row = nfp_df[nfp_df["month"] == data_month]
                if row.empty:
                    continue
                chg = float(row["chg"].iloc[0])
                nfp_events.append({
                    "date": date, "type": "nfp", "chg_k": chg,
                    "strong": chg >= 200.0, "weak": chg <= 120.0,
                })
    return cpi_events, nfp_events


def session_positions(daily: pd.DataFrame) -> pd.Series:
    dates = daily["session_date"].reset_index(drop=True)
    pos = pd.Series(range(len(dates)), index=dates)
    return pos


def compute_stats(returns: pd.Series, baseline: pd.Series) -> dict:
    r = returns.dropna()
    n = len(r)
    if n == 0:
        return {"n": 0}
    mean = float(r.mean())
    std = float(r.std(ddof=1)) if n > 1 else 0.0
    se = std / math.sqrt(n) if n > 1 else float("nan")
    t = mean / se if se and se > 0 else float("nan")
    win = float((r > 0).mean()) * 100.0
    base = float(baseline.mean()) if len(baseline) else float("nan")
    return {
        "n": n,
        "mean_pct": round(mean * 100.0, 4),
        "median_pct": round(float(r.median()) * 100.0, 4),
        "std_pct": round(std * 100.0, 4),
        "t_stat": round(t, 3) if not math.isnan(t) else None,
        "p_value": round(norm_p(t, n), 4) if not math.isnan(t) else None,
        "win_rate_pct": round(win, 2),
        "baseline_mean_pct": round(base * 100.0, 4) if not math.isnan(base) else None,
        "excess_vs_baseline_bps": round((mean - base) * 10000.0, 1) if not math.isnan(base) else None,
    }


def event_study(events: list[dict], daily: pd.DataFrame, label: str, group_key: str) -> dict:
    dates = daily["session_date"].reset_index(drop=True)
    pos = session_positions(daily)
    closes = daily["close"].reset_index(drop=True)
    daily_ret = closes / closes.shift(1) - 1.0
    # Baseline: r0 = event-day (close-to-close) return; rk = forward k-session return.
    baseline = {"r0": daily_ret.dropna()}
    for h in ("r1", "r5", "r20"):
        baseline[h] = (closes.shift(-HORIZONS[h]) / closes - 1.0).dropna()

    result: dict[str, dict] = {}
    car = {g: [] for g in set(e[group_key] for e in events)}
    for ev in events:
        # CME Globex session label = the calendar day the 17:00 CT session starts,
        # so trading day D has label D-1. Map event date -> first session label >= D-1
        # (handles weekend/holiday edge cases like the 2020-03-15 Sunday emergency cut).
        d = pd.Timestamp(ev["date"]) - pd.Timedelta(days=1)
        candidates = pos.index[pos.index >= d]
        if len(candidates) == 0:
            continue
        i = pos[candidates[0]]
        group = str(ev[group_key])
        path = []
        for k in range(-5, 21):
            j = i + k
            if 0 <= j < len(closes) - 1:
                path.append(float(closes[j] / closes[i] - 1.0) * 100.0)
            else:
                path.append(float("nan"))
        car[group].append(path)
        for h, k in HORIZONS.items():
            if h == "r0":
                if i >= 1:
                    ret = pd.Series([closes[i] / closes[i - 1] - 1.0])
                else:
                    ret = pd.Series(dtype=float)
            elif i + k < len(closes):
                ret = pd.Series([closes[i + k] / closes[i] - 1.0])
            else:
                ret = pd.Series(dtype=float)
            result.setdefault(group, {}).setdefault(h, []).append(ret.iloc[0] if len(ret) else float("nan"))

    out = {"label": label, "groups": {}}
    for g, series_map in result.items():
        out["groups"][g] = {}
        for h, vals in series_map.items():
            s = pd.Series([v for v in vals if not math.isnan(v)])
            out["groups"][g][h] = compute_stats(s, baseline[h].dropna())
        # CAR path (t=-5..+20) mean across events
        paths = pd.DataFrame(car[g])
        out["groups"][g]["car_mean_pct"] = [round(float(x), 3) if not math.isnan(x) else None
                                            for x in paths.mean(axis=0).tolist()]
    return out


def render_charts(fomc_res: dict, cpi_res: dict, nfp_res: dict) -> list[str]:
    files = []

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for ax, (res, title) in zip(axes, [(fomc_res, "FOMC"), (cpi_res, "CPI release"), (nfp_res, "NFP release")]):
        for g, data in res["groups"].items():
            car = data["car_mean_pct"]
            ax.plot(range(-5, 21), car, marker="o", markersize=2.5, label=g)
        ax.axvline(0, color="black", lw=0.8, ls="--")
        ax.axhline(0, color="gray", lw=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("trading sessions around event")
        ax.set_ylabel("cumulative mean return %")
        ax.legend(fontsize=8)
    fig.tight_layout()
    p1 = CHART_DIR / "car_around_events.png"
    fig.savefig(p1, dpi=110)
    plt.close(fig)
    files.append(str(p1))

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for ax, (res, title) in zip(axes, [(fomc_res, "FOMC"), (cpi_res, "CPI"), (nfp_res, "NFP")]):
        h_labels = list(HORIZONS)
        x = range(len(h_labels))
        width = 0.8 / max(len(res["groups"]), 1)
        for gi, (g, data) in enumerate(res["groups"].items()):
            means = [data[h]["mean_pct"] for h in h_labels]
            ax.bar([xi + gi * width for xi in x], means, width=width, label=g)
        ax.axhline(0, color="gray", lw=0.6)
        ax.set_xticks([xi + width for xi in x])
        ax.set_xticklabels(h_labels)
        ax.set_title(f"Mean forward return by horizon — {title}", fontsize=10)
        ax.set_ylabel("mean return %")
        ax.legend(fontsize=8)
    fig.tight_layout()
    p2 = CHART_DIR / "mean_returns_by_horizon.png"
    fig.savefig(p2, dpi=110)
    plt.close(fig)
    files.append(str(p2))
    return files


def main() -> None:
    bls = fetch_bls_values()
    cpi_events, nfp_events = build_event_sets(bls)
    # FOMC groups by rate action (delta of rate_after lower bound)
    def rate_lower(rate: str) -> float:
        return float(rate.split("–")[0].replace("%", ""))
    fomc_events = FOMC
    prev_rate = None
    for e in fomc_events:
        cur = rate_lower(e["rate_after"])
        e["delta_bp"] = None if prev_rate is None else round((cur - prev_rate) * 100.0)
        e["group"] = "hike" if (e["delta_bp"] or 0) > 0 else "cut" if (e["delta_bp"] or 0) < 0 else "hold"
        prev_rate = cur
    for e in cpi_events:
        e["group"] = "hot" if e["hot"] else "cool" if e["cool"] else "moderate"
    for e in nfp_events:
        e["group"] = "strong" if e["strong"] else "weak" if e["weak"] else "moderate"

    fomc_res = event_study(fomc_events, DAILY, "FOMC", "group")
    cpi_res = event_study(cpi_events, DAILY, "CPI", "group")
    nfp_res = event_study(nfp_events, DAILY, "NFP", "group")

    charts = render_charts(fomc_res, cpi_res, nfp_res)

    summary = {
        "instrument": "ES (E-mini S&P 500)",
        "period": "2020-01-01..2024-12-30",
        "daily_sessions": len(DAILY),
        "event_counts": {
            "fomc": len(fomc_events),
            "cpi": len(cpi_events),
            "nfp": len(nfp_events),
        },
        "horizons": list(HORIZONS),
        "fomc": fomc_res,
        "cpi": cpi_res,
        "nfp": nfp_res,
        "charts": charts,
        "caveats": [
            "Overlapping long-window events (r20) are not overlap-adjusted; p-values are indicative.",
            "Event classification uses realized data (CPI mom%, NFP change), not market consensus surprises.",
            "Daily closes are CME Globex-session aggregated from owned 1m data; no costs, no fills model.",
            "FOMC Jan 2020 row supplemented from the Federal Reserve statement (Wikipedia table omits it).",
        ],
    }
    out_json = STUDY_DIR / "news_longhorizon_results.json"
    out_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("EVENT COUNTS: fomc=%d cpi=%d nfp=%d" % (len(fomc_events), len(cpi_events), len(nfp_events)))
    for res in (fomc_res, cpi_res, nfp_res):
        for g, data in res["groups"].items():
            r20 = data.get("r20", {})
            print(f"  {res['label']}/{g}: n={r20.get('n')} r20_mean={r20.get('mean_pct')}% "
                  f"t={r20.get('t_stat')} p={r20.get('p_value')} win={r20.get('win_rate_pct')}% "
                  f"excess_vs_base_bps={r20.get('excess_vs_baseline_bps')}")
    print("saved:", out_json)


if __name__ == "__main__":
    main()
