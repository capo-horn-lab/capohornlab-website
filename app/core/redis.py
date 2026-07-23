"""Redis client for rate limiting, caching, and token blacklisting."""

from __future__ import annotations

from typing import Optional

import redis.asyncio as aioredis

from app.core.config import settings

# Lazy-init singleton
_redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    """Return a shared async Redis connection."""
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.redis_url,
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection gracefully."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
