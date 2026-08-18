"""Focused behavior checks for the responsible scraping example.

The production module is deliberately implemented with only the Python standard library,
so these tests can run with `python -m unittest -v` on a default Python installation.
"""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from responsible_web_scraper import ResultStore, extract_content, validate_record


class ResponsibleScraperTests(unittest.TestCase):
    def test_extract_content_ignores_non_visible_html_and_collects_metadata(self) -> None:
        html = """
        <html><head>
          <title>Example article</title>
          <meta name="description" content="A concise summary.">
          <script>window.tracker = true;</script>
        </head><body>
          <h1>Responsible crawling</h1>
          <p>First readable paragraph.</p>
          <style>.hidden { display: none; }</style>
          <p>Second readable paragraph.</p>
        </body></html>
        """

        record = extract_content("https://example.test/articles/1", html)

        self.assertEqual(record["title"], "Example article")
        self.assertEqual(record["description"], "A concise summary.")
        self.assertEqual(record["heading"], "Responsible crawling")
        self.assertIn("First readable paragraph.", record["text"])
        self.assertNotIn("window.tracker", record["text"])
        self.assertNotIn("display: none", record["text"])

    def test_validate_record_rejects_empty_or_oversized_content(self) -> None:
        valid = {
            "url": "https://example.test/articles/1",
            "title": "Useful page",
            "description": "",
            "heading": "",
            "text": "A readable article body.",
        }

        self.assertEqual(validate_record(valid), valid)
        with self.assertRaises(ValueError):
            validate_record({**valid, "text": ""})
        with self.assertRaises(ValueError):
            validate_record({**valid, "url": "not-a-url"})

    def test_result_store_writes_json_and_sqlite(self) -> None:
        record = {
            "url": "https://example.test/articles/1",
            "title": "Useful page",
            "description": "A description",
            "heading": "Heading",
            "text": "A readable article body.",
        }

        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            store = ResultStore(output_dir / "results.json", output_dir / "results.sqlite3")
            store.save([record])

            self.assertEqual(json.loads((output_dir / "results.json").read_text("utf-8")), [record])
            connection = sqlite3.connect(output_dir / "results.sqlite3")
            try:
                row = connection.execute(
                    "SELECT url, title, description, heading, text FROM scraped_pages"
                ).fetchone()
            finally:
                # `sqlite3.Connection` context managers commit/rollback but do not close.
                # Explicit close keeps this test portable on Windows, which locks open DB files.
                connection.close()
            self.assertEqual(row, tuple(record.values()))


if __name__ == "__main__":
    unittest.main()
