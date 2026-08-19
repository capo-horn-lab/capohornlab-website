"""Database engine and session management."""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Async engine — used by FastAPI endpoints
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

_is_sqlite = settings.async_database_url.startswith("sqlite")

_engine_kwargs: dict = {"echo": settings.DEBUG}
if not _is_sqlite:
    _engine_kwargs["pool_size"] = 5
    _engine_kwargs["max_overflow"] = 10

async_engine = create_async_engine(settings.async_database_url, **_engine_kwargs)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Sync engine — used by Alembic migrations
sync_engine = create_engine(settings.sync_database_url, **_engine_kwargs)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base model class for all SQLAlchemy models."""


async def get_async_db():
    """FastAPI dependency that yields an async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
