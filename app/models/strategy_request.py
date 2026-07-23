"""StrategyRequest model — the core business entity."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StrategyRequest(Base):
    __tablename__ = "strategy_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        Enum(
            "inviata",
            "info_mancanti",
            "in_valutazione",
            "accettata",
            "rifiutata",
            "in_lavorazione",
            "completata",
            name="request_status",
        ),
        default="inviata",
        nullable=False,
        index=True,
    )

    # Strategy identity
    strategy_name: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # nome
    description: Mapped[str | None] = mapped_column(Text, nullable=True)  # descrizione
    instrument: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # strumento

    # Time settings
    timeframe: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )
    historical_period: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # periodo_start → end
    session_times: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )  # orari_sessione

    # Rules
    entry_rules_long: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # regole_entry_long
    entry_rules_short: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # regole_entry_short
    exit_rules: Mapped[str | None] = mapped_column(Text, nullable=True)  # regole_uscita
    stop_loss: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    take_profit: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    trailing_stop: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    break_even: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    # Parameters
    indicators_params: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True
    )  # indicatori_params JSONB
    contracts: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )  # num_contratti
    commission_slippage: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # commissioni + slippage
    additional_notes: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )  # note_aggiuntive

    # Admin fields
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    clarification_request: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    evaluated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="strategy_requests")  # type: ignore[name-defined]  # noqa: F821
    status_history: Mapped[list["StatusHistory"]] = relationship(
        "StatusHistory", back_populates="request", lazy="dynamic"
    )
    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment", back_populates="request", lazy="dynamic"
    )
    internal_notes: Mapped[list["InternalNote"]] = relationship(
        "InternalNote", back_populates="request", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return (
            f"<StrategyRequest {self.id} {self.strategy_name} "
            f"[{self.status}]>"
        )
