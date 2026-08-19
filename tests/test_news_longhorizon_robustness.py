"""Regression checks for the news-study robustness layer."""
import sys
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parents[1] / "research" / "studies" / "news_longhorizon"
sys.path.insert(0, str(STUDY_DIR))

from pre_news_study import holm_adjust, regime_label, subset_sensitivity  # noqa: E402


def test_holm_adjustment_is_monotone_and_conservative():
    adjusted = holm_adjust([0.01, 0.03, 0.20, None])
    assert adjusted == [0.03, 0.06, 0.20, None]


def test_regime_labels_and_covid_exclusion_are_explicit():
    assert regime_label("2020-01-03") == "2020_2021"
    assert regime_label("2022-01-03") == "2022_2024"

    rows = [
        {"date": "2020-06-05", "pre5": 0.01, "r20": 0.02},
        {"date": "2022-06-03", "pre5": -0.01, "r20": -0.02},
        {"date": "2023-06-02", "pre5": 0.02, "r20": 0.01},
    ]
    result = subset_sensitivity(rows, "all")
    assert result["n"] == 3
    assert result["same_sign"]["hit_rate"] == 100.0
