"""PUT/GET /api/v1/live/{chiave} (and the /api/v1/frequenze alias): live snapshots published by the trading engine."""
from __future__ import annotations

import asyncio
import json
import os
import time
import unittest
import unittest.mock
from datetime import datetime, timezone
from pathlib import Path

# Must be set before `app` is imported: settings and the engine are built at import time.
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_frequenze.db"
os.environ["FREQ_PUBLISH_TOKEN"] = "test-token"

import httpx  # noqa: E402
from sqlalchemy import func, select  # noqa: E402

import app.models  # noqa: E402,F401  # register every table on Base.metadata
from app.api.v1.frequenze import CHIAVI, eta_secondi  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.core.database import AsyncSessionLocal, Base, async_engine  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402
from app.models.live_snapshot import LiveSnapshot  # noqa: E402

OK = {"generato": "2026-10-26 15:31", "strumenti": {"MNQ": {"contratto": "MNQ 12-26"}}}
TOKEN = {"X-Publish-Token": "test-token"}
LIVE = "/api/v1/live"
MEMORIA_FIXTURE = Path(__file__).parent / "fixtures" / "memoria-payload.json"  # real engine payload, no local paths


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

    def put(self, content: bytes | str, headers: dict | None = None, path: str = "/api/v1/frequenze") -> httpx.Response:
        async def go():
            async with client() as c:
                return await c.put(path, content=content, headers=headers or {})

        return run(go)

    def get(self, path: str = "/api/v1/frequenze", headers: dict | None = None) -> httpx.Response:
        async def go():
            async with client() as c:
                return await c.get(path, headers=headers or {})

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

    def test_put_oltre_limite_413(self):
        corpo = json.dumps({"generato": "x", "strumenti": {"MNQ": "x" * 2_100_000}})
        self.assertGreater(len(corpo), 2_097_152)
        self.assertEqual(self.put(corpo, TOKEN).status_code, 413)
        self.assertIsNone(self.get().json()["dati"])

    def test_live_chiave_ignota_403(self):
        # unknown key: 403 on both methods (even with a valid token), and no row is created
        self.assertEqual(self.put(json.dumps(OK), TOKEN, f"{LIVE}/altro").status_code, 403)
        self.assertEqual(self.get(f"{LIVE}/altro").status_code, 403)

        async def conta():
            async with AsyncSessionLocal() as db:
                return (await db.execute(select(func.count()).select_from(LiveSnapshot))).scalar_one()

        self.assertEqual(run(conta), 0)

    def test_live_scenari_put_poi_get(self):
        scenari = {"generato": "2026-10-26 15:32", "strumenti": {"MNQ": {"da_qui": {}}}}
        self.assertEqual(self.put(json.dumps(scenari), TOKEN, f"{LIVE}/scenari").status_code, 204)
        g = self.get(f"{LIVE}/scenari")
        self.assertEqual(g.status_code, 200)
        self.assertEqual(g.headers["cache-control"], "no-store")
        self.assertEqual(g.json()["dati"], scenari)
        self.assertIsNone(self.get(f"{LIVE}/frequenze").json()["dati"])  # keys are independent
        self.assertIsNone(self.get().json()["dati"])
        self.assertEqual(self.put(json.dumps(OK), None, f"{LIVE}/scenari").status_code, 401)  # same token rules

    def test_live_memoria_put_poi_get(self):
        memoria = json.loads(MEMORIA_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(self.put(json.dumps(memoria), TOKEN, f"{LIVE}/memoria").status_code, 204)
        g = self.get(f"{LIVE}/memoria")
        self.assertEqual(g.status_code, 200)
        self.assertEqual(g.headers["cache-control"], "no-store")
        corpo = g.json()
        self.assertEqual(corpo["dati"], memoria)
        self.assertGreaterEqual(corpo["eta_s"], 0)
        self.assertEqual(self.put(json.dumps(memoria), None, f"{LIVE}/memoria").status_code, 401)  # same token rules

    def test_live_x_ancora_403(self):
        self.assertEqual(self.put(json.dumps(OK), TOKEN, f"{LIVE}/x").status_code, 403)
        self.assertEqual(self.get(f"{LIVE}/x").status_code, 403)

    def test_live_memoria_corpo_senza_generato_422(self):
        for corpo in (b"[]", json.dumps({}), json.dumps({"generato": 1}), json.dumps({"stato": {}, "verdetti": {}})):
            with self.subTest(corpo=corpo):
                self.assertEqual(self.put(corpo, TOKEN, f"{LIVE}/memoria").status_code, 422)
        self.assertIsNone(self.get(f"{LIVE}/memoria").json()["dati"])  # nothing stored by the refused PUTs

    def test_memoria_e_frequenze_sono_righe_distinte(self):
        memoria = json.loads(MEMORIA_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(self.put(json.dumps(OK), TOKEN, f"{LIVE}/frequenze").status_code, 204)
        self.assertEqual(self.put(json.dumps(memoria), TOKEN, f"{LIVE}/memoria").status_code, 204)
        self.assertEqual(self.get(f"{LIVE}/frequenze").json()["dati"], OK)
        self.assertEqual(self.get(f"{LIVE}/memoria").json()["dati"], memoria)

        async def conta():
            async with AsyncSessionLocal() as db:
                return (await db.execute(select(func.count()).select_from(LiveSnapshot))).scalar_one()

        self.assertEqual(run(conta), 2)

    def test_alias_frequenze_equivale(self):
        self.assertEqual(self.put(json.dumps(OK), TOKEN).status_code, 204)  # alias -> live/frequenze
        self.assertEqual(self.get(f"{LIVE}/frequenze").json()["dati"], OK)
        altro = {"generato": "2026-10-26 15:33", "strumenti": {"MES": {}}}
        self.assertEqual(self.put(json.dumps(altro), TOKEN, f"{LIVE}/frequenze").status_code, 204)  # live/frequenze -> alias
        self.assertEqual(self.get().json()["dati"], altro)

        async def conta():
            async with AsyncSessionLocal() as db:
                return (await db.execute(select(func.count()).select_from(LiveSnapshot))).scalar_one()

        self.assertEqual(run(conta), 1)  # same storage row

    def test_limite_due_mib(self):
        base = len(json.dumps({"generato": "x", "strumenti": {"MNQ": ""}}))

        def corpo_di(n: int) -> str:
            return json.dumps({"generato": "x", "strumenti": {"MNQ": "x" * (n - base)}})

        self.assertEqual(len(corpo_di(2_097_153)), 2_097_153)
        self.assertEqual(self.put(corpo_di(2_097_153), TOKEN).status_code, 413)
        self.assertIsNone(self.get().json()["dati"])
        self.assertEqual(self.put(corpo_di(1_200_000), TOKEN).status_code, 204)
        self.assertEqual(self.put(corpo_di(2_097_152), TOKEN, f"{LIVE}/scenari").status_code, 204)  # exactly at the limit

    def test_get_gzip(self):
        grande = {"generato": "x", "strumenti": {"MNQ": {"nota": "abc" * 2000}}}
        self.assertEqual(self.put(json.dumps(grande), TOKEN).status_code, 204)
        g = self.get(headers={"Accept-Encoding": "gzip"})
        self.assertEqual(g.headers["content-encoding"], "gzip")
        self.assertEqual(g.json()["dati"], grande)
        self.assertEqual(g.headers["cache-control"], "no-store")

    # --- conditional requests (ETag / If-None-Match) ---

    def etag_di(self, chiave: str) -> str:
        return f'W/"{chiave}-{self.get(f"{LIVE}/{chiave}").json()["ricevuto"]}"'

    def test_etag_su_200(self):
        self.put(json.dumps(OK), TOKEN)
        g = self.get(f"{LIVE}/frequenze")
        self.assertEqual(g.status_code, 200)
        self.assertEqual(g.headers["etag"], f'W/"frequenze-{g.json()["ricevuto"]}"')
        self.assertEqual(g.headers["cache-control"], "no-store")
        self.assertEqual(set(g.json()), {"ricevuto", "eta_s", "dati"})

    def test_if_none_match_uguale_304(self):
        self.put(json.dumps(OK), TOKEN)
        etag = self.etag_di("frequenze")
        for valore in (etag, f'"altro", {etag}'):
            with self.subTest(valore=valore):
                g = self.get(f"{LIVE}/frequenze", {"If-None-Match": valore})
                self.assertEqual(g.status_code, 304)
                self.assertEqual(g.content, b"")
                self.assertNotIn("content-length", g.headers)
                self.assertEqual(g.headers["etag"], etag)
                self.assertEqual(g.headers["cache-control"], "no-store")

    def test_if_none_match_diverso_o_asterisco_200(self):
        self.put(json.dumps(OK), TOKEN)
        for valore in ('W/"frequenze-1999-01-01T00:00:00Z"', "*", ""):
            with self.subTest(valore=valore):
                g = self.get(f"{LIVE}/frequenze", {"If-None-Match": valore})
                self.assertEqual(g.status_code, 200)
                self.assertEqual(g.json()["dati"], OK)
                self.assertIn("etag", g.headers)

    def test_etag_cambia_dopo_nuovo_put(self):
        self.put(json.dumps(OK), TOKEN)
        vecchio = self.etag_di("frequenze")
        altro = {"generato": "2026-10-26 15:40", "strumenti": {"MES": {}}}
        with unittest.mock.patch("app.api.v1.frequenze.adesso_iso", return_value="2099-01-01T00:00:00Z"):  # a later second, no sleep
            self.put(json.dumps(altro), TOKEN)
        g = self.get(f"{LIVE}/frequenze", {"If-None-Match": vecchio})
        self.assertEqual(g.status_code, 200)
        self.assertNotEqual(g.headers["etag"], vecchio)
        self.assertEqual(g.json()["dati"], altro)
        self.assertEqual(self.get(f"{LIVE}/frequenze", {"If-None-Match": g.headers["etag"]}).status_code, 304)

    def test_canale_vuoto_etag_vuoto_e_304(self):
        for chiave in CHIAVI:
            with self.subTest(chiave=chiave):
                g = self.get(f"{LIVE}/{chiave}")
                self.assertEqual(g.status_code, 200)
                self.assertEqual(g.headers["etag"], f'W/"{chiave}-vuoto"')
                c = self.get(f"{LIVE}/{chiave}", {"If-None-Match": f'W/"{chiave}-vuoto"'})
                self.assertEqual(c.status_code, 304)
                self.assertEqual(c.content, b"")
                self.assertEqual(c.headers["cache-control"], "no-store")
        self.assertEqual(self.get(f"{LIVE}/memoria", {"If-None-Match": '*'}).status_code, 200)

    def test_etag_esposto_al_browser_cross_origin(self):
        # the web app runs on another origin: without Access-Control-Expose-Headers the browser hides ETag from fetch()
        self.put(json.dumps(OK), TOKEN)
        origine = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")[0].strip()
        for intestazioni, atteso in (({"Origin": origine}, 200), ({"Origin": origine, "If-None-Match": self.etag_di("frequenze")}, 304)):
            with self.subTest(atteso=atteso):
                g = self.get(f"{LIVE}/frequenze", intestazioni)
                self.assertEqual(g.status_code, atteso)
                self.assertIn("etag", g.headers.get("access-control-expose-headers", "").lower())

    def test_alias_frequenze_etag_come_live(self):
        self.assertEqual(self.get().headers["etag"], 'W/"frequenze-vuoto"')
        self.put(json.dumps(OK), TOKEN)
        etag = self.etag_di("frequenze")
        a = self.get("/api/v1/frequenze")
        self.assertEqual(a.headers["etag"], etag)
        self.assertEqual(self.get("/api/v1/frequenze", {"If-None-Match": etag}).status_code, 304)
        self.assertEqual(self.get("/api/v1/frequenze", {"If-None-Match": "*"}).status_code, 200)
        # an ETag of another channel never matches
        self.assertEqual(self.get("/api/v1/frequenze", {"If-None-Match": 'W/"scenari-vuoto"'}).status_code, 200)

    def test_get_senza_if_none_match_invariato(self):
        self.put(json.dumps(OK), TOKEN)
        g = self.get(f"{LIVE}/frequenze")
        self.assertEqual(g.status_code, 200)
        self.assertEqual(g.json()["dati"], OK)

    def test_eta_mai_negativa(self):
        adesso = datetime.now(timezone.utc)
        self.assertEqual(eta_secondi("2099-01-01T00:00:00Z", adesso), 0)


if __name__ == "__main__":
    unittest.main()
