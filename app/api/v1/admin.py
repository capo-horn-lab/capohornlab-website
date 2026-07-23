"""Admin API endpoints — strategy request management, status changes, notes."""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.models.internal_note import InternalNote
from app.models.newsletter import NewsletterCampaign, NewsletterSubscriber
from app.models.status_history import StatusHistory
from app.models.strategy_request import StrategyRequest
from app.models.user import User
from app.schemas.newsletter import (
    CampaignCreate,
    NewsletterCampaignListResponse,
    NewsletterCampaignResponse,
    NewsletterMessageResponse,
    NewsletterSubscriberListResponse,
    NewsletterSubscriberResponse,
)
from app.schemas.strategy_request import (
    AdminClarifyRequest,
    AdminStatusUpdate,
    ClarifyResponse,
    InternalNoteCreate,
    InternalNoteResponse,
    StatusHistoryResponse,
    StrategyRequestDetailResponse,
    StrategyRequestListResponse,
    StrategyRequestResponse,
)
from app.services.auth import get_current_user
from app.services.newsletter import (
    create_campaign,
    list_campaigns,
    list_subscribers,
    send_campaign,
)

router = APIRouter(prefix="/admin", tags=["admin"])


# ── Admin Dependency ──


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """Dependency: ensure the current user has admin role."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# ── Requests List (Admin) ──


@router.get("/requests", response_model=StrategyRequestListResponse)
async def admin_list_requests(
    status_filter: Optional[str] = None,
    user_id: Optional[UUID] = None,
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """List ALL strategy requests with optional filters and pagination (admin only)."""
    # Build count query
    count_stmt = select(sa_func.count()).select_from(StrategyRequest)
    list_stmt = (
        select(StrategyRequest)
        .order_by(StrategyRequest.created_at.desc())
    )

    if status_filter:
        count_stmt = count_stmt.where(StrategyRequest.status == status_filter)
        list_stmt = list_stmt.where(StrategyRequest.status == status_filter)

    if user_id:
        count_stmt = count_stmt.where(StrategyRequest.user_id == user_id)
        list_stmt = list_stmt.where(StrategyRequest.user_id == user_id)

    # Count total
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # Fetch page
    offset = (page - 1) * per_page
    list_stmt = list_stmt.offset(offset).limit(per_page)
    result = await db.execute(list_stmt)
    items = list(result.scalars().all())

    return StrategyRequestListResponse(
        items=[StrategyRequestResponse.model_validate(r) for r in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/requests/{request_id}", response_model=StrategyRequestDetailResponse)
async def admin_get_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Get full request details including status history, attachments, and internal notes."""
    stmt = (
        select(StrategyRequest)
        .where(StrategyRequest.id == request_id)
        .options(
            selectinload(StrategyRequest.status_history),
            selectinload(StrategyRequest.attachments),
            selectinload(StrategyRequest.internal_notes),
        )
    )
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    return req


# ── Status Change ──


@router.patch("/requests/{request_id}/status", response_model=StrategyRequestResponse)
async def admin_change_status(
    request_id: UUID,
    body: AdminStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Change the status of a strategy request (admin only)."""
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    old_status = req.status
    req.status = body.status

    # Update evaluated_at when moving to in_valutazione
    if body.status == "in_valutazione" and req.evaluated_at is None:
        from datetime import datetime, timezone
        req.evaluated_at = datetime.now(timezone.utc)

    # Update completed_at when moving to completata
    if body.status == "completata" and req.completed_at is None:
        from datetime import datetime, timezone
        req.completed_at = datetime.now(timezone.utc)

    # Record status change in history
    history = StatusHistory(
        request_id=req.id,
        from_status=old_status,
        to_status=body.status,
        changed_by=admin.id,
        note=body.note,
    )
    db.add(history)
    await db.commit()
    await db.refresh(req)

    return req


# ── Internal Notes ──


@router.post(
    "/requests/{request_id}/notes",
    response_model=InternalNoteResponse,
    status_code=201,
)
async def admin_add_note(
    request_id: UUID,
    body: InternalNoteCreate,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Add an internal note to a strategy request (admin only)."""
    # Verify request exists
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    note = InternalNote(
        request_id=req.id,
        author_id=admin.id,
        content=body.content,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)

    return note


@router.get(
    "/requests/{request_id}/notes",
    response_model=list[InternalNoteResponse],
)
async def admin_list_notes(
    request_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """List all internal notes for a strategy request (admin only)."""
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    notes_stmt = (
        select(InternalNote)
        .where(InternalNote.request_id == req.id)
        .order_by(InternalNote.created_at.desc())
    )
    notes_result = await db.execute(notes_stmt)
    return list(notes_result.scalars().all())


# ── Clarify Request ──


@router.post(
    "/requests/{request_id}/clarify",
    response_model=ClarifyResponse,
)
async def admin_request_clarification(
    request_id: UUID,
    body: AdminClarifyRequest,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Request clarifications from the client (admin only).

    Sets the request status to 'info_mancanti' and stores
    the clarification request text.
    """
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    old_status = req.status
    req.status = "info_mancanti"
    req.clarification_request = body.message

    # Record status change
    history = StatusHistory(
        request_id=req.id,
        from_status=old_status,
        to_status="info_mancanti",
        changed_by=admin.id,
        note=f"Richiesta chiarimenti: {body.message[:200]}{'...' if len(body.message) > 200 else ''}",
    )
    db.add(history)
    await db.commit()
    await db.refresh(req)

    return ClarifyResponse(
        message="Clarification request sent to client",
        clarification_request=req.clarification_request,
    )


# ── Status History ──


@router.get(
    "/requests/{request_id}/history",
    response_model=list[StatusHistoryResponse],
)
async def admin_get_status_history(
    request_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Get the full status change history for a strategy request (admin)."""
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    hist_stmt = (
        select(StatusHistory)
        .where(StatusHistory.request_id == req.id)
        .order_by(StatusHistory.created_at.asc())
    )
    hist_result = await db.execute(hist_stmt)
    return list(hist_result.scalars().all())


# ── Newsletter Admin ──


@router.post(
    "/newsletter/send",
    response_model=NewsletterMessageResponse,
)
async def admin_send_newsletter_campaign(
    campaign_id: UUID = Query(..., description="Campaign ID to send"),
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Send a newsletter campaign to all active subscribers (admin only)."""
    result = await send_campaign(db, campaign_id=campaign_id, admin=admin)
    return NewsletterMessageResponse(message=result["message"])


@router.get(
    "/newsletter/subscribers",
    response_model=NewsletterSubscriberListResponse,
)
async def admin_list_newsletter_subscribers(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    verified_only: bool = Query(False),
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """List all newsletter subscribers with pagination (admin only)."""
    result = await list_subscribers(
        db,
        page=page,
        per_page=per_page,
        verified_only=verified_only,
    )
    return NewsletterSubscriberListResponse(
        items=[
            NewsletterSubscriberResponse.model_validate(s) for s in result["items"]
        ],
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
    )


@router.post(
    "/newsletter/campaigns",
    response_model=NewsletterCampaignResponse,
    status_code=201,
)
async def admin_create_newsletter_campaign(
    body: CampaignCreate,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Create a new newsletter campaign in 'bozza' status (admin only)."""
    campaign = await create_campaign(
        db,
        subject=body.subject,
        content_html=body.content_html,
        content_text=body.content_text,
        admin=admin,
    )
    return campaign


@router.get(
    "/newsletter/campaigns",
    response_model=NewsletterCampaignListResponse,
)
async def admin_list_newsletter_campaigns(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """List all newsletter campaigns with pagination (admin only)."""
    result = await list_campaigns(db, page=page, per_page=per_page)
    return NewsletterCampaignListResponse(
        items=[
            NewsletterCampaignResponse.model_validate(c) for c in result["items"]
        ],
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
    )
