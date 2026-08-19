"""COVID sensitivity analysis for the post-release ES event study.

This is a descriptive robustness check only. It reuses the parent study's event
classification and forward-return definition, and compares the full sample with:
(1) removal of events dated in March--April 2020; (2) removal of all 2020 events.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from news_event_study import DAILY, FOMC, build_event_sets, event_study, fetch_bls_values

STUDY_DIR = Path(__file__).resolve().parent
SCENARIOS = {
    "full_sample": "No event-date exclusion.",
    "exclude_covid_mar_apr_2020": "Exclude events dated 2020-03-01 through 2020-04-30 inclusive.",
    "exclude_2020": "Exclude all events dated in calendar year 2020.",
}


def filter_event_dates(events: Iterable[dict], scenario: str) -> list[dict]:
    """Return copied events under a predeclared date exclusion, without mutation."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    copied = [dict(event) for event in events]
    if scenario == "full_sample":
        return copied
    if scenario == "exclude_covid_mar_apr_2020":
        return [e for e in copied if not ("2020-03-01" <= e["date"] <= "2020-04-30")]
    return [e for e in copied if not e["date"].startswith("2020-")]


def classify_events() -> dict[str, list[dict]]:
    """Build the identical realized-outcome groups used by the parent study."""
    cpi_events, nfp_events = build_event_sets(fetch_bls_values())
    fomc_events = [dict(event) for event in FOMC]

    def rate_lower(rate: str) -> float:
        return float(rate.split("–")[0].replace("%", ""))

    previous_rate = None
    for event in fomc_events:
        current_rate = rate_lower(event["rate_after"])
        delta_bp = None if previous_rate is None else round((current_rate - previous_rate) * 100.0)
        event["group"] = "hike" if (delta_bp or 0) > 0 else "cut" if (delta_bp or 0) < 0 else "hold"
        previous_rate = current_rate
    for event in cpi_events:
        event["group"] = "hot" if event["hot"] else "cool" if event["cool"] else "moderate"
    for event in nfp_events:
        event["group"] = "strong" if event["strong"] else "weak" if event["weak"] else "moderate"
    return {"fomc": fomc_events, "cpi": cpi_events, "nfp": nfp_events}


def r20_rows(result: dict) -> dict[str, dict]:
    """Keep only machine-readable r20 fields; CAR paths are unchanged parent output."""
    return {group: payload.get("r20", {"n": 0}) for group, payload in result["groups"].items()}


def run() -> dict:
    event_sets = classify_events()
    scenarios: dict[str, dict] = {}
    for name, description in SCENARIOS.items():
        scenarios[name] = {"description": description, "results": {}}
        for family, events in event_sets.items():
            filtered = filter_event_dates(events, name)
            study = event_study(filtered, DAILY, family.upper(), "group")
            scenarios[name]["results"][family] = r20_rows(study)
    return {
        "study": "ES post-release long-horizon COVID sensitivity",
        "status": "preliminary_non_promotable",
        "instrument": "ES (E-mini S&P 500)",
        "period": "2020-01-01..2024-12-30",
        "horizon": "r20: close-to-close forward 20 CME Globex sessions",
        "event_classification": "Realized CPI month-over-month, NFP payroll change, and FOMC target-range action; not consensus surprises.",
        "scenarios": scenarios,
        "limitations": [
            "Event-date sensitivity is not an as-of event-vintage or source-provenance validation.",
            "Twenty-session windows overlap; the parent study's unadjusted normal-approximation p-values remain indicative.",
            "No multiplicity correction is applied across families, groups, horizons, or sensitivity scenarios.",
            "Daily-close reference returns have no executable fill, cost, slippage, roll, or position-sizing model.",
            "This does not establish a tradeable strategy or causal mechanism.",
        ],
    }


def render_report(summary: dict) -> str:
    lines = [
        "# Post-News COVID Robustness — ES Long-Horizon Event Study",
        "",
        "**Status:** Preliminary and non-promotable. Descriptive sensitivity only; not a trading rule.",
        "",
        "## Objective",
        "Test whether the parent study's post-release r20 summaries persist after excluding March–April 2020 and, separately, all of 2020. Event definitions, session alignment, and r20 calculation are unchanged.",
        "",
        "## Results (r20)",
        "",
        "| Scenario | Family / group | N | Mean % | Median % | t | unadjusted p | Win % |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for scenario, payload in summary["scenarios"].items():
        for family, groups in payload["results"].items():
            for group, stats in groups.items():
                lines.append(
                    f"| {scenario} | {family}/{group} | {stats.get('n', 0)} | "
                    f"{stats.get('mean_pct', '—')} | {stats.get('median_pct', '—')} | "
                    f"{stats.get('t_stat', '—')} | {stats.get('p_value', '—')} | {stats.get('win_rate_pct', '—')} |"
                )
    lines += [
        "",
        "## Interpretation",
        "The table is a stress test of sample composition, not confirmatory evidence. A result that materially changes under either exclusion is regime-sensitive. A result that does not change still remains preliminary because it has not passed the parent study's provenance, as-of-vintage, IS/OOS, overlap-robust, multiple-testing, and execution-assumption gates.",
        "",
        "## Limits",
    ]
    lines.extend(f"- {item}" for item in summary["limitations"])
    lines += [
        "",
        "## Reproducibility",
        "Run `.venv/Scripts/python.exe research/studies/news_longhorizon/post_news_robustness.py`. Output: `post_news_robustness_results.json` and this report.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    summary = run()
    output = STUDY_DIR / "post_news_robustness_results.json"
    report = STUDY_DIR / "POST_NEWS_ROBUSTNESS_REPORT.md"
    output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    report.write_text(render_report(summary), encoding="utf-8")
    for scenario, payload in summary["scenarios"].items():
        weak = payload["results"].get("nfp", {}).get("weak", {})
        hold = payload["results"].get("fomc", {}).get("hold", {})
        print(f"{scenario}: nfp_weak n={weak.get('n')} mean={weak.get('mean_pct')} p={weak.get('p_value')} | "
              f"fomc_hold n={hold.get('n')} mean={hold.get('mean_pct')} p={hold.get('p_value')}")
    print(f"SAVED {output.name} {report.name}")


if __name__ == "__main__":
    main()
