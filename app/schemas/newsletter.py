"""Newsletter Pydantic schemas — request/response models."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


# ── Request Schemas ──


class SubscribeRequest(BaseModel):
    """Subscribe a new email to the newsletter (double opt-in)."""

    email: EmailStr
    name: str | None = Field(None, max_length=150)


class UnsubscribeRequest(BaseModel):
    """One-click unsubscribe via token."""

    token: str = Field(..., min_length=1)


class CampaignCreate(BaseModel):
    """Create a new newsletter campaign (admin only)."""

    subject: str = Field(..., min_length=1, max_length=255)
    content_html: str = Field(..., min_length=1)
    content_text: str | None = None


class CampaignSendRequest(BaseModel):
    """Send a campaign (admin only)."""


# ── Response Schemas ──


class NewsletterSubscriberResponse(BaseModel):
    """Public subscriber data."""

    id: str
    email: str
    name: str | None
    verified: bool
    unsubscribed: bool
    subscribed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class NewsletterSubscriberListResponse(BaseModel):
    """Paginated list of subscribers."""

    items: list[NewsletterSubscriberResponse]
    total: int
    page: int = 1
    per_page: int = 20


class NewsletterCampaignResponse(BaseModel):
    """Public campaign data."""

    id: str
    subject: str
    content_html: str
    content_text: str | None
    status: str
    sent_at: datetime | None
    created_by: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class NewsletterCampaignListResponse(BaseModel):
    """Paginated list of campaigns."""

    items: list[NewsletterCampaignResponse]
    total: int
    page: int = 1
    per_page: int = 20


class NewsletterMessageResponse(BaseModel):
    """Generic newsletter message response."""

    message: str


class VerifyQuery(BaseModel):
    """Query parameter for email verification."""

    token: str = Field(..., min_length=1)
