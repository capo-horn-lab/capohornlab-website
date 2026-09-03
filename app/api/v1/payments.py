"""Payment and purchase API endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_user
from app.core.config import settings
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


@router.post("/webhook", include_in_schema=True)
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_async_db)):
    """Verify and handle Stripe webhook events (signature-verified)."""
    import stripe as stripe_lib
    from datetime import datetime, timezone
    from sqlalchemy import select
    from uuid import UUID

    from app.models.order import Order

    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not settings.STRIPE_WEBHOOK_SECRET or not sig_header:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="Webhook not configured")

    try:
        event = stripe_lib.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (stripe_lib.error.SignatureVerificationError, ValueError) as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")

    event_type = event["type"]
    data = event["data"]["object"]
    metadata = data.get("metadata") or {}

    # One-time purchases are charged synchronously, but keep order status in
    # sync from async PaymentIntent events too (idempotent).
    if event_type in ("payment_intent.succeeded", "payment_intent.payment_failed"):
        order_id = metadata.get("order_id")
        if order_id:
            try:
                result = await db.execute(select(Order).where(Order.id == UUID(order_id)))
                order = result.scalar()
            except (ValueError, TypeError):
                order = None
            if order and order.status != "paid":
                order.status = "paid" if event_type.endswith("succeeded") else "failed"
                if event_type.endswith("succeeded"):
                    order.paid_at = datetime.now(timezone.utc)
                await db.commit()

    # checkout.session.completed / invoice.* / customer.subscription.* →
    # subscription lifecycle handled here when subscriptions are implemented.
    return {"received": True, "type": event_type}