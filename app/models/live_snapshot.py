"""Latest live snapshot pushed by the trading engine (one row per key)."""
from __future__ import annotations

from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LiveSnapshot(Base):
    __tablename__ = "live_snapshots"

    chiave: Mapped[str] = mapped_column(String(32), primary_key=True)
    ricevuto: Mapped[str] = mapped_column(String(32), nullable=False)  # UTC, %Y-%m-%dT%H:%M:%SZ
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    byte: Mapped[int] = mapped_column(Integer, nullable=False)
