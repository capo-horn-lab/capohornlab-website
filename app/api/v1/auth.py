"""Auth API endpoints: signup, login, refresh, verify, reset-password."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MessageResponse,
    ResetPasswordConfirmRequest,
    ResetPasswordRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
    VerifyRequest,
)
from app.services.auth import (
    authenticate_user,
    check_rate_limit,
    get_current_user,
    mark_user_verified,
    refresh_tokens,
    reset_password,
    send_reset_code,
    send_verification_code,
    signup_user,
    verify_email_code,
)
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=MessageResponse, status_code=201)
async def signup(
    body: SignupRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
):
    """Register a new user account.

    Creates the user and sends a verification code to their email.
    """
    # Rate limit: max 5 signups per minute per IP
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"signup:{ip}", max_requests=5)

    user = await signup_user(
        db,
        email=body.email,
        password=body.password,
        name=body.name,
    )

    # Generate and dispatch a verification code. Never include it in an HTTP response.
    await send_verification_code(user.email)
    return MessageResponse(message="Registration received. Check your email to verify the account.")


@router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
):
    """Authenticate user and return JWT token pair."""
    # Rate limit: max 10 login attempts per minute per IP
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"login:{ip}", max_requests=10)

    user, access_token, refresh_token = await authenticate_user(
        db,
        email=body.email,
        password=body.password,
        request=request,
    )

    # Keep the long-lived credential out of JavaScript. Secure is mandatory in production.
    response.set_cookie(
        key="chl_refresh",
        value=refresh_token,
        httponly=True,
        secure=settings.APP_ENV.lower() == "production",
        samesite="lax",
        max_age=settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )
    return LoginResponse(
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role,
            verified=user.verified,
            created_at=user.created_at,
        ),
        access_token=access_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
):
    """Rotate the HttpOnly refresh cookie and return a short-lived access token."""
    refresh_token = request.cookies.get("chl_refresh")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh session")
    _, access_token, new_refresh_token = await refresh_tokens(db, refresh_token)
    response.set_cookie(
        key="chl_refresh", value=new_refresh_token, httponly=True,
        secure=settings.APP_ENV.lower() == "production", samesite="lax",
        max_age=settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 60 * 60, path="/api/v1/auth",
    )
    return TokenResponse(access_token=access_token)


@router.post("/verify", response_model=MessageResponse)
async def verify_email(
    body: VerifyRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """Verify a user's email address with a 6-digit code."""
    valid = await verify_email_code(body.email, body.code)
    if not valid:
        return MessageResponse(message="Invalid or expired verification code")

    await mark_user_verified(db, body.email)
    return MessageResponse(message="Email verified successfully")


@router.post("/reset-password", response_model=MessageResponse)
async def request_reset_password(
    body: ResetPasswordRequest,
    request: Request,
):
    """Request a reset without revealing whether an account exists."""
    ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"password-reset:{ip}", max_requests=5)
    await send_reset_code(body.email)
    return MessageResponse(message="If the address is eligible, reset instructions have been sent.")


@router.post("/reset-password/confirm", response_model=MessageResponse)
async def confirm_reset_password(
    body: ResetPasswordConfirmRequest,
    db: AsyncSession = Depends(get_async_db),
):
    """Confirm password reset with code and new password."""
    await reset_password(
        db,
        email=body.email,
        code=body.code,
        new_password=body.new_password,
    )
    return MessageResponse(message="Password reset successfully")


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Return the currently authenticated user's profile."""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        verified=current_user.verified,
        created_at=current_user.created_at,
    )
