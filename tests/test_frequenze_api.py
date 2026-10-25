"""PUT/GET /api/v1/frequenze: live snapshot published by the trading engine."""
from __future__ import annotations

import asyncio
import json
import os
import unittest
from datetime import datetime, timezone

# Must be set before `app` is imported: settings and the engine are built at import time.
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_frequenze.db"
os.environ["FREQ_PUBLISH_TOKEN"] = "test-token"

import httpx  # noqa: E402
from sqlalchemy import func, select  # noqa: E402

import app.models  # noqa: E402,F401  # register every table on Base.metadata
from app.api.v1.frequenze import eta_secondi  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.core.database import AsyncSessionLocal, Base, async_engine  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402
from app.models.live_snapshot import LiveSnapshot  # noqa: E402

OK = {"generato": "2026-10-26 15:31", "strumenti": {"MNQ": {"contratto": "MNQ 12-26"}}}
TOKEN = {"X-Publish-Token": "test-token"}


def run(coro_fn):
    """Run one coroutine function on a fresh loop; dispose pooled connections tied to it."""

    async def main():
        try:
            return await coro_fn()
        finally:
            await async_engine.dispose()

    return asyncio.run(main())


def client() -> httpx.AsyncClient:
    # ASGITransport does not run the lifespan, so setUp creates the tables itself.
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=fastapi_app), base_url="http://test")


class FrequenzeApiTest(unittest.TestCase):
    def setUp(self) -> None:
        # drop_all below must never touch a real database (e.g. if another module imported `app` first).
        self.assertTrue(str(async_engine.url).endswith("test_frequenze.db"), async_engine.url)

        async def reset():
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        run(reset)

    @classmethod
    def tearDownClass(cls) -> None:
        run(async_engine.dispose)
        if os.path.exists("test_frequenze.db"):
            os.remove("test_frequenze.db")

    def put(self, content: bytes | str, headers: dict | None = None) -> httpx.Response:
        async def go():
            async with client() as c:
                return await c.put("/api/v1/frequenze", content=content, headers=headers or {})

        return run(go)

    def get(self) -> httpx.Response:
        async def go():
            async with client() as c:
                return await c.get("/api/v1/frequenze")

        return run(go)

    def test_get_vuoto_restituisce_dati_null(self):
        r = self.get()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"ricevuto": None, "eta_s": None, "dati": None})
        self.assertEqual(r.headers["cache-control"], "no-store")

    def test_put_senza_variabile_503(self):
        prima = settings.FREQ_PUBLISH_TOKEN
        settings.FREQ_PUBLISH_TOKEN = None
        try:
            r = self.put(json.dumps(OK), TOKEN)
        finally:
            settings.FREQ_PUBLISH_TOKEN = prima
        self.assertEqual(r.status_code, 503)
        self.assertNotIn("test-token", r.text)
        self.assertIsNone(self.get().json()["dati"])

    def test_put_token_mancante_401(self):
        r = self.put(json.dumps(OK))
        self.assertEqual(r.status_code, 401)
        self.assertIsNone(self.get().json()["dati"])

    def test_put_token_sbagliato_401(self):
        r = self.put(json.dumps(OK), {"X-Publish-Token": "nope"})
        self.assertEqual(r.status_code, 401)
        self.assertNotIn("test-token", r.text)
        self.assertIsNone(self.get().json()["dati"])

    def test_put_token_con_spazi_accettato(self):
        # the header is stripped, and so is the configured value; a configured value that is only whitespace means "not configured"
        self.assertEqual(self.put(json.dumps(OK), {"X-Publish-Token": " test-token\n"}).status_code, 204)
        prima = settings.FREQ_PUBLISH_TOKEN
        try:
            for configurato, atteso in ((" test-token\n", 204), (" \n", 503)):
                settings.FREQ_PUBLISH_TOKEN = configurato
                with self.subTest(configurato=configurato):
                    self.assertEqual(self.put(json.dumps(OK), TOKEN).status_code, atteso)
        finally:
            settings.FREQ_PUBLISH_TOKEN = prima

    def test_put_ok_poi_get_restituisce_dati(self):
        r = self.put(json.dumps(OK), TOKEN)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.content, b"")
        g = self.get()
        self.assertEqual(g.status_code, 200)
        self.assertEqual(g.headers["cache-control"], "no-store")
        corpo = g.json()
        self.assertEqual(corpo["dati"], OK)
        self.assertIsInstance(corpo["eta_s"], int)
        self.assertTrue(0 <= corpo["eta_s"] <= 5)
        self.assertTrue(corpo["ricevuto"].endswith("Z"))
        datetime.strptime(corpo["ricevuto"], "%Y-%m-%dT%H:%M:%SZ")  # raises if the format is off

    def test_put_sovrascrive_la_riga(self):
        primo = {"generato": "2026-10-26 15:31", "strumenti": {"MNQ": {}}}
        secondo = {"generato": "2026-10-26 15:32", "strumenti": {"MNQ": {}, "MES": {}}}
        self.assertEqual(self.put(json.dumps(primo), TOKEN).status_code, 204)
        self.assertEqual(self.put(json.dumps(secondo), TOKEN).status_code, 204)
        self.assertEqual(self.get().json()["dati"], secondo)

        async def conta():
            async with AsyncSessionLocal() as db:
                return (await db.execute(select(func.count()).select_from(LiveSnapshot))).scalar_one()

        self.assertEqual(run(conta), 1)

    def test_put_corpo_non_oggetto_422(self):
        for corpo in (b"[]", json.dumps({"generato": "x"}), json.dumps({"generato": 1, "strumenti": {}}),
                      json.dumps({"generato": "x", "strumenti": []})):
            with self.subTest(corpo=corpo):
                self.assertEqual(self.put(corpo, TOKEN).status_code, 422)
        self.assertIsNone(self.get().json()["dati"])

    def test_put_corpo_non_json_422(self):
        # Never 500, and nothing stored: invalid UTF-8, malformed JSON, runaway nesting, and values that
        # parse but could not be rendered by the public GET (NaN, 1e999 -> inf, lone surrogate).
        for corpo in (b"\xff\xfe{", b"{", b"[" * 100_000,
                      b'{"generato":"x","strumenti":{"MNQ":NaN}}',
                      b'{"generato":"x","strumenti":{"MNQ":1e999}}',
                      b'{"generato":"\\ud800","strumenti":{}}'):
            with self.subTest(corpo=corpo[:20]):
                self.assertEqual(self.put(corpo, TOKEN).status_code, 422)
                self.assertIsNone(self.get().json()["dati"])

    def test_put_oltre_1mb_413(self):
        corpo = json.dumps({"generato": "x", "strumenti": {"MNQ": "x" * 1_050_000}})
        self.assertGreater(len(corpo), 1_048_576)
        self.assertEqual(self.put(corpo, TOKEN).status_code, 413)
        self.assertIsNone(self.get().json()["dati"])

    def test_eta_mai_negativa(self):
        adesso = datetime.now(timezone.utc)
        self.assertEqual(eta_secondi("2099-01-01T00:00:00Z", adesso), 0)


if __name__ == "__main__":
    unittest.main()
