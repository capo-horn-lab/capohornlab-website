"""Regression checks for post-release COVID robustness filtering."""
import sys
from pathlib import Path

STUDY_DIR = Path(__file__).resolve().parents[1] / "research" / "studies" / "news_longhorizon"
sys.path.insert(0, str(STUDY_DIR))

from post_news_robustness import filter_event_dates  # noqa: E402


def test_covid_filters_are_explicit_and_non_mutating():
    events = [
        {"date": "2020-03-06", "group": "weak"},
        {"date": "2020-03-20", "group": "weak"},
        {"date": "2020-04-03", "group": "weak"},
        {"date": "2020-05-08", "group": "weak"},
        {"date": "2021-01-08", "group": "weak"},
    ]

    assert [e["date"] for e in filter_event_dates(events, "exclude_covid_mar_apr_2020")] == [
        "2020-05-08", "2021-01-08"
    ]
    assert [e["date"] for e in filter_event_dates(events, "exclude_2020")] == ["2021-01-08"]
    assert len(events) == 5
