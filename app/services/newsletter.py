"""Newsletter service — business logic for subscribe/verify/unsubscribe/send."""

from __future__ import annotations

import secrets
from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.newsletter import (
    NewsletterCampaign,
    NewsletterSend,
    NewsletterSubscriber,
)
from app.models.user import User
from app.services.email import email_service
from app.services.auth import check_rate_limit


def _generate_token(length: int = 64) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


# ── Subscribe (Double Opt-In) ──


async def subscribe_newsletter(
    db: AsyncSession,
    email: str,
    name: str | None = None,
) -> dict:
    """Subscribe an email with double opt-in.

    1. Check if already subscribed (verified) → 409
    2. Check if previously subscribed + unsubscribed → re-subscribe
    3. Otherwise create new subscriber with verification_token
    4. Send verification email
    """
    # Check existing subscriber
    result = await db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        if existing.verified and not existing.unsubscribed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already subscribed to the newsletter.",
            )
        # Re-subscribe if unsubscribed or not yet verified
        token = _generate_token()
        existing.verified = False
        existing.unsubscribed = False
        existing.verification_token = token
        if name:
            existing.name = name
        await db.commit()
        await db.refresh(existing)
        subscriber = existing
    else:
        # Create new subscriber
        token = _generate_token()
        subscriber = NewsletterSubscriber(
            email=email,
            name=name,
            verified=False,
            verification_token=token,
            unsubscribed=False,
        )
        db.add(subscriber)
        await db.commit()
        await db.refresh(subscriber)

    # Send verification email
    base_url = settings.FRONTEND_URL or "http://localhost:5173"
    verify_url = f"{base_url}/newsletter/verify?token={subscriber.verification_token}"
    await email_service.send_verification_email(
        to_email=subscriber.email,
        to_name=subscriber.name,
        verification_url=verify_url,
    )

    return {"message": "Verification email sent. Please check your inbox."}


# ── Verify Email (Double Opt-In confirmation) ──


async def verify_subscriber(db: AsyncSession, token: str) -> dict:
    """Verify a subscriber's email address using the verification token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token is required.",
        )

    result = await db.execute(
        select(NewsletterSubscriber).where(
            NewsletterSubscriber.verification_token == token
        )
    )
    subscriber = result.scalar_one_or_none()

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired verification token.",
        )

    if subscriber.verified:
        return {"message": "Email already verified."}

    subscriber.verified = True
    subscriber.verification_token = None  # Consume the token
    await db.commit()

    return {"message": "Email verified successfully. Welcome to the newsletter!"}


# ── Unsubscribe (One-click) ──


async def unsubscribe_subscriber(db: AsyncSession, email: str) -> dict:
    """Unsubscribe an email address from the newsletter."""
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required.",
        )

    result = await db.execute(
        select(NewsletterSubscriber).where(NewsletterSubscriber.email == email)
    )
    subscriber = result.scalar_one_or_none()

    if not subscriber:
        # Don't reveal whether the email was subscribed
        return {"message": "You have been unsubscribed."}

    subscriber.unsubscribed = True
    await db.commit()

    await email_service.send_unsubscribe_confirmation(
        to_email=subscriber.email,
        to_name=subscriber.name,
    )

    return {"message": "You have been unsubscribed."}


# ── Send Campaign (Admin only) ──


async def send_campaign(
    db: AsyncSession,
    campaign_id: UUID,
    admin: User,
) -> dict:
    """Send a newsletter campaign to all verified, non-unsubscribed subscribers.

    1. Load campaign (must be 'bozza')
    2. Load all active subscribers
    3. Create NewsletterSend records
    4. Simulate sending (stub: mark all as sent)
    5. Update campaign status to 'completata'
    """
    result = await db.execute(
        select(NewsletterCampaign).where(NewsletterCampaign.id == campaign_id)
    )
    campaign = result.scalar_one_or_none()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found.",
        )

    if campaign.status != "bozza":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot send campaign with status '{campaign.status}'. Only 'bozza' campaigns can be sent.",
        )

    # Get all verified, non-unsubscribed subscribers
    sub_result = await db.execute(
        select(NewsletterSubscriber).where(
            NewsletterSubscriber.verified == True,
            NewsletterSubscriber.unsubscribed == False,
        )
    )
    subscribers = list(sub_result.scalars().all())

    if not subscribers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active subscribers to send to.",
        )

    now = datetime.now(timezone.utc)
    unsubscribe_base = f"{settings.FRONTEND_URL or 'http://localhost:5173'}/newsletter/unsubscribe"

    # Create send records for each subscriber
    for sub in subscribers:
        send_record = NewsletterSend(
            campaign_id=campaign.id,
            subscriber_id=sub.id,
            sent_at=now,
        )
        db.add(send_record)

        # Stub: call email service
        unsubscribe_url = f"{unsubscribe_base}?email={sub.email}"
        await email_service.send_campaign_email(
            to_email=sub.email,
            to_name=sub.name,
            subject=campaign.subject,
            html_content=campaign.content_html,
            unsubscribe_url=unsubscribe_url,
        )

    # Update campaign
    campaign.status = "completata"
    campaign.sent_at = now
    await db.commit()

    return {
        "message": f"Campaign sent to {len(subscribers)} subscriber(s).",
        "subscribers_count": len(subscribers),
    }


# ── Create Campaign ──


async def create_campaign(
    db: AsyncSession,
    subject: str,
    content_html: str,
    content_text: str | None,
    admin: User,
) -> NewsletterCampaign:
    """Create a new campaign in 'bozza' status."""
    campaign = NewsletterCampaign(
        subject=subject,
        content_html=content_html,
        content_text=content_text,
        status="bozza",
        created_by=admin.id,
    )
    db.add(campaign)
    await db.commit()
    await db.refresh(campaign)
    return campaign


# ── List Subscribers (Admin) ──


async def list_subscribers(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20,
    verified_only: bool = False,
) -> dict:
    """List all newsletter subscribers with pagination."""
    count_stmt = select(sa_func.count()).select_from(NewsletterSubscriber)
    list_stmt = select(NewsletterSubscriber).order_by(
        NewsletterSubscriber.created_at.desc()
    )

    if verified_only:
        count_stmt = count_stmt.where(NewsletterSubscriber.verified == True)
        list_stmt = list_stmt.where(NewsletterSubscriber.verified == True)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    offset = (page - 1) * per_page
    list_stmt = list_stmt.offset(offset).limit(per_page)
    result = await db.execute(list_stmt)
    items = list(result.scalars().all())

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


# ── List Campaigns (Admin) ──


async def list_campaigns(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20,
) -> dict:
    """List all campaigns with pagination."""
    count_stmt = select(sa_func.count()).select_from(NewsletterCampaign)
    list_stmt = select(NewsletterCampaign).order_by(
        NewsletterCampaign.created_at.desc()
    )

    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    offset = (page - 1) * per_page
    list_stmt = list_stmt.offset(offset).limit(per_page)
    result = await db.execute(list_stmt)
    items = list(result.scalars().all())

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
    }
