"""Contract tests for the home page that shows the live frequencies pushed by the trading engine."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


class FrequenzeLiveWiringTests(unittest.TestCase):
    def test_home_carica_il_client_e_porta_la_nota(self) -> None:
        page = read("index.html")
        self.assertIn("assets/js/frequenze-live.js", page)
        self.assertIn("Frequenze descrittive su dati gia' visti, non segnali.", page)
        self.assertIn('id="freq-dati"', page)
        self.assertIn('id="freq-stato"', page)
        self.assertIn('id="freq-avviso"', page)

    def test_home_non_ha_piu_il_contenuto_del_laboratorio(self) -> None:
        page = read("index.html")
        for old in ("pricing.html", "checkout.html", "test-strategy.html", "Enter the Lab"):
            self.assertNotIn(old, page)

    def test_client_legge_il_backend_senza_innerhtml(self) -> None:
        client = read("assets/js/frequenze-live.js")
        for needed in ("/frequenze", "CHL_API_BASE", "textContent", "60000", "JSON.stringify"):
            self.assertIn(needed, client)
        self.assertNotIn("innerHTML", client)


if __name__ == "__main__":
    unittest.main()
