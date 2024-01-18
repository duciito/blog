from functools import lru_cache

import redis.asyncio as aioredis
from config import get_settings


@lru_cache
def get_redis_client() -> aioredis.Redis:
    settings = get_settings()
    return aioredis.Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )
