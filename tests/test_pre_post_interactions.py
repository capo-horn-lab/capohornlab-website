"""Regression checks for descriptive pre×post interaction helpers."""
import sys
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parents[1] / "research" / "studies" / "news_longhorizon"
sys.path.insert(0, str(STUDY_DIR))

from pre_post_interactions import FLAT_BAND, classify_pre5, holm_adjust  # noqa: E402


def test_pre5_states_have_fixed_zero_centered_flat_band():
    assert FLAT_BAND == 0.0025
    assert classify_pre5(-0.0026) == "negative"
    assert classify_pre5(-0.0025) == "flat"
    assert classify_pre5(0.0) == "flat"
    assert classify_pre5(0.0025) == "flat"
    assert classify_pre5(0.0026) == "positive"


def test_holm_adjustment_is_monotone_and_preserves_missing_values():
    assert holm_adjust([0.01, 0.03, 0.20, None]) == [0.03, 0.06, 0.20, None]
