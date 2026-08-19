"""Regression checks for finite, small-sample pre-news inference."""
import math
import sys
from pathlib import Path


STUDY_DIR = Path(__file__).resolve().parents[1] / "research" / "studies" / "news_longhorizon"
sys.path.insert(0, str(STUDY_DIR))
from pre_news_study import contingency, pearson, tstats  # noqa: E402


def test_tstats_uses_finite_values_t_distribution_and_standard_even_median():
    result = tstats([float("nan"), 0.01, 0.02, 0.03, 0.04])
    assert result["n"] == 4
    assert result["median"] == 2.5
    assert 0 < result["p"] < 0.1


def test_predictive_statistics_exclude_nan_and_report_a_binomial_hit_rate_p_value():
    correlation = pearson([0.01, float("nan"), 0.03, 0.04], [0.02, 0.01, 0.06, 0.08])
    assert correlation["n"] == 3
    assert math.isfinite(correlation["r"])

    import pandas as pd
    result = contingency(pd.DataFrame({"pre": [1, 1, -1, -1], "post": [1, -1, -1, -1]}), "pre", "post")
    assert result == {"n": 4, "same_sign": 3, "hit_rate": 75.0, "p_vs_50": 0.625}