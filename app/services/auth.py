"""Auth service: business logic for signup, login, token management."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_db
from app.core.redis import get_redis
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.models.login_history import LoginHistory
from app.models.user import User
from app.core.config import settings

security_scheme = HTTPBearer(auto_error=False)

# ── In-memory verification codes (replace with DB/Redis in production) ──
# Structure: {email: {"code": "123456", "expires_at": datetime}}
_verification_codes: Dict[str, Dict] = {}
_reset_codes: Dict[str, Dict] = {}


# ── Signup ──


async def signup_user(
    db: AsyncSession,
    email: str,
    password: str,
    name: str,
) -> User:
    """Create a new user account."""
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=email,
        password_hash=hash_password(password),
        name=name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# ── Login ──


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
    request: Request,
) -> Tuple[User, str, str]:
    """Authenticate user and return (user, access_token, refresh_token)."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    # Get IP and User-Agent
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", None)

    if not user or not verify_password(password, user.password_hash):
        # Log failed attempt
        if user:
            log_attempt = LoginHistory(
                user_id=user.id,
                ip=ip,
                user_agent=user_agent,
                success=False,
            )
            db.add(log_attempt)
            await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Log successful login
    log_attempt = LoginHistory(
        user_id=user.id,
        ip=ip,
        user_agent=user_agent,
        success=True,
    )
    db.add(log_attempt)
    await db.commit()

    # Generate tokens
    access_token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return user, access_token, refresh_token


# ── Token Refresh ──


async def refresh_tokens(
    db: AsyncSession,
    refresh_token: str,
) -> Tuple[User, str, str]:
    """Validate refresh token and issue new token pair."""
    payload = decode_refresh_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Issue new token pair (rotation)
    new_access = create_access_token({"sub": str(user.id), "role": user.role})
    new_refresh = create_refresh_token({"sub": str(user.id)})

    return user, new_access, new_refresh


# ── Email Verification ──


async def send_verification_code(email: str) -> str:
    """Generate and store a 6-digit verification code."""
    code = f"{secrets.randbelow(1000000):06d}"
    _verification_codes[email] = {
        "code": code,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    # TODO: Send email via Resend/SendGrid
    return code


async def verify_email_code(email: str, code: str) -> bool:
    """Verify a 6-digit code sent to the user's email."""
    stored = _verification_codes.get(email)
    if not stored:
        return False
    if stored["code"] != code:
        return False
    if datetime.now(timezone.utc) > stored["expires_at"]:
        return False
    del _verification_codes[email]
    return True


async def mark_user_verified(db: AsyncSession, email: str) -> User:
    """Mark a user's email as verified."""
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    user.verified = True
    await db.commit()
    await db.refresh(user)
    return user


# ── Password Reset ──


async def send_reset_code(email: str) -> str:
    """Generate and store a password reset code."""
    code = f"{secrets.randbelow(1000000):06d}"
    _reset_codes[email] = {
        "code": code,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    # TODO: Send email via Resend/SendGrid
    return code


async def reset_password(
    db: AsyncSession,
    email: str,
    code: str,
    new_password: str,
) -> User:
    """Verify reset code and update password."""
    stored = _reset_codes.get(email)
    if not stored:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No reset code requested for this email",
        )
    if stored["code"] != code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code",
        )
    if datetime.now(timezone.utc) > stored["expires_at"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset code expired",
        )

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.password_hash = hash_password(new_password)
    await db.commit()
    await db.refresh(user)
    del _reset_codes[email]
    return user


# ── Rate Limiting ──


async def check_rate_limit(
    key: str,
    max_requests: int = 0,
    window_seconds: int = 60,
) -> None:
    """Check rate limit using Redis sliding window.

    Raises HTTP 429 if limit exceeded.
    """
    if max_requests <= 0:
        max_requests = settings.RATE_LIMIT_PER_MINUTE

    redis = await get_redis()
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window_seconds)

    if current > max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )


# ── Current User Dependency ──


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: AsyncSession = Depends(get_async_db),
) -> User:
    """Dependency: extract and validate the current user from the Bearer token."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
