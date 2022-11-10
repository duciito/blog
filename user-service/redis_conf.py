import redis.asyncio as aioredis

from config import get_settings

redis_client = None


def get_redis_client() -> aioredis.Redis:
    if not redis_client:
        settings = get_settings()
        return aioredis.Redis(host=settings.redis_host, port=settings.redis_port)
    return redis_client
