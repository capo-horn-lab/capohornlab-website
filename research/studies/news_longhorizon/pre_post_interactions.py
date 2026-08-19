"""Pre × post interaction helpers for the news long-horizon study.

Pre-news drift classification (5-session window) and Holm-Bonferroni
multiple-testing adjustment used by the pre×post interaction analysis.
"""
from __future__ import annotations

from typing import List, Optional

# Half-band (decimal return) around zero treated as "flat" pre-news drift.
# 0.25% over 5 sessions ≈ noise floor for ES daily.
FLAT_BAND = 0.0025


def classify_pre5(drift: float) -> str:
    """Classify the pre-news 5-session drift as negative/flat/positive."""
    if drift < -FLAT_BAND:
        return "negative"
    if drift > FLAT_BAND:
        return "positive"
    return "flat"


def holm_adjust(p_values: List[Optional[float]]) -> List[Optional[float]]:
    """Holm-Bonferroni step-up adjustment, preserving None placeholders.

    For k non-missing p-values sorted ascending, the i-th smallest p is
    multiplied by (k - i). None entries stay None in their original slot.
    """
    idx = [(i, p) for i, p in enumerate(p_values) if p is not None]
    k = len(idx)
    if k == 0:
        return list(p_values)
    ordered = sorted(idx, key=lambda t: t[1])
    adjusted: dict[int, float] = {}
    for rank, (orig_i, p) in enumerate(ordered):
        adjusted[orig_i] = min(1.0, p * (k - rank))
    return [
        adjusted[i] if p_values[i] is not None else None
        for i in range(len(p_values))
    ]
