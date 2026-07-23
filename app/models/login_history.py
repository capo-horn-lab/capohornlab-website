"""LoginHistory model — tracks every login attempt."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LoginHistory(Base):
    __tablename__ = "login_history"

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
    ip: Mapped[str] = mapped_column(
        String(45), nullable=True, comment="Client IP address"
    )
    user_agent: Mapped[str] = mapped_column(
        String(512), nullable=True, comment="Client User-Agent header"
    )
    success: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="login_history"
    )

    def __repr__(self) -> str:
        return (
            f"<LoginHistory {self.id} user={self.user_id} "
            f"success={self.success}>"
        )
