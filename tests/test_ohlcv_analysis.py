import math
import unittest

from ohlcv_analysis import analyze_ohlcv


class AnalyzeOhlcvTests(unittest.TestCase):
    def test_calculates_indicators_crosses_returns_and_json_safe_summary(self):
        # The step up creates a 20/50 golden cross; the later decline creates a death cross.
        closes = [100.0] * 60 + [200.0] * 60 + [100.0] * 100
        rows = [
            {
                "Date": f"2024-01-{index + 1:03d}",
                "Open": str(close),
                "High": str(close + 1),
                "Low": str(close - 1),
                "Close": str(close),
                "Volume": "1000",
            }
            for index, close in enumerate(closes)
        ]

        summary = analyze_ohlcv(rows, source_name="fixture.csv")

        self.assertEqual(summary["source"], "fixture.csv")
        self.assertEqual(summary["row_count"], 220)
        self.assertEqual(summary["date_range"], {"start": "2024-01-001", "end": "2024-01-220"})
        self.assertEqual(summary["latest_indicators"]["sma_20"], 100.0)
        self.assertEqual(summary["latest_indicators"]["sma_50"], 100.0)
        self.assertEqual(summary["latest_indicators"]["sma_200"], 130.0)
        self.assertGreaterEqual(len(summary["crosses"]["golden_crosses"]), 1)
        self.assertGreaterEqual(len(summary["crosses"]["death_crosses"]), 1)
        self.assertEqual(len(summary["daily_log_returns"]), 219)
        self.assertTrue(math.isfinite(summary["volatility"]["daily_log_return_stddev"]))
        self.assertTrue(math.isfinite(summary["volatility"]["annualized_log_return_stddev"]))


if __name__ == "__main__":
    unittest.main()
