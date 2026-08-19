"""Regression checks for fixed-calendar post-news regime sensitivity."""
import sys
from pathlib import Path

import pytest

STUDY_DIR = Path(__file__).resolve().parents[1] / "research" / "studies" / "news_longhorizon"
sys.path.insert(0, str(STUDY_DIR))

from post_news_regime_split import filter_regime, regime_label, student_t_stats  # noqa: E402


def test_regime_labels_are_fixed_and_filtering_does_not_mutate():
    events = [
        {"date": "2020-03-06", "group": "weak"},
        {"date": "2021-12-03", "group": "weak"},
        {"date": "2022-01-07", "group": "weak"},
        {"date": "2024-12-06", "group": "weak"},
    ]
    assert regime_label("2020-01-01") == "2020_2021"
    assert regime_label("2021-12-31") == "2020_2021"
    assert regime_label("2022-01-01") == "2022_2024"
    assert [item["date"] for item in filter_regime(events, "2020_2021")] == ["2020-03-06", "2021-12-03"]
    assert [item["date"] for item in filter_regime(events, "2022_2024")] == ["2022-01-07", "2024-12-06"]
    assert len(events) == 4


def test_student_stats_independently_recomputes_known_sample():
    summary = student_t_stats([0.01, -0.01, 0.03])
    assert summary["n"] == 3
    assert summary["mean_pct"] == pytest.approx(1.0)
    assert summary["median_pct"] == pytest.approx(1.0)
    assert summary["std_pct"] == pytest.approx(2.0)
    assert summary["win_rate_pct"] == pytest.approx(66.67)
    assert summary["t_stat"] == pytest.approx(0.866, abs=0.001)
    assert summary["p_value"] == pytest.approx(0.478, abs=0.001)
