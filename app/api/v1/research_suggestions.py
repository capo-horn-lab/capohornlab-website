"""Research suggestions API — public submission + admin moderation."""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.models.research_suggestion import ResearchSuggestion
from app.models.user import User
from app.schemas.research_suggestion import (
    ResearchSuggestionAcceptResponse,
    ResearchSuggestionAdminUpdate,
    ResearchSuggestionCreate,
    ResearchSuggestionListResponse,
    ResearchSuggestionResponse,
)
from app.services.auth import check_rate_limit, get_current_user

router = APIRouter(prefix="/research/suggestions", tags=["research-suggestions"])

_TAG_RE = re.compile(r'<[^>]*>')
_ALLOWED_SLUGS = {
    "es-1m-quant-summary", "when-structure-meets-reality",
    "time-series-momentum-futures", "opening-range-breakout-intraday",
    "vwap-mean-reversion-intraday", "intraday-momentum-spy",
    "cwmr-confidence-weighted-mean-reversion",
    "pamr-passive-aggressive-mean-reversion",
    "ftrl-follow-the-regularized-leader",
    "market-cycle-analysis", "volatility-risk-premium-vix",
    "trend-following-concretum-replication",
    "5m-mean-reversion-alpha-overlay", "news-trading-longhorizon-es",
}

def _sanitize(s: str) -> str:
    if not s: return s
    return _TAG_RE.sub('', s).strip()


@router.post("", response_model=ResearchSuggestionResponse, status_code=201)
async def submit_suggestion(
    body: ResearchSuggestionCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    """Submit a suggestion for a published research study. Rate limited: 3/hour per IP."""
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"suggestion:{ip}", max_requests=3)

    if body.research_slug not in _ALLOWED_SLUGS:
        raise HTTPException(status_code=404, detail="Research study not found")

    suggestion = ResearchSuggestion(
        research_slug=body.research_slug,
        author_name=_sanitize(body.author_name),
        author_email=body.author_email,
        author_link=body.author_link,
        content=_sanitize(body.content),
    )
    db.add(suggestion)
    await db.commit()
    await db.refresh(suggestion)
    return suggestion


# ── Admin endpoints ──

admin_router = APIRouter(prefix="/admin/research/suggestions", tags=["admin-suggestions"])


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@admin_router.get("", response_model=ResearchSuggestionListResponse)
async def admin_list_suggestions(
    research_slug: str | None = None,
    status_filter: str | None = Query(None, alias="status"),
    page: int = 1,
    per_page: int = 50,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """List research suggestions with filters (admin only)."""
    count_stmt = select(sa_func.count()).select_from(ResearchSuggestion)
    list_stmt = select(ResearchSuggestion).order_by(ResearchSuggestion.created_at.desc())

    if research_slug:
        count_stmt = count_stmt.where(ResearchSuggestion.research_slug == research_slug)
        list_stmt = list_stmt.where(ResearchSuggestion.research_slug == research_slug)
    if status_filter:
        count_stmt = count_stmt.where(ResearchSuggestion.status == status_filter)
        list_stmt = list_stmt.where(ResearchSuggestion.status == status_filter)

    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    offset = (page - 1) * per_page
    list_stmt = list_stmt.offset(offset).limit(per_page)
    result = await db.execute(list_stmt)
    items = list(result.scalars().all())

    return ResearchSuggestionListResponse(
        items=[ResearchSuggestionResponse.model_validate(r) for r in items],
        total=total, page=page, per_page=per_page,
    )


@admin_router.patch("/{suggestion_id}", response_model=ResearchSuggestionAcceptResponse)
async def admin_update_suggestion(
    suggestion_id: uuid.UUID,
    body: ResearchSuggestionAdminUpdate,
    db: AsyncSession = Depends(get_async_db),
    admin: User = Depends(require_admin),
):
    """Accept or reject a suggestion. On accept, optionally generate a discount code."""
    stmt = select(ResearchSuggestion).where(ResearchSuggestion.id == suggestion_id)
    result = await db.execute(stmt)
    sug = result.scalar_one_or_none()

    if not sug:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    sug.status = body.status
    sug.admin_note = body.admin_note

    discount_code = None
    if body.status == "accepted":
        sug.accepted_at = datetime.now(timezone.utc)
        if body.generate_discount:
            code = f"RESEARCH{uuid.uuid4().hex[:8].upper()}"
            discount_code = code
            # Note: discount code generation handled client-side via admin panel
            # for full integration with the existing discount system

    await db.commit()
    await db.refresh(sug)

    return ResearchSuggestionAcceptResponse(
        message=f"Suggestion {body.status}",
        suggestion_id=sug.id,
        status=body.status,
        discount_code=discount_code,
    )