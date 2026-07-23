"""Newsletter models: Subscriber, Campaign, Send tracking."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class NewsletterSubscriber(Base):
    """A newsletter subscriber with double opt-in verification."""

    __tablename__ = "newsletter_subscribers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    verification_token: Mapped[str | None] = mapped_column(
        String(128), nullable=True, unique=True
    )
    unsubscribed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    subscribed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    sends: Mapped[list["NewsletterSend"]] = relationship(
        "NewsletterSend", back_populates="subscriber", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<NewsletterSubscriber {self.email} verified={self.verified}>"


class NewsletterCampaign(Base):
    """A newsletter email campaign."""

    __tablename__ = "newsletter_campaigns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    subject: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    content_html: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    content_text: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(30), default="bozza", nullable=False, index=True
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
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
    sends: Mapped[list["NewsletterSend"]] = relationship(
        "NewsletterSend", back_populates="campaign", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<NewsletterCampaign {self.subject} [{self.status}]>"


class NewsletterSend(Base):
    """Tracks the delivery of a campaign to a specific subscriber."""

    __tablename__ = "newsletter_sends"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("newsletter_campaigns.id", ondelete="CASCADE"),
        nullable=False,
    )
    subscriber_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("newsletter_subscribers.id", ondelete="CASCADE"),
        nullable=False,
    )
    sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    opened_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    campaign: Mapped["NewsletterCampaign"] = relationship(
        "NewsletterCampaign", back_populates="sends"
    )
    subscriber: Mapped["NewsletterSubscriber"] = relationship(
        "NewsletterSubscriber", back_populates="sends"
    )

    __table_args__ = (
        UniqueConstraint("campaign_id", "subscriber_id", name="uq_campaign_subscriber"),
    )

    def __repr__(self) -> str:
        return f"<NewsletterSend campaign={self.campaign_id} sub={self.subscriber_id}>"
