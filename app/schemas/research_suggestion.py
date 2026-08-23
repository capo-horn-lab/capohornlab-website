"""ResearchSuggestion Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ResearchSuggestionCreate(BaseModel):
    research_slug: str = Field(..., min_length=1, max_length=100)
    author_name: str = Field(..., min_length=1, max_length=100)
    author_email: Optional[str] = Field(None, max_length=255)
    author_link: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=10, max_length=5000)


class ResearchSuggestionAdminUpdate(BaseModel):
    status: str = Field(..., pattern="^(accepted|rejected)$")
    admin_note: Optional[str] = Field(None, max_length=1000)
    generate_discount: bool = Field(False)


class ResearchSuggestionResponse(BaseModel):
    id: UUID
    research_slug: str
    author_name: str
    author_email: Optional[str] = None
    author_link: Optional[str] = None
    content: str
    status: str
    admin_note: Optional[str] = None
    discount_code: Optional[str] = None
    accepted_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ResearchSuggestionListResponse(BaseModel):
    items: list[ResearchSuggestionResponse]
    total: int
    page: int = 1
    per_page: int = 20


class ResearchSuggestionAcceptResponse(BaseModel):
    message: str
    suggestion_id: UUID
    status: str
    discount_code: Optional[str] = None