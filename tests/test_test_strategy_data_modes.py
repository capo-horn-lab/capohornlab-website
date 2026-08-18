"""Contract tests for data-mode and news-event request capture in the strategy wizard."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "test-strategy.html"


class TestStrategyDataModesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.page = PAGE.read_text(encoding="utf-8")

    def test_wizard_offers_tick_depth10_and_news_event_study_modes(self) -> None:
        self.assertIn('id="s2_data_mode"', self.page)
        self.assertIn('value="tick_trades"', self.page)
        self.assertIn('value="depth_10"', self.page)
        self.assertIn('value="news_event"', self.page)
        self.assertIn('id="s2_news_events"', self.page)

    def test_request_payload_preserves_data_and_news_requirements_structurally(self) -> None:
        self.assertIn('data_mode: getVal(\'s2_data_mode\')', self.page)
        self.assertIn('news_event_families: getVal(\'s2_news_events\')', self.page)
        self.assertIn('news_signal_rule: getVal(\'s2_news_rule\')', self.page)
        self.assertIn('indicators_params:', self.page)

    def test_public_copy_does_not_overclaim_depth_or_news_execution(self) -> None:
        self.assertIn('10-level depth is used for liquidity and imbalance research', self.page)
        self.assertIn('does not claim queue position or exact fills', self.page)
        self.assertIn('actual, forecast, prior, revisions and first public availability', self.page)
        self.assertIn('Post-release returns are research outcomes, not inputs available before release', self.page)


if __name__ == "__main__":
    unittest.main()
