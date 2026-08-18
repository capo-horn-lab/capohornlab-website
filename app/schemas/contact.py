"""Public contact form schemas."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr
    subject: str = Field(..., min_length=1, max_length=255)
    message: str = Field(..., min_length=10, max_length=10000)
    website: str | None = Field(default=None, max_length=200)


class ContactMessageResponse(BaseModel):
    message: str
