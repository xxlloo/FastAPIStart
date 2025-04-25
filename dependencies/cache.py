from typing import AsyncGenerator

import aioredis
from aioredis import ConnectionPool, Redis

from config.config import settings


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis_url = f"{settings.REDIS_URL}"

    pool = ConnectionPool.from_url(
        redis_url,
        db=settings.REDIS_DB,
        max_connections=settings.MAX_POOL_SIZE,
        socket_connect_timeout=settings.TIMEOUT,
        socket_timeout=settings.TIMEOUT,
    )

    redis = aioredis.Redis(
        connection_pool=pool,
        decode_responses=settings.DECODE_RESPONSES,
        health_check_interval=30,
    )

    try:
        yield redis
    finally:
        await redis.close()
        await pool.disconnect()
