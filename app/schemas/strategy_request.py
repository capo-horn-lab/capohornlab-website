"""StrategyRequest Pydantic schemas — request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Status Constants ──

REQUEST_STATUSES = [
    "inviata",
    "info_mancanti",
    "in_valutazione",
    "accettata",
    "rifiutata",
    "in_lavorazione",
    "completata",
]


# ── Request Schemas ──


class StrategyRequestCreate(BaseModel):
    """Schema for creating a new strategy request."""
    strategy_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    instrument: str = Field(..., min_length=1, max_length=50)
    timeframe: Optional[str] = Field(None, max_length=30)
    historical_period: Optional[str] = Field(None, max_length=100)
    session_times: Optional[str] = Field(None, max_length=200)
    entry_rules_long: Optional[str] = None
    entry_rules_short: Optional[str] = None
    exit_rules: Optional[str] = None
    stop_loss: Optional[str] = Field(None, max_length=100)
    take_profit: Optional[str] = Field(None, max_length=100)
    trailing_stop: Optional[str] = Field(None, max_length=100)
    break_even: Optional[str] = Field(None, max_length=100)
    indicators_params: Optional[dict[str, Any]] = None
    contracts: Optional[int] = None
    commission_slippage: Optional[str] = None
    additional_notes: Optional[str] = None


class StrategyRequestUpdate(BaseModel):
    """Schema for updating own request (only when status is inviata/info_mancanti)."""
    strategy_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    instrument: Optional[str] = Field(None, min_length=1, max_length=50)
    timeframe: Optional[str] = Field(None, max_length=30)
    historical_period: Optional[str] = Field(None, max_length=100)
    session_times: Optional[str] = Field(None, max_length=200)
    entry_rules_long: Optional[str] = None
    entry_rules_short: Optional[str] = None
    exit_rules: Optional[str] = None
    stop_loss: Optional[str] = Field(None, max_length=100)
    take_profit: Optional[str] = Field(None, max_length=100)
    trailing_stop: Optional[str] = Field(None, max_length=100)
    break_even: Optional[str] = Field(None, max_length=100)
    indicators_params: Optional[dict[str, Any]] = None
    contracts: Optional[int] = None
    commission_slippage: Optional[str] = None
    additional_notes: Optional[str] = None


class AdminStatusUpdate(BaseModel):
    """Schema for admin status change."""
    status: str = Field(..., pattern="|".join(REQUEST_STATUSES))
    note: Optional[str] = None


class AdminClarifyRequest(BaseModel):
    """Schema for admin requesting clarifications from client."""
    message: str = Field(..., min_length=1)


class InternalNoteCreate(BaseModel):
    """Schema for creating an internal note."""
    content: str = Field(..., min_length=1)


# ── Response Schemas ──


class StatusHistoryResponse(BaseModel):
    id: UUID
    request_id: UUID
    from_status: Optional[str] = None
    to_status: str
    changed_by: Optional[UUID] = None
    note: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AttachmentResponse(BaseModel):
    id: UUID
    request_id: UUID
    file_name: str
    original_name: str
    mime_type: str
    file_size: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class InternalNoteResponse(BaseModel):
    id: UUID
    request_id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StrategyRequestResponse(BaseModel):
    """Full response schema for a strategy request."""
    id: UUID
    user_id: UUID
    status: str
    strategy_name: str
    description: Optional[str] = None
    instrument: str
    timeframe: Optional[str] = None
    historical_period: Optional[str] = None
    session_times: Optional[str] = None
    entry_rules_long: Optional[str] = None
    entry_rules_short: Optional[str] = None
    exit_rules: Optional[str] = None
    stop_loss: Optional[str] = None
    take_profit: Optional[str] = None
    trailing_stop: Optional[str] = None
    break_even: Optional[str] = None
    indicators_params: Optional[dict] = None
    contracts: Optional[int] = None
    commission_slippage: Optional[str] = None
    additional_notes: Optional[str] = None
    admin_notes: Optional[str] = None
    clarification_request: Optional[str] = None
    submitted_at: datetime
    evaluated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StrategyRequestDetailResponse(StrategyRequestResponse):
    """Detailed response with related data."""
    status_history: List[StatusHistoryResponse] = Field(default_factory=list)
    attachments: List[AttachmentResponse] = Field(default_factory=list)
    internal_notes: List[InternalNoteResponse] = Field(default_factory=list)


class StrategyRequestListResponse(BaseModel):
    """Paginated list response."""
    items: List[StrategyRequestResponse]
    total: int
    page: int = 1
    per_page: int = 20


# ── Utility Schemas ──


class ClarifyResponse(BaseModel):
    message: str
    clarification_request: str
