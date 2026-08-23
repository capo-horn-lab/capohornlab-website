"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import admin, auth, contact, newsletter, requests, research_suggestions
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

from app.core.redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup / shutdown."""
    # Ensure schema exists (idempotent; Alembic handles PG in docker-compose,
    # this covers SQLite / fresh deployments).
    try:
        from app.core.database import Base, async_engine  # noqa: PLC0415
        import app.models  # noqa: F401, PLC0415  # register all models
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:  # noqa: BLE001
        logger.exception("DB schema init failed - endpoints will report DB errors")
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(requests.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(newsletter.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")
app.include_router(research_suggestions.router, prefix="/api/v1")
app.include_router(research_suggestions.admin_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "ok", "version": settings.APP_VERSION}
