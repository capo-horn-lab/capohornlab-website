"""Strategy request API endpoints — user-facing CRUD."""

from __future__ import annotations

import os
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_async_db
from app.models.attachment import Attachment as AttachmentModel
from app.models.status_history import StatusHistory as StatusHistoryModel
from app.models.strategy_request import StrategyRequest
from app.models.user import User
from app.schemas.strategy_request import (
    AttachmentResponse,
    ClarifyResponse,
    StatusHistoryResponse,
    StrategyRequestCreate,
    StrategyRequestDetailResponse,
    StrategyRequestListResponse,
    StrategyRequestResponse,
    StrategyRequestUpdate,
)
from app.services.auth import get_current_user
from app.utils.file_upload import (
    MAX_FILE_SIZE,
    check_file_size,
    validate_uploaded_file,
)

router = APIRouter(prefix="/requests", tags=["requests"])


# ── Helper ──


async def _get_user_request(
    db: AsyncSession,
    request_id: UUID,
    user: User,
) -> StrategyRequest:
    """Fetch a request by ID, verifying ownership (admin can see all)."""
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)
    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    if req.user_id != user.id and user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this request",
        )

    return req


async def _build_storage_path(request_id: UUID) -> str:
    """Build the storage directory path for a request's attachments.
    
    Creates the directory if it doesn't exist.
    """
    base = settings.UPLOAD_DIR
    rel = os.path.join(str(request_id))
    full = os.path.join(base, rel)
    os.makedirs(full, exist_ok=True)
    return full


# ── Endpoints ──


@router.post("", response_model=StrategyRequestResponse, status_code=201)
async def create_request(
    body: StrategyRequestCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new strategy request (authenticated user)."""
    req = StrategyRequest(
        user_id=current_user.id,
        strategy_name=body.strategy_name,
        description=body.description,
        instrument=body.instrument,
        timeframe=body.timeframe,
        historical_period=body.historical_period,
        session_times=body.session_times,
        entry_rules_long=body.entry_rules_long,
        entry_rules_short=body.entry_rules_short,
        exit_rules=body.exit_rules,
        stop_loss=body.stop_loss,
        take_profit=body.take_profit,
        trailing_stop=body.trailing_stop,
        break_even=body.break_even,
        indicators_params=body.indicators_params,
        contracts=body.contracts,
        commission_slippage=body.commission_slippage,
        additional_notes=body.additional_notes,
    )
    db.add(req)
    await db.flush()

    # Record initial status in history
    history = StatusHistoryModel(
        request_id=req.id,
        from_status=None,
        to_status="inviata",
        changed_by=current_user.id,
        note="Richiesta creata",
    )
    db.add(history)
    await db.commit()
    await db.refresh(req)

    return req


@router.get("", response_model=StrategyRequestListResponse)
async def list_requests(
    page: int = 1,
    per_page: int = 20,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """List strategy requests for the current user (paginated)."""
    # Count total for user
    count_stmt = (
        select(sa_func.count())
        .select_from(StrategyRequest)
        .where(StrategyRequest.user_id == current_user.id)
    )
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0

    # Fetch page
    offset = (page - 1) * per_page
    stmt = (
        select(StrategyRequest)
        .where(StrategyRequest.user_id == current_user.id)
        .order_by(StrategyRequest.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    result = await db.execute(stmt)
    items = list(result.scalars().all())

    return StrategyRequestListResponse(
        items=[StrategyRequestResponse.model_validate(r) for r in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/{request_id}", response_model=StrategyRequestDetailResponse)
async def get_request(
    request_id: UUID,
    include_history: bool = True,
    include_attachments: bool = True,
    include_notes: bool = False,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Get detailed information about a strategy request.

    Regular users see only their own requests.
    Pass `include_notes=true` to include internal notes (admin-only filter applied).
    """
    # Build query with optional eager loads
    stmt = select(StrategyRequest).where(StrategyRequest.id == request_id)

    if include_history:
        stmt = stmt.options(selectinload(StrategyRequest.status_history))
    if include_attachments:
        stmt = stmt.options(selectinload(StrategyRequest.attachments))
    if include_notes and current_user.role == "admin":
        stmt = stmt.options(selectinload(StrategyRequest.internal_notes))

    result = await db.execute(stmt)
    req = result.scalar_one_or_none()

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found",
        )

    if req.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this request",
        )

    return req


@router.patch("/{request_id}", response_model=StrategyRequestResponse)
async def update_request(
    request_id: UUID,
    body: StrategyRequestUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Update a strategy request (only when status is inviata or info_mancanti)."""
    req = await _get_user_request(db, request_id, current_user)

    if req.status not in ("inviata", "info_mancanti"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update request with status '{req.status}'. "
            f"Only 'inviata' or 'info_mancanti' requests can be updated.",
        )

    # Apply only non-None fields
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(req, field, value)

    await db.commit()
    await db.refresh(req)
    return req


@router.delete("/{request_id}", status_code=204)
async def delete_request(
    request_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a strategy request (only when status is inviata)."""
    req = await _get_user_request(db, request_id, current_user)

    if req.status != "inviata":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete request with status '{req.status}'. "
            f"Only 'inviata' requests can be deleted.",
        )

    await db.delete(req)
    await db.commit()


# ── Attachments ──


@router.post("/{request_id}/attachments", response_model=AttachmentResponse, status_code=201)
async def upload_attachment(
    request_id: UUID,
    file: UploadFile,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Upload a file attachment for a strategy request.

    Validates extension, MIME type, and size (max 10 MB).
    Allowed extensions: pdf, png, jpg, jpeg, doc, docx, zip, py, txt, csv.
    """
    req = await _get_user_request(db, request_id, current_user)

    # Validate file
    storage_name = validate_uploaded_file(file)

    # Read content and check size
    content = await file.read()
    check_file_size(content)

    # Build storage path
    storage_dir = await _build_storage_path(request_id)
    storage_path = os.path.join(storage_dir, storage_name)

    # Write file to disk
    with open(storage_path, "wb") as f:
        f.write(content)

    # Create DB record
    attachment = AttachmentModel(
        request_id=req.id,
        file_name=storage_name,
        original_name=file.filename or storage_name,
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        storage_path=storage_path,
    )
    db.add(attachment)
    await db.commit()
    await db.refresh(attachment)

    return attachment


@router.delete(
    "/{request_id}/attachments/{attachment_id}",
    status_code=204,
)
async def delete_attachment(
    request_id: UUID,
    attachment_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an attachment from a strategy request."""
    req = await _get_user_request(db, request_id, current_user)

    stmt = select(AttachmentModel).where(
        AttachmentModel.id == attachment_id,
        AttachmentModel.request_id == req.id,
    )
    result = await db.execute(stmt)
    attachment = result.scalar_one_or_none()

    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found",
        )

    # Delete file from disk
    if os.path.exists(attachment.storage_path):
        os.remove(attachment.storage_path)

    await db.delete(attachment)
    await db.commit()


# ── Status History ──


@router.get("/{request_id}/history", response_model=list[StatusHistoryResponse])
async def get_status_history(
    request_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Get the full status change history for a strategy request."""
    req = await _get_user_request(db, request_id, current_user)

    stmt = (
        select(StatusHistoryModel)
        .where(StatusHistoryModel.request_id == req.id)
        .order_by(StatusHistoryModel.created_at.asc())
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())
