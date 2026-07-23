"""Attachment model — files uploaded for a strategy request."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("strategy_requests.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="UUID-based storage filename"
    )
    original_name: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Original uploaded filename"
    )
    mime_type: Mapped[str] = mapped_column(
        String(100), nullable=False,
        comment="Detected MIME type"
    )
    file_size: Mapped[int] = mapped_column(
        BigInteger, nullable=False,
        comment="File size in bytes"
    )
    storage_path: Mapped[str] = mapped_column(
        String(500), nullable=False,
        comment="Path on disk or S3 key"
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    request: Mapped["StrategyRequest"] = relationship(
        "StrategyRequest", back_populates="attachments"
    )

    def __repr__(self) -> str:
        return (
            f"<Attachment {self.id} {self.original_name} "
            f"({self.file_size} bytes)>"
        )
