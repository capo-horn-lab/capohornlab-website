"""Tests for a look-ahead-safe, source-validated economic-news calendar."""
from __future__ import annotations

import pandas as pd


def test_calendar_features_only_events_known_at_or_before_each_bar():
    from research.news_calendar import EconomicNewsCalendar

    events = pd.DataFrame(
        {
            "event_id": ["bls-cpi-2024-01"],
            "release_time_utc": pd.to_datetime(["2024-01-10T13:30:00Z"], utc=True),
            "available_at_utc": pd.to_datetime(["2024-01-10T13:30:00Z"], utc=True),
            "event_name": ["Consumer Price Index"],
            "category": ["inflation"],
            "source": ["BLS"],
            "source_url": ["https://www.bls.gov/schedule/news_release/cpi.htm"],
            "importance": ["high"],
        }
    )
    bars = pd.DataFrame(
        {"close": [100.0, 101.0, 102.0]},
        index=pd.to_datetime(
            ["2024-01-10T13:29:00Z", "2024-01-10T13:30:00Z", "2024-01-10T13:31:00Z"], utc=True
        ),
    )

    features = EconomicNewsCalendar(events).known_event_features(bars)

    assert features.loc[pd.Timestamp("2024-01-10T13:29:00Z"), "high_impact_event_now"] == 0
    assert features.loc[pd.Timestamp("2024-01-10T13:30:00Z"), "high_impact_event_now"] == 1
    assert pd.isna(features.loc[pd.Timestamp("2024-01-10T13:29:00Z"), "minutes_since_last_event"])
    assert features.loc[pd.Timestamp("2024-01-10T13:31:00Z"), "minutes_since_last_event"] == 1.0


def test_calendar_event_study_labels_post_release_return_without_claiming_a_signal():
    from research.news_calendar import EconomicNewsCalendar

    events = pd.DataFrame(
        {
            "event_id": ["fed-fomc-2024-01"],
            "release_time_utc": pd.to_datetime(["2024-01-31T19:00:00Z"], utc=True),
            "available_at_utc": pd.to_datetime(["2024-01-31T19:00:00Z"], utc=True),
            "event_name": ["FOMC statement"],
            "category": ["monetary_policy"],
            "source": ["Federal Reserve"],
            "source_url": ["https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"],
            "importance": ["high"],
        }
    )
    bars = pd.DataFrame(
        {"close": [100.0, 101.5, 102.0]},
        index=pd.to_datetime(
            ["2024-01-31T18:59:00Z", "2024-01-31T19:00:00Z", "2024-01-31T19:01:00Z"], utc=True
        ),
    )

    study = EconomicNewsCalendar(events).event_study(bars, post_minutes=1)

    assert study.loc[0, "baseline_close"] == 100.0
    assert study.loc[0, "post_close"] == 102.0
    assert study.loc[0, "post_return_bps"] == 200.0
    assert study.loc[0, "analysis_label"] == "post_release_outcome_not_a_signal"
