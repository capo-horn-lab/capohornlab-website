"""Public contact endpoint with persistence, rate limiting and email handoff."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.contact_message import ContactMessage
from app.schemas.contact import ContactMessageCreate, ContactMessageResponse
from app.services.auth import check_rate_limit
from app.services.email import email_service

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactMessageResponse, status_code=201)
async def create_contact_message(
    body: ContactMessageCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    """Store a support request and notify the configured mailbox.

    The honeypot is silently accepted to avoid teaching bots the detection rule.
    Email delivery is fail-closed when the transactional provider is not configured.
    """
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"contact:{ip}", max_requests=5)
    if body.website:
        return ContactMessageResponse(message="Message received.")

    record = ContactMessage(
        name=body.name.strip(),
        email=str(body.email),
        subject=body.subject.strip(),
        message=body.message.strip(),
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    delivered = await email_service.send_contact_notification(
        visitor_email=str(body.email),
        visitor_name=body.name.strip(),
        subject=body.subject.strip(),
        message=body.message.strip(),
    )
    if not delivered:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Message saved, but support email delivery is temporarily unavailable.",
        )
    await email_service.send_contact_acknowledgement(
        to_email=str(body.email),
        to_name=body.name.strip(),
        subject=body.subject.strip(),
    )
    return ContactMessageResponse(message="Message received. We will reply by email.")
