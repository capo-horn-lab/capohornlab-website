"""Live trading-frequency snapshot: the engine PUTs it every ~60 s, the home page GETs it."""
from __future__ import annotations

import hmac
import json
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_db
from app.models.live_snapshot import LiveSnapshot

router = APIRouter(prefix="/frequenze", tags=["frequenze"])

CHIAVE = "frequenze"
MAX_BYTE = 1_048_576
_FORMATO = "%Y-%m-%dT%H:%M:%SZ"


def adesso_iso() -> str:
    """Current UTC time as ``YYYY-MM-DDTHH:MM:SSZ``."""
    return datetime.now(timezone.utc).strftime(_FORMATO)


def eta_secondi(ricevuto: str, adesso: datetime) -> int:
    """Whole seconds elapsed since ``ricevuto``; never negative (clock skew clamps to 0)."""
    if adesso.tzinfo is None:
        adesso = adesso.replace(tzinfo=timezone.utc)
    quando = datetime.strptime(ricevuto, _FORMATO).replace(tzinfo=timezone.utc)
    return max(0, int((adesso - quando).total_seconds()))


def _verifica_token(request: Request) -> None:
    atteso = settings.FREQ_PUBLISH_TOKEN
    if not atteso:
        raise HTTPException(status_code=503, detail="Publishing is not configured.")
    inviato = request.headers.get("x-publish-token")
    if not inviato or not hmac.compare_digest(inviato.encode(), atteso.encode()):
        raise HTTPException(status_code=401, detail="Invalid publish token.")


@router.put("", status_code=204)
async def pubblica_frequenze(request: Request, db: AsyncSession = Depends(get_async_db)) -> Response:
    """Replace the single ``frequenze`` snapshot. Requires the ``X-Publish-Token`` header."""
    _verifica_token(request)
    corpo = await request.body()
    if len(corpo) > MAX_BYTE:
        raise HTTPException(status_code=413, detail="Payload too large.")
    try:
        dati = json.loads(corpo.decode("utf-8"))
        # Round-trip exactly as the public GET will render it: rejects NaN/Infinity (also via 1e999)
        # and lone surrogates, which would otherwise be stored and then fail every GET.
        json.dumps(dati, ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (UnicodeDecodeError, ValueError, RecursionError):
        raise HTTPException(status_code=422, detail="Body must be a UTF-8 JSON object.") from None
    if not (
        isinstance(dati, dict)
        and isinstance(dati.get("generato"), str)
        and isinstance(dati.get("strumenti"), dict)
    ):
        raise HTTPException(status_code=422, detail="Body needs 'generato' (string) and 'strumenti' (object).")

    riga = await db.get(LiveSnapshot, CHIAVE)
    if riga is None:
        db.add(LiveSnapshot(chiave=CHIAVE, ricevuto=adesso_iso(), payload=dati, byte=len(corpo)))
    else:
        riga.ricevuto, riga.payload, riga.byte = adesso_iso(), dati, len(corpo)
    await db.commit()
    return Response(status_code=204)


@router.get("")
async def leggi_frequenze(db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    """Public: latest snapshot with its age, or nulls when nothing was published yet."""
    riga = await db.get(LiveSnapshot, CHIAVE)
    if riga is None:
        risposta = {"ricevuto": None, "eta_s": None, "dati": None}
    else:
        risposta = {
            "ricevuto": riga.ricevuto,
            "eta_s": eta_secondi(riga.ricevuto, datetime.now(timezone.utc)),
            "dati": riga.payload,
        }
    return JSONResponse(risposta, headers={"Cache-Control": "no-store"})
