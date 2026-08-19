"""Prevent incomplete event studies from becoming public trading claims."""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY_REPORT = ROOT / "research" / "studies" / "news_longhorizon" / "REPORT.md"
PUBLIC_PAGES = (
    ROOT / "research.html",
    ROOT / "research-detail.html",
    ROOT / "pages" / "research.html",
    ROOT / "pages" / "research-detail.html",
)


def test_incomplete_news_study_is_quarantined_from_public_research_until_governance_gates_pass():
    report = STUDY_REPORT.read_text(encoding="utf-8").lower()
    assert "preliminary and non-promotable" in report
    assert "not an execution-ready strategy" in report
    assert "buy weak payrolls" not in report
    assert "the patience is the edge" not in report

    for page in PUBLIC_PAGES:
        assert "news-event-long-horizon-es" not in page.read_text(encoding="utf-8")
