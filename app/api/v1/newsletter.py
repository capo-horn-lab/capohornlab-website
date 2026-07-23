"""Newsletter API endpoints: subscribe, verify, unsubscribe."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.schemas.newsletter import (
    NewsletterMessageResponse,
    SubscribeRequest,
)
from app.services.newsletter import (
    subscribe_newsletter,
    unsubscribe_subscriber,
    verify_subscriber,
)

router = APIRouter(prefix="/newsletter", tags=["newsletter"])


@router.post(
    "/subscribe",
    response_model=NewsletterMessageResponse,
    status_code=201,
)
async def subscribe(
    body: SubscribeRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    """Subscribe an email to the newsletter with double opt-in.

    Sends a verification email to confirm the subscription.
    Rate limited: max 5 requests per minute per IP.
    """
    # Rate limit
    ip = request.client.host if request.client else "unknown"
    from app.services.auth import check_rate_limit

    await check_rate_limit(f"newsletter_subscribe:{ip}", max_requests=5)

    result = await subscribe_newsletter(
        db,
        email=body.email,
        name=body.name,
    )
    return NewsletterMessageResponse(message=result["message"])


@router.get("/verify", response_model=NewsletterMessageResponse)
async def verify(
    token: str = Query(..., description="Verification token from email"),
    db: AsyncSession = Depends(get_async_db),
):
    """Verify a subscriber's email address via token (double opt-in confirmation)."""
    result = await verify_subscriber(db, token=token)
    return NewsletterMessageResponse(message=result["message"])


@router.post("/unsubscribe", response_model=NewsletterMessageResponse)
async def unsubscribe(
    email: str = Query(..., description="Email to unsubscribe"),
    db: AsyncSession = Depends(get_async_db),
):
    """One-click unsubscribe from the newsletter."""
    result = await unsubscribe_subscriber(db, email=email)
    return NewsletterMessageResponse(message=result["message"])
