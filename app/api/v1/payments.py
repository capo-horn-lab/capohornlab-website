"""Payment and purchase API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.database import get_async_db
from app.models.user import User
from app.schemas.payment import (
    CardResponse,
    CreateOrderRequest,
    OrderResponse,
    PurchaseItem,
    SetupCardRequest,
    UserPurchases,
)
from app.services.payment import (
    charge_for_order,
    get_user_cards,
    get_user_purchases,
    has_purchased,
    save_card,
)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


@router.post("/setup-card", response_model=CardResponse, status_code=201)
async def setup_card(
    body: SetupCardRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Save a payment card for future purchases."""
    card = await save_card(db, current_user, body.payment_method_id)
    return card


@router.get("/cards", response_model=list[CardResponse])
async def list_cards(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Return the user's saved cards."""
    cards = await get_user_cards(db, current_user)
    return cards


@router.post("/buy", response_model=OrderResponse, status_code=201)
async def buy_product(
    body: CreateOrderRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Purchase a data pack or backtest and charge the saved card."""
    from app.models.order import Order

    # Prevent duplicate purchases (idempotent for already-paid items)
    if await has_purchased(db, current_user, body.product_slug):
        from fastapi import HTTPException
        raise HTTPException(409, "You already own this product.")

    order = Order(
        user_id=current_user.id,
        product_slug=body.product_slug,
        product_name=body.product_name,
        product_type=body.product_type,
        amount=body.amount,
        currency="EUR",
    )
    db.add(order)
    await db.flush()

    try:
        order = await charge_for_order(db, current_user, order)
    except ValueError as e:
        from fastapi import HTTPException
        raise HTTPException(402, str(e))

    return order


@router.get("/purchases", response_model=list[PurchaseItem])
async def list_purchases(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Return the user's purchased data packs and backtests."""
    orders = await get_user_purchases(db, current_user, paid_only=True)
    return [
        PurchaseItem(
            order_id=o.id,
            product_slug=o.product_slug,
            product_name=o.product_name,
            product_type=o.product_type,
            amount=o.amount,
            currency=o.currency,
            purchased_at=o.paid_at or o.created_at,
        )
        for o in orders
    ]


@router.get("/dashboard", response_model=UserPurchases)
async def payment_dashboard(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    """Full payment summary: cards + purchases."""
    cards = await get_user_cards(db, current_user)
    orders = await get_user_purchases(db, current_user, paid_only=True)
    return UserPurchases(
        cards=[CardResponse.model_validate(c) for c in cards],
        purchases=[
            PurchaseItem(
                order_id=o.id,
                product_slug=o.product_slug,
                product_name=o.product_name,
                product_type=o.product_type,
                amount=o.amount,
                currency=o.currency,
                purchased_at=o.paid_at or o.created_at,
            )
            for o in orders
        ],
    )