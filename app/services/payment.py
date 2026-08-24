"""Stripe payment service — card storage and charges."""
from __future__ import annotations

from typing import Optional
from uuid import UUID

import stripe
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.payment import PaymentMethod
from app.models.order import Order
from app.models.user import User


def _stripe() -> stripe:
    if not settings.STRIPE_SECRET_KEY:
        raise RuntimeError("STRIPE_SECRET_KEY is not configured — payment features are unavailable.")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


async def get_or_create_stripe_customer(
    db: AsyncSession, user: User
) -> str:
    """Return the Stripe customer ID for `user`, creating one if necessary."""
    result = await db.execute(
        select(PaymentMethod).where(
            PaymentMethod.user_id == user.id,
            PaymentMethod.is_default == True,
        )
    )
    pm = result.scalar()
    if pm and pm.stripe_customer_id:
        return pm.stripe_customer_id

    # No existing payment method — create a fresh Stripe customer
    s = _stripe()
    customer = s.Customer.create(
        email=user.email,
        metadata={"user_id": str(user.id)},
    )
    return customer.id


async def save_card(
    db: AsyncSession,
    user: User,
    stripe_payment_method_id: str,
) -> PaymentMethod:
    """Attach a Stripe PaymentMethod to the user and persist it as the default card."""
    s = _stripe()
    customer_id = await get_or_create_stripe_customer(db, user)

    # Attach the PaymentMethod to the customer
    s.PaymentMethod.attach(stripe_payment_method_id, customer=customer_id)

    # Set as default
    s.Customer.modify(customer_id, invoice_settings={"default_payment_method": stripe_payment_method_id})

    # Retrieve card details
    pm_data = s.PaymentMethod.retrieve(stripe_payment_method_id)
    card = pm_data.card

    # Deactivate any existing default card
    existing = await db.execute(
        select(PaymentMethod).where(
            PaymentMethod.user_id == user.id,
            PaymentMethod.is_default == True,
        )
    )
    for old in existing.scalars().all():
        old.is_default = False

    new_card = PaymentMethod(
        user_id=user.id,
        stripe_customer_id=customer_id,
        stripe_payment_method_id=stripe_payment_method_id,
        card_brand=card.brand,
        card_last4=card.last4,
        card_exp_month=card.exp_month,
        card_exp_year=card.exp_year,
        is_default=True,
    )
    db.add(new_card)
    await db.flush()
    await db.refresh(new_card)
    return new_card


async def charge_for_order(
    db: AsyncSession,
    user: User,
    order: Order,
) -> Order:
    """Charge the user's default card for an order and update it."""
    s = _stripe()

    # Find default card
    result = await db.execute(
        select(PaymentMethod).where(
            PaymentMethod.user_id == user.id,
            PaymentMethod.is_default == True,
        )
    )
    card = result.scalar()
    if not card:
        raise ValueError("No payment method on file. Add a card first.")

    amount_cents = int(round(order.amount * 100))

    try:
        pi = s.PaymentIntent.create(
            amount=amount_cents,
            currency=order.currency.lower(),
            customer=card.stripe_customer_id,
            payment_method=card.stripe_payment_method_id,
            off_session=True,
            confirm=True,
            metadata={
                "order_id": str(order.id),
                "user_id": str(user.id),
                "product_slug": order.product_slug,
            },
        )
        order.stripe_payment_intent_id = pi.id

        if pi.status == "succeeded":
            order.status = "paid"
            from datetime import datetime, timezone
            order.paid_at = datetime.now(timezone.utc)
        else:
            order.status = "failed"

    except stripe.error.CardError as e:
        order.status = "failed"
        raise ValueError(f"Card declined: {e.error.message}") from e

    await db.flush()
    await db.refresh(order)
    return order


async def get_user_cards(
    db: AsyncSession, user: User
) -> list[PaymentMethod]:
    result = await db.execute(
        select(PaymentMethod)
        .where(PaymentMethod.user_id == user.id)
        .order_by(PaymentMethod.is_default.desc(), PaymentMethod.created_at.desc())
    )
    return list(result.scalars().all())


async def get_user_purchases(
    db: AsyncSession, user: User, paid_only: bool = True
) -> list[Order]:
    stmt = select(Order).where(Order.user_id == user.id)
    if paid_only:
        stmt = stmt.where(Order.status == "paid")
    result = await db.execute(stmt.order_by(Order.created_at.desc()))
    return list(result.scalars().all())


async def has_purchased(db: AsyncSession, user: User, product_slug: str) -> bool:
    """Check if the user has already paid for a specific product."""
    result = await db.execute(
        select(Order).where(
            Order.user_id == user.id,
            Order.product_slug == product_slug,
            Order.status == "paid",
        )
    )
    return result.scalar() is not None