"""Tests for the dependency-free OHLCV analysis CLI."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ohlcv_analyzer import analyse_ohlcv


class OhlcvAnalyzerTests(unittest.TestCase):
    def test_analysis_emits_moving_averages_returns_volatility_and_crosses(self) -> None:
        # A long decline puts the 50-day average below the 200-day average.
        # The following sustained rally creates a 50/200 golden cross.
        rows = [
            {"date": f"2024-01-{index + 1:03d}", "open": 0, "high": 0, "low": 0,
             "close": float(400 - index), "volume": 1000}
            for index in range(200)
        ]
        rows.extend(
            {
                "date": f"2025-01-{index + 1:03d}", "open": 0, "high": 0, "low": 0,
                "close": float(201 + index * 10), "volume": 1000,
            }
            for index in range(100)
        )

        result = analyse_ohlcv(rows)

        self.assertEqual(result["observations"], 300)
        self.assertIsNone(result["moving_averages"][0]["sma_20"])
        self.assertAlmostEqual(result["moving_averages"][-1]["sma_20"], 1096.0)
        self.assertEqual(result["daily_log_returns"][0]["log_return"], None)
        self.assertGreater(result["volatility"]["daily"], 0)
        self.assertGreater(result["volatility"]["annualized_252_days"], 0)
        self.assertTrue(
            any(cross["pattern"] == "golden_cross" for cross in result["crosses"])
        )

    def test_cli_reads_standard_ohlcv_csv_and_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            csv_path = directory_path / "prices.csv"
            json_path = directory_path / "summary.json"
            with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=["Date", "Open", "High", "Low", "Close", "Volume"],
                )
                writer.writeheader()
                for index in range(200):
                    writer.writerow(
                        {
                            "Date": f"2024-01-{index + 1:03d}",
                            "Open": 1,
                            "High": 1,
                            "Low": 1,
                            "Close": 100 + index,
                            "Volume": 1000,
                        }
                    )

            completed = subprocess.run(
                [sys.executable, "ohlcv_analyzer.py", str(csv_path), "--output", str(json_path)],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.stdout, "")
            summary = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["observations"], 200)
            self.assertEqual(summary["source"], str(csv_path))
            self.assertAlmostEqual(summary["latest"]["sma_200"], 199.5)


if __name__ == "__main__":
    unittest.main()
