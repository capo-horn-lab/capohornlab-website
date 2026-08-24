"""Payment and order schemas."""
from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# ── Payment Method ──

class SetupCardRequest(BaseModel):
    """Stripe card element token to attach as payment method."""
    payment_method_id: str = Field(..., min_length=1, description="Stripe PaymentMethod ID from Elements")


class CardResponse(BaseModel):
    id: UUID
    card_brand: str
    card_last4: str
    card_exp_month: int
    card_exp_year: int
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Order / Purchase ──

class CreateOrderRequest(BaseModel):
    product_slug: str = Field(..., min_length=1, max_length=100)
    product_name: str = Field(..., min_length=1, max_length=255)
    product_type: str = Field(..., pattern=r"^(data_pack|backtest|subscription)$")
    amount: float = Field(..., gt=0)


class OrderResponse(BaseModel):
    id: UUID
    product_slug: str
    product_name: str
    product_type: str
    amount: float
    currency: str
    status: str
    stripe_payment_intent_id: str | None = None
    created_at: datetime
    paid_at: datetime | None = None

    model_config = {"from_attributes": True}


# ── Dashboard summary ──

class PurchaseItem(BaseModel):
    """A purchased data pack or backtest the user owns."""
    order_id: UUID
    product_slug: str
    product_name: str
    product_type: str
    amount: float
    currency: str
    purchased_at: datetime


class UserPurchases(BaseModel):
    cards: list[CardResponse]
    purchases: list[PurchaseItem]