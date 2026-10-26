"""Live snapshots (``frequenze``, ``scenari``): the engine PUTs each every few seconds, the home page GETs them."""
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

router = APIRouter(prefix="/live", tags=["live"])
alias = APIRouter(prefix="/frequenze", tags=["live"])  # fase 1 URL, same storage row as /live/frequenze

CHIAVI = ("frequenze", "scenari")
MAX_BYTE = 2_097_152
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
    atteso = (settings.FREQ_PUBLISH_TOKEN or "").strip()
    if not atteso:
        raise HTTPException(status_code=503, detail="Publishing is not configured.")
    inviato = (request.headers.get("x-publish-token") or "").strip()
    if not inviato or not hmac.compare_digest(inviato.encode(), atteso.encode()):
        raise HTTPException(status_code=401, detail="Invalid publish token.")


def _verifica_chiave(chiave: str) -> None:
    if chiave not in CHIAVI:
        raise HTTPException(status_code=403, detail="Unknown snapshot key.")


async def _salva(chiave: str, request: Request, db: AsyncSession) -> Response:
    """Replace the snapshot stored under ``chiave``. Requires the ``X-Publish-Token`` header."""
    _verifica_chiave(chiave)
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

    riga = await db.get(LiveSnapshot, chiave)
    if riga is None:
        db.add(LiveSnapshot(chiave=chiave, ricevuto=adesso_iso(), payload=dati, byte=len(corpo)))
    else:
        riga.ricevuto, riga.payload, riga.byte = adesso_iso(), dati, len(corpo)
    await db.commit()
    return Response(status_code=204)


async def _leggi(chiave: str, db: AsyncSession) -> JSONResponse:
    """Public: latest snapshot under ``chiave`` with its age, or nulls when nothing was published yet."""
    _verifica_chiave(chiave)
    riga = await db.get(LiveSnapshot, chiave)
    if riga is None:
        risposta = {"ricevuto": None, "eta_s": None, "dati": None}
    else:
        risposta = {
            "ricevuto": riga.ricevuto,
            "eta_s": eta_secondi(riga.ricevuto, datetime.now(timezone.utc)),
            "dati": riga.payload,
        }
    return JSONResponse(risposta, headers={"Cache-Control": "no-store"})


@router.put("/{chiave}", status_code=204)
async def pubblica(chiave: str, request: Request, db: AsyncSession = Depends(get_async_db)) -> Response:
    return await _salva(chiave, request, db)


@router.get("/{chiave}")
async def leggi(chiave: str, db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    return await _leggi(chiave, db)


@alias.put("", status_code=204)
async def pubblica_frequenze(request: Request, db: AsyncSession = Depends(get_async_db)) -> Response:
    return await _salva("frequenze", request, db)


@alias.get("")
async def leggi_frequenze(db: AsyncSession = Depends(get_async_db)) -> JSONResponse:
    return await _leggi("frequenze", db)
